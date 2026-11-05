# Min Kim · Checkpoint 3

My deliverables are consented speech transcription, a reviewed follow-up summary, critical-path tests, the safety write-up, and the edge-case and safety demo. This laptop demo runs independently of the team’s Android project.

## Run

From `checkpoint3/min/`, install Python 3.12 dependencies and fetch the local model. Start Ollama in its own terminal (`ollama serve`) if necessary.

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r app/speech/requirements.txt
ollama pull qwen3:8b
.venv/bin/python app/speech/server.py
```

On its first run the server downloads Whisper tiny.en. Keep this terminal open. In a second terminal, from the same folder, run the synthetic audio demo:

```sh
.venv/bin/python app/speech/demo.py --output ~/cp3-demo-note.txt
```

Add `--mic` to record eight seconds live on the laptop. Grant microphone access when prompted. Use a new output filename each time. After consent, Whisper transcribes the clip and Qwen selects a supported quote. The student can edit, approve or discard the draft. Remove the approved local text file when finished.

## Verify

```sh
.venv/bin/python -m unittest discover -s tests/unit
.venv/bin/python -m unittest discover -s tests/integration
.venv/bin/python tests/integration/live_speech.py
```

The last command requires the running service. It sends synthetic speech through both models and checks the returned quote. The unit and HTTP suites cover approval, discard, invented details, contact redaction, instruction overrides, invalid audio, consent, busy responses and retries.

[Safety and privacy](docs/safety_privacy.md) · [My presentation cues](docs/demo.md)

The earlier [Android integration prototype and emulator tests](https://github.com/lunana-7/is492-llm-wearable-project/commit/15930b2b0561d289209de85d508f67dd38660434) remain available in Git history. The runnable deliverable here is the standalone laptop workflow.
