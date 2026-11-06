# CP3 verification record

**Min Kim — test record. Initial runs: November 5, 2026. Speech test rerun: November 6, 2026.**

For the November 5 Android run, application source was reviewed at commit `182d5e6`. The Android production source matches the team's CameraAccess implementation. This run adds the Min test suite through the opt-in Gradle init script.

## Automated results

| Run | Environment | Outcome |
|---|---|---|
| MinSafetyIntegrationTest | Android 15 / API 35 ARM64 emulator, Pixel 5 device profile; Android compile SDK 36; JDK 17; project Gradle 8.14.1 | 8 tests passed, 0 failures; Gradle BUILD SUCCESSFUL |
| test_prompt_contract.py | Python 3.12 with requirements-prompts.txt | 4 tests passed, 0 failures |

The Android command built the application and instrumentation APK before executing the tests. The embedding smoke test executed the bundled TFLite model on synthetic pixels. The matching tests used controlled vectors. The roster tests encrypted, decoded, reloaded and deleted entries through the current storage methods.

Run commands and individual method coverage are in [the integration guide](README.md) and [unit guide](../unit/README.md). Local Android XML and HTML test reports are generated under `app/CameraAccess/app/build/outputs/androidTest-results/` and `app/CameraAccess/app/build/reports/androidTests/`.

## Evidence boundaries

- The new suite checks method behavior and a real model invocation. It does not measure recognition accuracy from camera images.
- The stop test checks state and callback behavior. It does not execute the live loop's 30-second/8-second timers or prove that the lens clears.
- The reload tests reset the singleton and decode SharedPreferences in the same instrumentation process. Cold-start recovery and damaged storage remain separate checks.
- Android consent enforcement, authenticated student controls, term-end deletion and app-to-speech integration remain implementation work. The local speech flow is verified separately below.
- Physical microphone, glasses registration/display, lighting robustness, stale-card recovery and full demo timing remain unverified in this run.
- Neha's previously reported eleven live prompt cases are recorded in app/prompts/README.md. This run repeats the four contract tests only.
- The earlier deleted speech prototype's eight/ten-test reports are excluded from this record.

## Before submission

Min coordinates M-01 through M-10 in the integration guide with the component owners. Attach actual device observations and issue owners. Submit only claims supported by the current commit and recorded outcomes.

## Speech-module run on November 5, 2026

| Check | Observed result |
|---|---|
| test_speech_workflow.py | 10 tests passed |
| test_speech_service.py | 6 tests passed |
| live_speech.py | Actual HTTP → Whisper tiny.en → Qwen3 8B → student edit → approval → private JSON → deletion passed |
| demo.py normal CLI with synthetic WAV | Consent, transcript review, summary review, exact student-ID approval and deletion completed successfully |

The live fixture returned “I will bring the revised water quality chart to office hours.” The edited smoke saved “Bring the revised chart to office hours.” and then deleted the file. The CLI run independently saved the accepted quote and deleted it through its normal deletion command.

This run used Python 3.12, faster-whisper 1.2.1, CPU int8 Whisper and local qwen3:8b via Ollama. Service logs reported transcription durations of 260 and 181 ms and model-step durations of 4,761 and 547 ms for the smoke and CLI calls. Both model calls reported 159 input tokens and 18 output tokens. These are two synthetic observations with different warm-up state, rather than a latency benchmark. Local inference carries no per-call provider API fee; hardware and energy costs were not measured.

The sixteen automated speech tests include controlled failures at the model boundary. The two live runs use actual model inference. Audio capture used a synthetic WAV in both live runs. Real microphone quality and the team’s Android/glasses integration remain unverified. Existing Android test results above are from the preceding run, with no new Android production changes in this speech addition.

## November 6 speech test rerun

I reran the two speech suites against repository commit `5e876ed` using Python 3.12.13. No application code was changed for this run.

Commands, from `checkpoint3/` with the speech dependencies installed:

```sh
python -m unittest discover -s tests/unit -p 'test_speech_workflow.py'
python -m unittest discover -s tests/integration -p 'test_speech_service.py'
```

| Suite | Actual result |
|---|---|
| Speech workflow | 10 tests, 0 failures; `OK` |
| Speech HTTP service | 6 tests, 0 failures; `OK` |

The HTTP tests run the real request handler with controlled model responses. The workflow tests exercise validation, approval and file operations; microphone cancellation uses a mocked recorder. This rerun did not execute Whisper/Qwen inference, an Android emulator, a physical microphone or glasses. The November 5 results above remain the separate evidence for actual model execution and Android component behavior.

For CP3, this establishes executable speech-module tests and documented safety checks. Full application acceptance still requires the Android UI/storage connections and a recorded real-device run of the workflow in [the integration handoff](../../docs/speech-integration-handoff.md#min--integration-verification).
