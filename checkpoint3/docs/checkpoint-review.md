# Checkpoint review and demo handoff

| Checkpoint | Work reviewed | What carries forward |
|---|---|---|
| 1 | The proposal, bibliography, role table and individual reflections describe consented recognition, approved context and reviewed conversation summaries. | Keep recognition and follow-up as separate consent decisions. Explain the actual phone/laptop architecture during the demo. |
| 2 | Aman’s classroom design and interview framing set the enrollment and correction flows. Steven’s prototype and gap analysis describe phone recognition, uncertainty and HUD constraints. Neha’s theory lens and validation distinguish retrieval from the professor’s judgment. Min’s prompt comparisons and interviews identify invented deadlines and review fatigue. | Offer a follow-up only on request. Require a source quote, allow edits and discard, and keep the professor responsible for confirming identity. CP2 design thresholds and timing goals are proposals, not measured CP3 results. |
| 3 | Steven’s merged sample contribution and the standalone CameraAccess implementation/documentation uploaded by Aman include local roster, capture, TFLite matching and lens display code. The standalone project is the documented build target. | Min’s speech action uses its existing roster and recognition card. Both the original description and approved follow-up remain under the profile’s deletion lifecycle. |

[CP1 proposal](../../Checkpoint%201/proposal/PROPOSAL.md) · [CP2 design](../../Checkpoint%202/DESIGN_SPEC.md) · [CP2 validation](../../Checkpoint%202/validation/) · [Steven’s merged contribution](https://github.com/lunana-7/is492-llm-wearable-project/pull/25)

## Remaining team checks

- **Aman and Steven** — On compatible glasses, run enrolled and unknown participants under more than one lighting condition. Verify that an uncertain or changed candidate clears the old card, and test disconnect/reconnect. Track false matches and elapsed time. The 0.60 threshold needs calibration.
- **Min** — In the live demo, ask a consenting speaker for a follow-up, show the editable draft, discard once, approve once, then remove it. Run the retry sequence in the speech guide. Record the phone, microphone and glasses used and observed results.
- **Neha** — Use the versioned speech prompt in the walkthrough. Describe its extractive behavior and remaining ASR errors. The presentation and use-case assignments still need the team’s finalized scripts.
- **Team** — CP2’s learning-mode fade, field-level sharing, quiet/on-demand variants, term expiry and authenticated student self-service need a demonstrated implementation or an explicit limitations slide. Keep participant interviews and simulated prompting exercises distinct when discussing evidence.

See [speech setup and verification](../app/speech/README.md) and [safety and privacy](safety_privacy.md).

## Verification on November 5, 2026

| Check | Observed result |
|---|---|
| Debug application and instrumentation APK | Both built with JDK 17, Android SDK 36 and the project Gradle wrapper. |
| Service and input tests | Four unit tests and three HTTP integration tests passed. Covered unsupported output, explicit instruction override, contact details, invalid audio, consent, browser origin, busy service, timeout and retry. |
| Live audio → Whisper → Qwen smoke | The synthetic audio yielded “I will bring the revised water quality chart to office hours.” Both models ran locally. |
| Android 15 emulator | Three instrumented tests passed, including a Compose dialog test that discarded one generated draft, edited a second and approved it. The USB reverse connection, service, models and roster encryption were real. The UI test supplied a synthetic clip at the microphone boundary. |
| Physical rehearsal | Still needed for real microphone quality, glasses registration/display, recognition accuracy and full presentation timing. |

[Min’s slide 4 and 6 cues](presentation/min-demo.md)
