"""Interactive standalone speech review. Run from checkpoint3/min."""
import argparse
import io
import json
import os
from pathlib import Path
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen
import wave

FIXTURE = Path(__file__).resolve().parents[2] / "tests/fixtures/office-hours.wav"


def record():
    import sounddevice as sd
    print("Recording eight seconds on the laptop microphone…", flush=True)
    pcm = sd.rec(8 * 16000, samplerate=16000, channels=1, dtype="int16", blocking=True)
    stream = io.BytesIO()
    with wave.open(stream, "wb") as wav:
        wav.setparams((1, 2, 16000, 0, "NONE", ""))
        wav.writeframes(pcm.astype("<i2").tobytes())
    return stream.getvalue()


def review(draft, output):
    print("Draft:", draft)
    text = input("Enter a revision, or press Enter to keep this quote: ").strip() or draft
    if len(text) > 180:
        raise ValueError("Keep the approved follow-up within 180 characters.")
    if input("Type APPROVE to save, or press Enter to discard: ").strip() != "APPROVE":
        return False
    # Create a private file exclusively so an existing note cannot be overwritten.
    with os.fdopen(os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as file:
        file.write(text + "\n")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mic", action="store_true", help="Record now instead of using synthetic audio")
    parser.add_argument("--output", type=Path, required=True, help="New private note path outside the repository")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Choose a new output file.")
    if input("Everyone speaking agrees to local processing? Type YES to proceed: ").strip() != "YES":
        return
    audio = record() if args.mic else FIXTURE.read_bytes()
    request = Request("http://127.0.0.1:8765/draft", data=audio,
                      headers={"Content-Type": "audio/wav", "X-Recording-Consent": "yes"})
    with urlopen(request, timeout=110) as response:
        draft = json.load(response)["draft"]
    if draft:
        print("Saved." if review(draft, args.output) else "Discarded.")
    else:
        print("No supported follow-up found. Try a clearer recording.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, URLError) as exc:
        sys.exit(f"Demo stopped: {exc}")
