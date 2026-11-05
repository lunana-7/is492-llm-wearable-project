# Observability — CameraAccess (Checkpoint 3)

**Scope:** Actual Android source as uploaded in `checkpoint3/app/CameraAccess/`. Distinguish existing logging from recommended instrumentation. No production monitoring service or backend metrics database is present in the inspected source.

## 1. Existing observability

| Signal | Existing source | Status |
|---|---|---|
| Model tensor dimensions | `ui/FaceEmbedder.kt` → `Log.d("FaceEmbedder", ...)` | Implemented debug logging |
| Display attach / send errors | `ui/DisplayHelper.kt` → `Log.d` / `Log.e` | Implemented |
| Recognition status | `ui/LiveRecognizer.kt` → Compose `text` state | Implemented UI status; not a persistent metric |
| Unknown-face best score | `ui/LiveRecognizer.kt` status text | Implemented UI text; **do not export** |
| PixelCopy failures | `ui/LiveRecognizer.kt` status text after repeated failures | Implemented UI status |
| Recognition loop interval | `delay(500)` in `LiveRecognizer.kt` | Scheduling interval, **not** measured latency |
| Display refresh suppression | `DisplayHelper.shouldSend()` (15 s) | Implemented |
| LLM token usage / cost | No LLM client in inspected source | Not applicable / not implemented |

`LiveRecognizer` can show a recognized name and description in its status string, and `DisplayHelper` uses text-bearing display keys. **Do not collect raw status strings or identifying text in shared logs.**

## 2. How to inspect logs

In Android Studio, open **Logcat** while the app is running.

Example terminal command (Android SDK platform-tools required):

```bash
adb logcat -s FaceEmbedder:D DisplayHelper:D AndroidRuntime:E '*:S'
```

Useful manual observations:
- Does the device session and display attach successfully?
- Does the model initialize with the expected input/output dimensions?
- Are there display send failures or uncaught Android exceptions?
- Does recognition stop after the configured timeout?
- After deletion, does the roster stop matching the deleted participant?

Do not upload unredacted Logcat captures, photos, embeddings, profile names, descriptions, or access tokens to GitHub.

## 3. Latency: what is measured versus what is not

The uploaded code does **not** instrument or aggregate end-to-end latency. Do not report numerical latency, throughput, or percentile claims without collecting measurements.

For a future measured evaluation, instrument these stages with `SystemClock.elapsedRealtimeNanos()` and aggregate locally:

1. Frame copy (PixelCopy request to callback)
2. ML Kit face detection
3. Face crop and TFLite embedding inference
4. Roster matching
5. Display API send
6. Total recognition-start to visible-name interval, measured on real hardware

Suggested output: number of samples, median/p95 milliseconds, device model, firmware version, lighting condition, enrolled roster size, and whether the measurement used glasses or an emulator. Avoid student identifiers in the measurements.

The current `delay(500)` should **not** be added to model inference time and should not be presented as a latency benchmark.

## 4. Error categories and fallback behavior

| Error or edge case | Current handling | Verification |
|---|---|---|
| No detected face | Clears candidate, sends waiting display | Manual live test |
| Unknown or low-similarity face | Returns no recognized person | Manual live test |
| Face crop too small | UI shows `Face too small` | Manual live test |
| PixelCopy fails | UI shows `Frame copy failed` after repeated failures | Manual test / induced failure |
| Recognition loop exception | UI shows error message | Inspect with Logcat; avoid PII |
| Display attach or send fails | Android `Log.e` records error | Hardware test |
| No match for 30 seconds | Stops recognition | Timed manual test |
| Name displayed for 8 seconds | Stops recognition | Timed manual test |
| Device disconnect / permission denied | SDK and UI behavior must be tested | Not fully verified |
| Voice command unavailable | Phone controls remain the demo path | Current workaround |

## 5. Recommended privacy-safe telemetry (not yet implemented)

If adding metrics later, record only event names and aggregate timings, for example:

```text
event=face_detection_completed duration_ms=<number> face_count=<number>
event=embedding_completed duration_ms=<number>
event=recognition_completed matched=<true|false> duration_ms=<number>
event=display_send_failed category=<non_sensitive_error_code>
event=session_stopped reason=<timeout|user|error>
```

Never include images, embeddings, names, student IDs, descriptions, voice transcripts, raw similarity vectors, credentials, or unrestricted exception payloads. Use a random per-session identifier if correlation is necessary, and keep logs short-lived and local.

## 6. Token usage and cost

The inspected CameraAccess application performs **local face embedding inference**, not LLM inference. Therefore there are no LLM input/output tokens or provider API charges to report for this code path. Local compute still consumes phone battery and processing resources.

If the team later integrates a real flashcard-generation LLM, document:
- Provider/model name and model version
- Request count, input/output token counts from actual provider responses
- Per-model pricing source and calculation date
- Estimated cost = input tokens × input rate + output tokens × output rate
- Latency, timeout, retries, rate-limit responses and safe fallback
- Sanitization of student information before prompts are sent externally

**Do not invent token counts, dollar costs, or LLM features that are not integrated.**

## 7. Demo evidence checklist

- Capture a build/test command and its actual result.
- Record real-device recognition success and unknown-person behavior.
- Verify local roster deletion.
- Show a sanitized Logcat snippet for a display or model event.
- Report measured timings only if instrumented and collected.
- Record any limitations explicitly (voice invocation, provisional threshold, no remote backend, no verified LLM in this module).
