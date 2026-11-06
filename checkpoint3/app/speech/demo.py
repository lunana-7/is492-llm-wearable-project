"""Run the supervised speech -> transcript review -> summary review -> save flow."""
import argparse
import io
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener
import wave

from core import MAX_AUDIO_BYTES, NoRedirects
from server import read_token
from workflow import Review, delete_note


def record():
    import sounddevice as sd
    print("Recording eight seconds. Speak now.", flush=True)
    try:
        pcm = sd.rec(8 * 16000, samplerate=16000, channels=1, dtype="int16")
        sd.wait()
    except sd.PortAudioError as exc:
        raise RuntimeError("Microphone unavailable. Check device selection and microphone permission, or use --wav.") from exc
    finally:
        sd.stop()
    stream = io.BytesIO()
    with wave.open(stream, "wb") as wav:
        wav.setparams((1, 2, 16000, 0, "NONE", ""))
        wav.writeframes(pcm.astype("<i2").tobytes())
    return stream.getvalue()


class Client:
    def __init__(self, token):
        self.token = token

    def call(self, route, payload, content_type):
        request = Request(
            "http://127.0.0.1:8765/" + route, data=payload,
            headers={"Authorization": "Bearer " + self.token, "X-Recording-Consent": "yes",
                     "Content-Type": content_type},
        )
        client = build_opener(ProxyHandler({}), NoRedirects())
        with client.open(request, timeout=105) as response:
            return json.load(response)


def interactive_call(client, route, payload, content_type):
    while True:
        try:
            return client.call(route, payload, content_type)
        except HTTPError as exc:
            print(f"Request failed (HTTP {exc.code}). Check the model/service; no note was saved.")
            if exc.code not in (429, 502, 503, 504):
                raise
            if input("Wait until the service is ready, then type RETRY; Enter cancels: ") != "RETRY":
                return None
        except (URLError, TimeoutError):
            print("The speech service is unreachable or timed out; no note was saved.")
            if input("Restore the service, then type RETRY; Enter cancels: ") != "RETRY":
                return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--student-id")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--wav", type=Path, help="Use an explicitly consented PCM16 WAV instead of the microphone")
    parser.add_argument("--delete", type=Path, help="Delete an approved local note")
    args = parser.parse_args()
    if args.delete:
        delete_note(args.delete, input("Enter the student ID to confirm deletion: ").strip())
        print("Note deleted.")
        return
    if not args.student_id or not args.output:
        parser.error("--student-id and --output are required for recording")
    if args.output.expanduser().exists():
        parser.error("Choose a new output file; existing notes are protected.")
    if input("All speakers consent to local transcription and summarization? Type YES: ") != "YES":
        print("Cancelled.")
        return
    review = Review(args.student_id, True)
    try:
        client = Client(read_token())
        if args.wav:
            with args.wav.open("rb") as file:
                audio = file.read(MAX_AUDIO_BYTES + 1)
            if len(audio) > MAX_AUDIO_BYTES:
                raise ValueError("Audio file is too large.")
        else:
            audio = record()
        result = interactive_call(client, "transcribe", audio, "audio/wav")
        if result is None or not result["transcript"]:
            print("No transcript to review.")
            return
        print("Transcript:", result["transcript"])
        correction = input("Edit transcript, Enter accepts, /discard cancels: ").strip()
        if correction == "/discard":
            return
        review.set_transcript(correction or result["transcript"])
        result = interactive_call(client, "summarize",
                                  json.dumps({"transcript": review.transcript}).encode(), "application/json")
        if result is None:
            return
        review.set_draft(result["quote"])
        if not review.summary:
            print("No supported follow-up found. Record again if useful.")
            return
        print("Draft:", review.summary)
        edited = input("Edit follow-up, Enter accepts, /discard cancels: ").strip()
        if edited == "/discard":
            return
        review.edit(edited or review.summary)
        print("Selected student:", review.student_id)
        print("Final follow-up:", review.summary)
        approval = input("Type the student ID to approve and save; Enter discards: ").strip()
        if approval != review.student_id:
            print("Discarded.")
            return
        review.save(args.output, approval)
        print("Approved note saved:", args.output.expanduser())
    finally:
        review.discard()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
    except (OSError, ValueError, RuntimeError, URLError) as exc:
        sys.exit(f"Stopped: {exc}")
