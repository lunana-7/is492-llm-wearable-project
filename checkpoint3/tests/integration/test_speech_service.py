"""Real HTTP handler with controlled model failures for reproducible error checks."""
import http.client
import json
from pathlib import Path
import sys
import threading
import time
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "app/speech"))
from core import InvalidModelOutput
from server import SpeechServer

TOKEN = "synthetic-test-token-with-at-least-32-characters"
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/office-hours.wav"


class SpeechHttp(unittest.TestCase):
    def setUp(self):
        self.models = Mock()
        self.models.transcribe.return_value = "Bring the chart to office hours."
        self.models.summarize.return_value = "Bring the chart to office hours."
        self.server = SpeechServer(("127.0.0.1", 0), self.models, TOKEN)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)

    def post(self, route="/transcribe", payload=None, **extra):
        if payload is None:
            payload = FIXTURE.read_bytes() if route == "/transcribe" else b'{"transcript":"Bring the chart."}'
        headers = {"Content-Type": "audio/wav" if route == "/transcribe" else "application/json",
                   "Authorization": "Bearer " + TOKEN, "X-Recording-Consent": "yes", **extra}
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=5)
        try:
            connection.request("POST", route, payload, headers)
            result = connection.getresponse()
            return result.status, json.loads(result.read())
        finally:
            connection.close()

    def test_auth_consent_and_origin_block_before_inference(self):
        for headers in ({"Authorization": ""}, {"X-Recording-Consent": "no"}, {"Origin": "https://example.org"}):
            self.assertEqual(self.post(**headers)[0], 403)
        self.models.transcribe.assert_not_called()

    def test_valid_transcription_then_summary(self):
        self.assertEqual(self.post()[1]["transcript"], "Bring the chart to office hours.")
        self.assertEqual(self.post("/summarize")[1]["quote"], "Bring the chart to office hours.")

    def test_invalid_format_schema_and_size(self):
        self.assertEqual(self.post(payload=b"invalid")[0], 422)
        self.assertEqual(self.post(**{"Content-Type": "text/plain"})[0], 415)
        self.assertEqual(self.post(payload=b"", **{"Content-Length": "650000"})[0], 413)
        self.assertEqual(self.post("/summarize", payload=b'{"transcript":"ok","extra":1}')[0], 422)
        self.assertEqual(self.post("/summarize", payload=b'{"transcript":null}')[0], 422)
        self.models.transcribe.assert_not_called()

    def test_busy_then_retry_and_rate_window_expiry(self):
        self.server.slot.acquire()
        self.assertEqual(self.post()[0], 429)
        self.server.slot.release()
        self.assertEqual(self.post()[0], 200)
        self.server.requests.extend([time.monotonic()] * 12)
        self.assertEqual(self.post()[0], 429)
        self.server.requests.clear()
        self.server.requests.extend([time.monotonic() - 61] * 12)
        self.assertEqual(self.post()[0], 200)

    def test_model_failure_timeout_bad_output_then_recovery(self):
        self.models.summarize.side_effect = [
            RuntimeError("private internal diagnostic"),
            TimeoutError(),
            InvalidModelOutput("invalid"),
            "Bring the chart.",
        ]
        for expected in (503, 504, 502, 200):
            status, body = self.post("/summarize")
            self.assertEqual(status, expected)
            self.assertNotIn("private", json.dumps(body))

    def test_transcript_contacts_removed_before_summary(self):
        self.post("/summarize", payload=json.dumps({"transcript": "Email synthetic@example.org"}).encode())
        self.models.summarize.assert_called_once_with("Email [redacted]")
