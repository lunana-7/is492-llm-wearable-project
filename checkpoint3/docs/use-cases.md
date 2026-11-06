# ContextLens use-case walkthroughs

**Owner — Neha Manishankar. Test coordination — Min Kim.**

These scripts target `app/CameraAccess/`. Source review establishes available controls. Each device result below still needs a rehearsal entry with device, firmware, date and actual outcome. Use distinct synthetic names and consenting volunteers.

## UC-01 · Enroll and recognize

**Preconditions.** Complete INSTALL.md, connect compatible glasses, and obtain the volunteer’s consent. Start with an empty demo roster.

1. Start the device session and preview. Capture a clear photo containing one volunteer.
2. Enter a synthetic preferred name and an approved short description. Select **Enroll this face**.
3. Open **Roster**. Confirm the entry and description.
4. Select **Start recognition** and show the enrolled participant.
5. Check the phone status and glasses. The live recognition loop requires three consecutive matches above the provisional 0.60 threshold.
6. Select **Stop recognition** and verify the device session ends.

**Expected from source.** Local face detection, embedding inference, roster comparison and display calls execute. An actual lens result and timing must be observed on hardware. The enrollment screen currently contains a consent reminder, so the facilitator obtains consent before the capture.

**Evidence.** CapturePreviewScreen.kt, RosterStore.kt, LiveRecognizer.kt and CameraScreen.kt. Record observed match/no-match and elapsed time, without storing identifying media.

## UC-02 · Unknown participant and timeout

1. Stop the preceding session. Start a fresh recognition session.
2. Show a consenting volunteer who has no entry in the demo roster.
3. Confirm that no enrolled identity appears. Wait through the 30-second no-match timeout.
4. Verify recognition stops, then restart with the enrolled volunteer.

**Expected from source.** Below-threshold matching returns no person. A fresh session with no accepted match times out after 30 seconds. A false match is a failed trial and must be reported.

## UC-03 · Withdraw and delete

1. Ask the enrolled volunteer whether they want the demo profile removed.
2. Open **Roster** and select the delete icon for their entry.
3. Verify the entry disappears. Start a fresh recognition session and show that volunteer again.
4. Confirm their former card does not appear. End the session.
5. After rehearsal, use **Delete all** to remove the remaining demo entries.

**Expected from source.** The named roster entry and its embeddings are removed from local storage. Deleting one entry and clearing the roster use different paths and should both be checked. Approved-summary deletion is pending a summary integration.

## UC-04 · Wrong match and recovery

1. If a wrong identity appears during a consented test, select **Stop recognition** immediately.
2. Record a false-match event using a synthetic trial ID.
3. Inspect the roster, remove the incorrect enrollment, and enroll the intended participant again with consent.
4. Restart recognition and repeat the trial.

The current recovery controls are stop, roster deletion and re-enrollment. Dedicated accept/reject/correct buttons remain a CP2 design requirement for Steven’s implementation work.

## UC-05 · Device interruption

1. Begin preview with the demo volunteer.
2. End the session or disconnect the glasses using the supported device controls.
3. Observe session status and any displayed error. Verify that new matches stop.
4. Reconnect, start a new session and retry recognition.

Record phone and lens behavior separately. Display failure handling exists in code, but stale lens content and reconnection behavior require device testing.

## UC-06 · Prompt policy evaluation

Run `python3 tests/unit/test_prompt_contract.py --live` from checkpoint3 after following the prompt README. It exercises active/revoked consent, missing fields, hidden HUD, uncertain recognition, conflicting profiles, hostile text and invented deadlines with synthetic JSON.

Expected results are versioned in `app/prompts/regression_cases.json`. This is a separate LLM evaluation. The Android application currently renders roster text directly.

## CP2 feature traceability

| Design flow | Current source or deliverable | Remaining verification or implementation |
|---|---|---|
| Enrollment, recognition, local deletion | UC-01–03 | Device rehearsal and consent enforcement |
| Stop and restart | UC-04–05 | Wrong-match correction UI and stale-display checks |
| Confidence tiers | Prompt cases and existing threshold/streak | Calibrated mapping and Android UI integration |
| Field sharing and student-controlled editing | Proposed prompt contract | Authenticated profile controls and field permissions |
| Quiet/on-demand and learning-mode fade | CP2 design and prompt hidden state | Demonstrate actual UI/state behavior |
| Speech and reviewed summary | Min’s assignment | Implement and verify in the shared application |
| Access history and term expiry | CP2 design | Access controls, audit interface and scheduled deletion |

## Rehearsal record

For each UC, record the Git commit, device/firmware, synthetic trial ID, operator, date, expected result, actual result, pass/fail and follow-up owner. Leave a test unverified until the team executes it. Keep participant names and captured faces out of the shared record.

## UX handoff to Steven

During rehearsal, check long preferred names and descriptions for clipping, readability at the actual lens size, and whether a changed or unknown face clears an earlier card. Confirm that the student can understand what will be stored before capture and can locate deletion without assistance. Record each issue with the screen/control, expected behavior and reproduction steps. The current roster shows name and description together, so field-specific sharing requires an explicit UI and storage design.
