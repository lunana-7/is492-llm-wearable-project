"""Student review state and explicit approval-only local persistence."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
import uuid

from core import CONTACT, InvalidInput, sanitize_transcript, validate_quote

REPOSITORY = Path(__file__).resolve().parents[3]


class Review:
    def __init__(self, student_id, consent):
        if consent is not True:
            raise InvalidInput("Recording consent is required.")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", student_id):
            raise InvalidInput("Use a pseudonymous student ID with letters, digits, _ or -.")
        self.student_id = student_id
        self.transcript = ""
        self.model_quote = ""
        self.summary = ""
        self.state = "consented"

    def set_transcript(self, text):
        if self.state in ("discarded", "saved"):
            raise InvalidInput("Start a new review.")
        self.transcript = sanitize_transcript(text)
        self.model_quote = ""
        self.summary = ""
        self.state = "transcript_reviewed"

    def set_draft(self, quote):
        if self.state != "transcript_reviewed":
            raise InvalidInput("Review the transcript first.")
        self.model_quote = validate_quote(self.transcript, {"quote": quote})
        self.summary = self.model_quote
        self.state = "draft" if self.summary else "transcript_reviewed"

    def edit(self, summary):
        if self.state != "draft":
            raise InvalidInput("Generate a draft before editing.")
        summary = summary.strip()
        if not summary or len(summary) > 180 or CONTACT.search(summary) or "[redacted]" in summary:
            raise InvalidInput("Use 1–180 characters without contact details.")
        self.summary = summary

    def discard(self):
        self.transcript = self.model_quote = self.summary = ""
        self.state = "discarded"

    def save(self, output, approval):
        if self.state != "draft" or approval != self.student_id:
            raise InvalidInput("Explicit approval for this student is required.")
        output = Path(output).expanduser().absolute()
        if output.resolve().is_relative_to(REPOSITORY):
            raise InvalidInput("Save demo notes outside the repository.")
        record = {
            "schema_version": 1, "record_id": str(uuid.uuid4()),
            "student_id": self.student_id, "summary": self.summary,
            "model_quote": self.model_quote,
            "student_edited": self.summary != self.model_quote,
            "approved": True, "recording_consent": True,
            "approved_at": datetime.now(timezone.utc).isoformat(),
        }
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, delete=False) as file:
                temporary = Path(file.name)
                json.dump(record, file, ensure_ascii=False, indent=2)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())
            # Atomic publication without replacing any existing path.
            os.link(temporary, output)
        finally:
            if temporary:
                temporary.unlink(missing_ok=True)
        self.state = "saved"
        self.transcript = ""
        return record


def delete_note(path, confirmation):
    path = Path(path).expanduser()
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 16000:
        raise InvalidInput("Choose an approved note file.")
    record = json.loads(path.read_text())
    if not isinstance(record, dict) or record.get("approved") is not True or record.get("schema_version") != 1:
        raise InvalidInput("Unrecognized note format.")
    if not record.get("student_id") or confirmation != record["student_id"]:
        raise InvalidInput("Confirm the note's student ID.")
    path.unlink()
