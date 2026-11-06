# Speech and reviewed follow-ups

**Owner — Min Kim.**

This module provides real local speech transcription, an extractive follow-up summary, transcript correction, student editing, approval-only saving, discard and deletion. Use the terminal demo on a laptop now. [Android integration requirements](../../docs/speech-integration-handoff.md) specify the changes Aman and Steven need to make to connect the team’s app.

## Files

| File | Responsibility |
|---|---|
| server.py | Authenticated loopback API, consent checks, audio limits, request limits and failure responses |
| core.py | WAV validation, local Whisper/Qwen calls, PII pattern redaction and source-quote validation |
| workflow.py | Transcript/draft state, explicit approval, private atomic export and deletion |
| demo.py | Microphone or WAV input and interactive student review |
| summary_prompt.txt | Versioned follow-up extraction instructions |
| output_schema.json | Exact model response shape |
| model_settings.json | Model names, generation settings and limits |

The summary is a short source quote about an academic follow-up. A student can revise it before saving. The original model quote and the final edited summary are distinguishable in the approved export.

## Install and start

Use Python 3.12, Ollama and a microphone-enabled macOS/Linux laptop. From the repository root:

```sh
cd checkpoint3
python3.12 -m venv .venv
.venv/bin/python -m pip install -r app/speech/requirements.txt
ollama pull qwen3:8b
```

Start `ollama serve` in a separate terminal if Ollama is not already running. Then, from `checkpoint3/`:

```sh
.venv/bin/python app/speech/server.py
```

Wait for “Speech API ready”. The first startup downloads Whisper tiny.en. Qwen also needs several GB of storage. Model inference runs locally after setup.

The server binds to `127.0.0.1:8765` and generates an owner-only token at `~/.config/contextlens/speech-token`. The local demo reads it automatically. Do not commit or paste this token into logs. For a different Ollama loopback port, set `CP3_OLLAMA_PORT` before starting the service. The sample .env file is documentation; the application reads process environment variables.

The live microphone uses sounddevice. Grant the terminal microphone permission on the laptop. On systems where sounddevice cannot load PortAudio, install the platform’s PortAudio library before recording. WAV input exercises the same review and model flow independently of microphone setup.

## Live demonstration

In a second terminal, from `checkpoint3/`:

```sh
.venv/bin/python app/speech/demo.py --student-id demo-01 --output ~/cp3-followup.json
```

1. Ask everyone who will speak for consent. Type YES to begin.
2. Speak during the eight-second recording. Example “I will bring the revised water quality chart to office hours.”
3. Inspect the transcript. Correct a recognition error or enter /discard to cancel.
4. Inspect the selected follow-up. Edit it or enter /discard.
5. Verify the pseudonymous student ID and final wording. Type the exact student ID to approve and save. Pressing Enter discards.
6. Delete the note after the demonstration:

```sh
.venv/bin/python app/speech/demo.py --delete ~/cp3-followup.json
```

Confirm the student ID when prompted. Use a new output filename for each approved note. Existing files are protected against replacement. Exports must be outside the repository.

For a reproducible synthetic recording:

```sh
.venv/bin/python app/speech/demo.py --student-id demo-01 \
  --wav tests/fixtures/office-hours.wav --output ~/cp3-followup.json
```

The CLI is a supervised prototype. The typed student ID expresses approval within this demo and does not authenticate a real student.

## Failure and recovery

If a model is down or a request is busy, the CLI offers RETRY or cancellation. On HTTP 429, wait for the current request or rate window before retrying. Inference errors never trigger automatic saving. A changed transcript invalidates its older summary draft. Empty or unsupported summaries cannot be saved.

To demonstrate recovery, stop Ollama before the summarization step, observe the error, restart it and choose RETRY. Do not stop someone else’s model process. Press Ctrl+C to cancel a recording; the client releases the microphone. A request already sent to the server can finish after the client closes.

## Test

From `checkpoint3/`:

```sh
.venv/bin/python -m unittest discover -s tests/unit -p 'test_speech_workflow.py'
.venv/bin/python -m unittest discover -s tests/integration -p 'test_speech_service.py'
.venv/bin/python tests/integration/live_speech.py
```

The first two suites cover local validation, consent, approval/discard, edits, private saving, deletion, authorization, HTTP errors, rate limits and retries. They use controlled model failures. The third requires the running API and actual models. It sends the synthetic WAV through Whisper and Qwen, edits/approves the output, verifies the saved record and deletes it.

## API contract

Both POST endpoints require `Authorization: Bearer <local token>` and `X-Recording-Consent: yes`. Browser-origin requests are rejected. The service allows one active inference request and up to twelve admitted requests per minute. The twelve-request limit covers both endpoints together.

| Endpoint | Body | Successful response |
|---|---|---|
| GET /health | Empty | {"status":"ready"} — service liveness only |
| POST /transcribe | audio/wav, mono PCM16, 16 kHz, at most 20 seconds | {"transcript":"…"}; empty string when no speech is found |
| POST /summarize | application/json, exactly {"transcript":"student-reviewed text"} | {"quote":"…"}; empty string when no supported follow-up exists |

Transcripts are limited to 4,000 characters. Quotes are limited to 180 characters and must occur verbatim in the redacted transcript. The server returns 403 for access/consent failure, 413 for invalid body size, 415 for unsupported content type, 422 for invalid input, 429 for busy/rate-limited requests, 502 for unusable model output, 503 for unavailable inference, and 504 for detected timeouts. Clients should display a retry/cancel choice and keep approved data intact.

## Storage and limits

Audio, transcripts and drafts live in memory. The local API has no database or save endpoint. The client writes only after approval. The JSON export contains schema_version, record_id, student_id, summary, model_quote, student_edited, approved, recording_consent and approved_at. It is created atomically with owner-only file permissions. It remains plaintext and needs manual deletion.

Email and digit-based phone patterns are redacted. Names, spoken numbers, sensitive academic content and transcription errors can still require manual correction. Explicit instruction-override patterns trigger abstention, and the model receives untrusted transcript text as data. These measures require human review and broader evaluation.

The current speech flow supports English. Actual microphone quality and Android/glasses integration require physical rehearsal. See the [current test record](../../tests/integration/RESULTS.md).
