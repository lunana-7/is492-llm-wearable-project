"""Audio validation, transcript minimization, and local model boundaries."""
import io
import json
from pathlib import Path
import re
import time
import wave
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
SETTINGS = json.loads((ROOT / "model_settings.json").read_text())
SCHEMA = json.loads((ROOT / "output_schema.json").read_text())
PROMPT = (ROOT / "summary_prompt.txt").read_text()
CONTACT = re.compile(r"[\w.+-]+@[\w.-]+\.\w+|(?<!\w)(?:\d[ .()-]*){7,}(?!\w)")
OVERRIDE = re.compile(r"\b(?:ignore|override|disregard) (?:all |the |your )?(?:previous |prior |system )?(?:instructions|rules|prompt)\b", re.I)
MAX_AUDIO_BYTES = 16000 * 2 * 20 + 4096


class InvalidInput(ValueError):
    pass


class InvalidModelOutput(ValueError):
    pass


def sanitize_transcript(text):
    if not isinstance(text, str) or not text.strip() or len(text) > 4000:
        raise InvalidInput("Transcript must contain 1–4000 characters.")
    return CONTACT.sub("[redacted]", text.strip())


def audio_samples(payload):
    import numpy as np
    try:
        with wave.open(io.BytesIO(payload)) as wav:
            if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) != (1, 2, 16000):
                raise InvalidInput("Use mono 16 kHz PCM16 WAV.")
            frames = wav.getnframes()
            if not 0 < frames <= 20 * 16000:
                raise InvalidInput("Audio must be between zero and twenty seconds.")
            raw = wav.readframes(frames)
            if len(raw) != frames * 2:
                raise InvalidInput("Audio is incomplete.")
    except (EOFError, wave.Error) as exc:
        raise InvalidInput("Invalid WAV file.") from exc
    return np.frombuffer(raw, dtype="<i2").astype("float32") / 32768


def validate_quote(transcript, response):
    try:
        Draft202012Validator(SCHEMA).validate(response)
    except Exception as exc:
        raise InvalidModelOutput("Model output failed its schema.") from exc
    quote = response["quote"].strip()
    if quote and (quote not in transcript or CONTACT.search(quote) or "[redacted]" in quote):
        raise InvalidModelOutput("Model quote is unsupported or contains contact information.")
    return quote


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class LocalModels:
    def __init__(self, whisper, ollama_port=11434):
        self.whisper = whisper
        self.ollama_port = ollama_port

    def transcribe(self, audio):
        segments, _ = self.whisper.transcribe(audio, language="en", vad_filter=True)
        text = " ".join(s.text.strip() for s in segments).strip()
        return sanitize_transcript(text) if text else ""

    def summarize(self, transcript):
        clean = sanitize_transcript(transcript)
        if OVERRIDE.search(clean):
            return ""
        body = {
            "model": SETTINGS["summary_model"], "think": False, "stream": False,
            "format": SCHEMA,
            "options": {"temperature": 0, "num_predict": SETTINGS["num_predict"]},
            "messages": [{"role": "system", "content": PROMPT}, {"role": "user", "content": clean}],
        }
        request = Request(
            f"http://127.0.0.1:{self.ollama_port}/api/chat",
            data=json.dumps(body).encode(), headers={"Content-Type": "application/json"},
        )
        client = build_opener(ProxyHandler({}), NoRedirects())
        started = time.monotonic()
        with client.open(request, timeout=SETTINGS["model_timeout_seconds"]) as response:
            raw = response.read(65537)
        if len(raw) > 65536:
            raise InvalidModelOutput("Model response is too large.")
        try:
            result = json.loads(raw)
            quote = validate_quote(clean, json.loads(result["message"]["content"]))
        except (ValueError, KeyError, TypeError) as exc:
            raise InvalidModelOutput("Model returned an unusable draft.") from exc
        print(json.dumps({
            "event": "summary_completed",
            "milliseconds": round(1000 * (time.monotonic() - started)),
            "input_tokens": result.get("prompt_eval_count"),
            "output_tokens": result.get("eval_count"),
        }), flush=True)
        return quote
