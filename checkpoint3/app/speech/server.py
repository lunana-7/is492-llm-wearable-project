"""Loopback-only speech API. Start with python server.py."""
from collections import deque
import hmac
import json
import os
from pathlib import Path
import secrets
import socket
import stat
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError

from core import InvalidInput, InvalidModelOutput, LocalModels, MAX_AUDIO_BYTES, SETTINGS, audio_samples, sanitize_transcript

TOKEN_PATH = Path.home() / ".config/contextlens/speech-token"


def read_token(path=TOKEN_PATH):
    if path.is_symlink():
        raise ValueError("Token file must be a regular private file.")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077:
        raise ValueError("Restrict token file permissions to its owner.")
    token = path.read_text().strip()
    if len(token) < 32:
        raise ValueError("Token file is invalid.")
    return token


def ensure_token(path=TOKEN_PATH):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as file:
            file.write(secrets.token_urlsafe(32))
    except FileExistsError:
        pass
    return read_token(path)


class SpeechServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, models, token):
        super().__init__(address, Handler)
        self.models = models
        self.token = token
        self.slot = threading.BoundedSemaphore(1)
        self.rate_lock = threading.Lock()
        self.requests = deque()

    def allow_request(self):
        with self.rate_lock:
            now = time.monotonic()
            while self.requests and now - self.requests[0] >= 60:
                self.requests.popleft()
            if len(self.requests) >= SETTINGS["requests_per_minute"]:
                return False
            self.requests.append(now)
            return True


class Handler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(10)

    def log_message(self, *args):
        pass

    def reply(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        if status == 429:
            self.send_header("Retry-After", "60")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        if self.path == "/health":
            self.reply(200, {"status": "ready"})
        else:
            self.reply(404, {"error": "unknown_route"})

    def do_POST(self):
        if self.path not in ("/transcribe", "/summarize"):
            return self.reply(404, {"error": "unknown_route"})
        expected = "Bearer " + self.server.token
        if self.headers.get("Origin") is not None or not hmac.compare_digest(
            self.headers.get("Authorization", "").encode(), expected.encode()
        ):
            return self.reply(403, {"error": "access_denied"})
        if self.headers.get("X-Recording-Consent") != "yes":
            return self.reply(403, {"error": "consent_required"})
        if self.headers.get("Transfer-Encoding"):
            return self.reply(400, {"error": "content_length_required"})
        required_type = "audio/wav" if self.path == "/transcribe" else "application/json"
        if self.headers.get("Content-Type") != required_type:
            return self.reply(415, {"error": "unsupported_content_type"})
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            size = 0
        limit = MAX_AUDIO_BYTES if self.path == "/transcribe" else 20000
        if not 0 < size <= limit:
            return self.reply(413, {"error": "invalid_size"})
        if not self.server.slot.acquire(blocking=False):
            return self.reply(429, {"error": "busy"})
        started = time.monotonic()
        try:
            if not self.server.allow_request():
                return self.reply(429, {"error": "rate_limit"})
            raw = self.rfile.read(size)
            if len(raw) != size:
                raise InvalidInput("Incomplete body.")
            if self.path == "/transcribe":
                transcript = self.server.models.transcribe(audio_samples(raw))
                self.reply(200, {"transcript": transcript})
            else:
                body = json.loads(raw)
                if not isinstance(body, dict) or set(body) != {"transcript"}:
                    raise InvalidInput("Expected transcript field.")
                transcript = sanitize_transcript(body["transcript"])
                self.reply(200, {"quote": self.server.models.summarize(transcript)})
        except socket.timeout:
            self.reply(504, {"error": "timeout"})
        except InvalidModelOutput:
            self.reply(502, {"error": "invalid_model_output"})
        except (InvalidInput, json.JSONDecodeError, UnicodeDecodeError):
            self.reply(422, {"error": "invalid_input"})
        except HTTPError as exc:
            self.reply(429 if exc.code == 429 else 503, {"error": "model_unavailable"})
        except Exception:
            self.reply(503, {"error": "inference_unavailable"})
        finally:
            self.server.slot.release()
            print(json.dumps({"event": self.path[1:], "milliseconds": round(1000 * (time.monotonic() - started))}), flush=True)


def main():
    from faster_whisper import WhisperModel
    token = ensure_token()
    whisper = WhisperModel(SETTINGS["whisper_model"], device="cpu", compute_type="int8")
    models = LocalModels(whisper, int(os.getenv("CP3_OLLAMA_PORT", "11434")))
    with SpeechServer(("127.0.0.1", 8765), models, token) as service:
        print("Speech API ready on 127.0.0.1:8765", flush=True)
        service.serve_forever()


if __name__ == "__main__":
    main()
