# CP3 verification record

**Recorded by Min's test workflow on November 5, 2026.**

Application source reviewed at commit `182d5e6`. The Android production source matches the team's CameraAccess implementation. This run adds the Min test suite through the opt-in Gradle init script.

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
- Consent enforcement, authenticated student controls, term-end deletion, reviewed summaries and service rate-limit recovery remain implementation work.
- Physical microphone, glasses registration/display, lighting robustness, stale-card recovery and full demo timing remain unverified in this run.
- Neha's previously reported eleven live prompt cases are recorded in app/prompts/README.md. This run repeats the four contract tests only.
- The earlier deleted speech prototype's eight/ten-test reports are excluded from this record.

## Before submission

Min coordinates M-01 through M-10 in the integration guide with the component owners. Attach actual device observations and issue owners. Submit only claims supported by the current commit and recorded outcomes.
