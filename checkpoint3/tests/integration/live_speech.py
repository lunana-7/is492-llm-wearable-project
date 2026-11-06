"""Opt-in real HTTP -> Whisper -> Qwen -> edited approval -> deletion smoke."""
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "app/speech"))
from demo import Client
from server import read_token
from workflow import Review, delete_note

audio = (Path(__file__).resolve().parents[1] / "fixtures/office-hours.wav").read_bytes()
client = Client(read_token())
transcript = client.call("transcribe", audio, "audio/wav")["transcript"]
review = Review("synthetic-demo-01", True)
review.set_transcript(transcript)
quote = client.call("summarize", json.dumps({"transcript": review.transcript}).encode(), "application/json")["quote"]
review.set_draft(quote)
if "chart" not in quote.casefold() or "office hours" not in quote.casefold():
    raise SystemExit("Live model output did not retain the fixture's core follow-up.")
with tempfile.TemporaryDirectory() as tmp:
    note = Path(tmp) / "approved.json"
    if note.exists():
        raise AssertionError("Draft was persisted before approval.")
    review.edit("Bring the revised chart to office hours.")
    review.save(note, "synthetic-demo-01")
    assert json.loads(note.read_text())["summary"] == review.summary
    delete_note(note, "synthetic-demo-01")
    assert not note.exists()
print(json.dumps({"test": "live_speech_review_save_delete", "status": "passed", "synthetic_quote": quote}))
