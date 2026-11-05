"""Run against the real, already-started demo service. No model doubles."""
import json
from pathlib import Path
from urllib.request import Request, urlopen

fixture = Path(__file__).resolve().parents[1] / "fixtures/office-hours.wav"
request = Request("http://127.0.0.1:8765/draft", data=fixture.read_bytes(),
                  headers={"Content-Type": "audio/wav", "X-Recording-Consent": "yes"})
with urlopen(request, timeout=110) as response:
    quote = json.load(response)["draft"]
if "chart" not in quote.lower() or "office hours" not in quote.lower():
    raise SystemExit(f"Unexpected output for synthetic fixture: {quote!r}")
print("Real transcription and summary passed:", quote)
