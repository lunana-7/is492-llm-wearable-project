"""Exercise the actual HTTP handler. Only the model boundary is replaced in failure tests."""
import http.client
import json
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import Mock, patch
from http.server import ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app/speech"))
import server


class Service(unittest.TestCase):
    def setUp(self):
        self.http = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        self.http.slot = threading.BoundedSemaphore(1)
        self.http.whisper = Mock()
        threading.Thread(target=self.http.serve_forever, daemon=True).start()
        self.addCleanup(self.http.server_close)
        self.addCleanup(self.http.shutdown)
        self.wav = (ROOT / "tests/fixtures/office-hours.wav").read_bytes()

    def post(self, wav=None, consent="yes", **headers):
        client = http.client.HTTPConnection(*self.http.server_address)
        try:
            client.request("POST", "/draft", self.wav if wav is None else wav,
                           {"Content-Type": "audio/wav", "X-Recording-Consent": consent, **headers})
            response = client.getresponse()
            return response.status, json.loads(response.read())
        finally:
            client.close()

    def test_consent_and_origin_precede_inference(self):
        self.assertEqual(self.post(consent="no")[0], 403)
        self.assertEqual(self.post(Origin="https://example.com")[0], 403)
        self.http.whisper.transcribe.assert_not_called()

    def test_busy_then_silent_input_recovers(self):
        self.http.slot.acquire()
        self.assertEqual(self.post()[0], 429)
        self.http.slot.release()
        self.http.whisper.transcribe.return_value = ([], None)
        with patch.object(server, "generate") as model:
            self.assertEqual(self.post(), (200, {"draft": ""}))
            model.assert_not_called()

    def test_invalid_input_and_model_outage_recover(self):
        self.assertEqual(self.post(b"invalid")[0], 422)
        self.http.whisper.transcribe.return_value = ([Mock(text="Bring the chart.")], None)
        with patch.object(server, "generate", side_effect=[TimeoutError(), "Bring the chart."]):
            self.assertEqual(self.post()[0], 503)
            self.assertEqual(self.post(), (200, {"draft": "Bring the chart."}))
