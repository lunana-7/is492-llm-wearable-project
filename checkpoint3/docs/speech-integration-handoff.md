# Speech integration handoff

**Min’s implemented module — app/speech/.** The service and terminal client can be run and tested using the module README. The following changes require the owners of the Android application and shared setup documents.

## Steven · Android recording and review UI

Relevant files are under `app/CameraAccess/app/src/main/java/com/meta/wearable/dat/externalsampleapps/cameraaccess/`.

| Location | Required change | Acceptance check |
|---|---|---|
| ui/RosterDialog.kt or a new review screen | Select one stable student profile and present recording consent, recording state, transcript editing, summary editing, approve and discard | Discard closes the review without changing saved profile text |
| New audio/client component | Record mono PCM16 WAV at 16 kHz, stop at the duration limit, release the microphone on cancellation/backgrounding, call /transcribe then /summarize after transcript review | Revoked OS permission and user cancellation stop recording cleanly |
| Android network configuration | For a supervised USB demo, use adb reverse tcp:8765 tcp:8765 and a debug-only loopback HTTP allowance | Release builds avoid broad cleartext access |
| Local API token provisioning | Transfer the laptop token through a deliberate debug setup flow; retain it privately and exclude it from logs/source | Missing/invalid token yields a clear failure; never hard-code credentials |
| Review request state | Associate each result with the selected profile and a current request generation | Responses from cancelled/older requests never overwrite a new draft |
| UI error handling | Map 403/413/415/422/429/502/503/504 to retry or cancel | Outage preserves previously approved text; retry does not save automatically |
| ui/LiveRecognizer.kt and ui/DisplayHelper.kt | Retrieve approved context only after current identity/consent checks and apply a short display limit | Wrong/unknown identity never reveals a pending draft |

The service returns a draft quote, and the app must own student approval. An exported JSON file or the consent header alone does not authenticate the approving student.

## Aman · Profile identity, storage and deletion

| Location | Required change | Acceptance check |
|---|---|---|
| ui/RosterStore.kt and roster serialization | Add a stable student ID, a reviewed-summary field, and consent/approval state with backward-compatible migration | Existing entries load safely; two people with the same name remain separate |
| Approved save operation | Verify selected entry still exists and consent remains active before updating the same entry | A profile deleted while inference runs rejects the late result |
| Delete and clear-all | Remove summaries together with the profile, embeddings and any app caches | Subsequent retrieval and recognition cannot use deleted context |
| Persistence | Reuse encrypted storage and report write failures; retain the old record until the new write succeeds | Failed save has a recoverable error and preserves consistency |
| Retention | Enforce the agreed term-end deletion policy | Expired entries and summaries are unavailable after restart |
| INSTALL.md and .env.example | Add exact speech setup, USB/token configuration and smoke-test steps after app integration | A teammate completes a clean setup from the instructions |

## Min · Integration verification

After the owners wire the app to the module, run a real-device sequence with a consenting volunteer. Select the correct profile, record speech, correct the transcript, review the summary, discard once, approve once, restart the app and retrieve it, then delete the profile and repeat recognition. Add outage, busy, revoked-consent and delayed-response cases. Record the app commit, devices and actual outcomes.

The current automated speech tests exercise the service, models and terminal approval workflow. The existing Android tests cover the current roster/model methods. Full app-to-speech-to-roster verification becomes possible after the changes above.
