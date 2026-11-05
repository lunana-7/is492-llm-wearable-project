"""Local CP3 demo service. Raw audio, transcript and draft live only in memory."""
import io
import json
import os
from pathlib import Path
import re
import threading
import time
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

RATE = 16000
LIMIT = RATE * 2 * 20 + 44
PROMPT = (Path(__file__).resolve().parents[1] / "prompts/speech-summary-v1.txt").read_text()
CONTACT = re.compile(r"[\w.+-]+@[\w.-]+\.\w+|(?<!\w)(?:\d[ .()-]*){7,}(?!\w)")
MODEL = "qwen3:8b"
DIRECTIVE = re.compile(r"\b(?:ignore|override|disregard) (?:all |the |your )?(?:previous |prior |system )?(?:instructions|rules|prompt)\b", re.I)


def samples(payload):
    import numpy as np
    try:
        with wave.open(io.BytesIO(payload)) as wav:
            frames = wav.getnframes()
            if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) != (1, 2, RATE):
                raise ValueError("Use 16 kHz mono PCM16 audio.")
            if not 0 < frames <= 20 * RATE:
                raise ValueError("Record up to 20 seconds.")
            raw = wav.readframes(frames)
            if len(raw) != frames * 2:
                raise ValueError("Incomplete audio.")
    except (EOFError, wave.Error) as exc:
        raise ValueError("Invalid WAV file.") from exc
    return np.frombuffer(raw, dtype="<i2").astype("float32") / 32768


def approved_candidate(transcript, quote):
    if not isinstance(quote, str):
        raise ValueError("Invalid model response.")
    quote = quote.strip()
    if not quote or len(quote) > 180 or quote not in transcript or CONTACT.search(quote) or "[redacted]" in quote:
        return ""
    return quote


class LocalOnly(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def generate(transcript):
    if DIRECTIVE.search(transcript):
        return ""
    clean = CONTACT.sub("[redacted]", transcript)
    port = int(os.getenv("CP3_OLLAMA_PORT", "11434"))
    body = {"model": MODEL, "stream": False, "think": False, "format": "json",
            "options": {"temperature": 0, "num_predict": 160},
            "messages": [{"role": "system", "content": PROMPT}, {"role": "user", "content": clean}]}
    request = Request(f"http://127.0.0.1:{port}/api/chat", data=json.dumps(body).encode(),
                      headers={"Content-Type": "application/json"})
    # Disable environment proxies for local speech data.
    local = build_opener(ProxyHandler({}), LocalOnly())
    started = time.monotonic()
    with local.open(request, timeout=90) as response:
        result = json.load(response)
    print(json.dumps({"event": "local_summary", "ms": round(1000 * (time.monotonic() - started)),
                      "input_tokens": result.get("prompt_eval_count"), "output_tokens": result.get("eval_count")}), flush=True)
    parsed = json.loads(result["message"]["content"])
    return approved_candidate(clean, parsed["quote"])


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/draft" or self.headers.get("Origin") is not None:
            return self.reply(403, {"error": "Native demo clients only."})
        if self.headers.get("X-Recording-Consent") != "yes":
            return self.reply(403, {"error": "Recording consent required."})
        if self.headers.get("Content-Type") != "audio/wav":
            return self.reply(415, {"error": "Expected WAV audio."})
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            size = 0
        if not 0 < size <= LIMIT:
            return self.reply(413, {"error": "Invalid audio size."})
        if not self.server.slot.acquire(blocking=False):
            return self.reply(429, {"error": "Busy. Try again after the current draft."})
        try:
            self.connection.settimeout(10)
            audio = samples(self.rfile.read(size))
            segments, _ = self.server.whisper.transcribe(audio, language="en", vad_filter=True)
            transcript = " ".join(s.text.strip() for s in segments).strip()
            draft = generate(transcript) if transcript else ""
            self.reply(200, {"draft": draft})
        except ValueError:
            self.reply(422, {"error": "Invalid audio or unusable model result. Try again."})
        except Exception:
            self.reply(503, {"error": "Inference unavailable. Check local models and retry."})
        finally:
            self.server.slot.release()


def serve():
    from faster_whisper import WhisperModel
    whisper = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    with ThreadingHTTPServer(("127.0.0.1", 8765), Handler) as server:
        server.whisper = whisper
        server.slot = threading.BoundedSemaphore(1)
        print("Speech demo ready on 127.0.0.1:8765", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    serve()
