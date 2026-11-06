# Safety and Privacy

**Owner — Min Kim. Aman implements storage and recognition controls. Neha reviews wording.**

This review covers CameraAccess, the prompt evaluation package, and Min’s local speech module. It distinguishes source-inspected behavior, automated checks and safeguards still requiring implementation. Test execution details belong in [the verification record](../tests/integration/RESULTS.md).

## Data and access

The local roster contains a name, description and one or more face embeddings. RosterStore encrypts the serialized roster with Android Keystore AES-GCM before writing it to SharedPreferences. Android backup is disabled. Roster deletion removes the named entry and its embeddings, and Delete all empties the roster. The current interface makes these controls available to the person operating the phone.

Recognition frames are used for face detection and embedding inference on the phone. The roster stores embeddings rather than captured image files. The separate photo-share and video-recording paths can retain or export media, so a claim that every captured frame is immediately erased would be inaccurate. CapturePreviewScreen writes shared photos to the cache, while CameraViewModel attempts deletion of a temporary video when its preview is dismissed. External shared copies require separate deletion.

The name and description can appear on the phone and glasses. Avoid sensitive details in demo descriptions and avoid sharing identifying screenshots or unredacted logs.

## Safeguards and evidence

| Area | Current implementation | Verification and remaining work |
|---|---|---|
| Consent | Enrollment shows a reminder to enroll people who agreed. | A recorded consent flag and an enforced consent gate are still required. Obtain consent before the demonstration. The existing enroll method accepts no consent argument. |
| Field permissions | A profile contains name and description, with all matched description text eligible for display. | Student-selected field permissions and authenticated profile editing remain open. The prompt fixture's approved_fields policy is separate from application access control. |
| Access controls | App-private storage, Keystore encryption and Android permission requests limit access. | Student/professor role checks and per-student authentication remain open. Phone access grants access to the roster UI. |
| Withdrawal | Individual delete and Delete all update the encrypted roster. | Automated tests verify deletion and matching after reloading the roster object. Already shared media and previously displayed text need separate checks. |
| Term-end retention | Manual deletion is available. | Scheduled term expiry is still required. Clear demo profiles after the session and verify the roster is empty. |
| Ephemeral frame handling | Live recognition processes sampled bitmaps and keeps embeddings in memory. | The app has capture/share/recording features. Audit cache lifetime, recording dismissal and exports on a device before claiming full ephemeral handling. |
| Session indicators | The phone exposes session/stream state and start/stop controls. | Test visible phone and lens behavior during start, timeout, stop and device loss. |
| PII minimization | Local processing avoids a separate face-recognition server. | Names and embeddings are identifying data. Student descriptions are free text, with no implemented PII sanitizer. Use synthetic names and minimal approved descriptions in tests. |
| Prompt injection | Neha's system prompt treats profile content as untrusted, with schema and regression fixtures. | Four contract tests and a separate live evaluation exercise this package. The Android display path currently bypasses an LLM, so these checks do not enforce field restrictions in the app. |
| Schema validation | The prompt package has a JSON output schema and executable evaluator. | Integrate validation at any future model-call boundary. Roster loading uses org.json and needs additional corrupt-record handling. |
| Low-confidence suppression | RosterStore returns no match below 0.60 similarity. LiveRecognizer waits for three consecutive matches. | Boundary and unknown-vector tests cover matching. The score is provisional. The photo preview has a separate single-match path. False matches and stale cards require device trials. |
| Rate limits and fallback | The live loop waits about 500 ms. Recognition has a 30-second no-match timeout and an eight-second shown-name timeout. | These are local scheduling/session controls. A future inference service needs explicit rate-limit, timeout and retry handling. Existing display exceptions are logged; test recovery on hardware. |
| Sensitive use restrictions | Current roster code has name, description and embeddings; it has no attendance or grade connector. | Free-text descriptions can still contain prohibited information. Keep attendance, grades and inferred personal attributes out of profiles. The recognition path sends text to the display; automatic spoken names are outside its implemented behavior. |

## Known failure paths to verify

1. **Wrong or stale identity.** CapturePreviewScreen reads the shared lastEmbedding value. A failed capture can leave an earlier embedding available. It also selects the first detected face. Reproduce with a valid photo followed by an empty or multi-person photo, and block unsafe enrollment before real use.
2. **Same-name profiles.** Enrollment merges samples by case-insensitive name. Two different people using the same name can share an entry. Distinct identifiers and explicit ownership are needed.
3. **Stale lens card.** The live loop can retain a prior candidate streak or display during crop/frame failures. Stop recognition if an identity is wrong and verify the lens clears. A fresh successful match alone does not prove the error path is safe.
4. **Legacy or corrupt storage.** RosterStore attempts to interpret the stored string as plaintext JSON if decryption fails. The encryption test checks ciphertext authentication directly. It does not establish that the whole loading path rejects every malformed or legacy record.
5. **Approval and speech.** The local speech module implements consent, transcript correction, draft review and explicit approval-only export. Android roster integration still requires the [owner handoff](speech-integration-handoff.md). The terminal’s typed student ID and exported approval fields express supervised demo approval rather than authenticated student identity.

These findings are implementation handoffs to the relevant owners. [Manual checks](../tests/integration/README.md#manual-checks) specify the expected safety behavior and how to record a failure.

## Demonstration procedure

Use consenting volunteers and synthetic roster entries. Explain what is captured, where it is stored, who can see it and how deletion works before capture. Confirm the selected profile on the phone. Stop immediately if a wrong identity appears. Demonstrate deletion with a fresh recognition attempt, then clear all demo profiles. Share only aggregate outcomes and synthetic trial identifiers.

## Limits of the evidence

Synthetic vectors exercise matching and deletion mechanics. A synthetic bitmap exercises the bundled model's execution path. Neither establishes face-recognition accuracy or fairness. Real-device testing must cover lighting, pose, glasses/masks, unfamiliar participants, disconnects and visible lens state. Record measured outcomes rather than treating source code, fixtures or a planned test as proof of behavior.

## Implemented speech-module safeguards

The [speech module](../app/speech/README.md) uses local Whisper and Qwen. Each microphone session starts with explicit operator-confirmed consent. The client corrects the transcript before summarization, then edits or discards the draft. Approving requires typing the selected pseudonymous student ID.

The API binds to loopback and requires a locally generated owner-only bearer token. It rejects browser-origin requests, missing consent, oversized/invalid audio and malformed request bodies. It serializes inference and admits at most twelve requests per minute. Failure responses offer controlled retry or cancellation. Authentication is for the local client, with application-level student authentication still required for deployment.

Email and digit-based phone patterns are redacted before model input. The prompt requests a short verbatim academic follow-up, the response is schema-validated, and unsupported or contact-bearing quotes are rejected. A common explicit instruction-override pattern triggers abstention. Human review remains necessary for ASR errors, names, spoken numbers, context and sensitive details.

Audio, transcript and unapproved drafts remain in memory. Changing a transcript invalidates its previous draft. Approval publishes a new owner-only JSON file atomically, preserving existing files. The export stores the selected student ID, model quote, edited summary and approval metadata, with no raw audio or transcript. The plaintext file requires deletion after the demonstration. The CLI supports deletion with student-ID confirmation.

The ten workflow tests and six HTTP tests cover these controls and recovery paths. The opt-in live smoke sends the synthetic recording through both actual models, edits and saves the note, verifies its content and deletes it. Refer to [RESULTS.md](../tests/integration/RESULTS.md) for the current run and its scope. Physical microphone capture, Android UI approval and glasses display remain rehearsal/integration checks.
