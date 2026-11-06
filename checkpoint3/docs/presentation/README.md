# Checkpoint 3 presentation

**Owner — Neha Manishankar.**

Open [the seven-slide deck](contextlens-cp3.pptx). Speaker notes contain timing, sources and demonstration cues. The deck uses the current phone-based recognition implementation and labels proposed prompt integration and CP4 evaluation.

| Slide | Presenter | Time |
|---|---|---|
| 1 · ContextLens and team | Neha | 0:30 |
| 2 · Architecture | Aman | 0:45 |
| 3 · Live enrollment and recognition | Steven | 2:15 |
| 4 · Live edge cases and recovery | To be assigned | 1:45 |
| 5 · Technical choices and prompts | Aman + Neha | 0:45 |
| 6 · Safety | Min | 0:45 |
| 7 · CP4 benchmark proposal | Neha | 0:45 |

Total 7:30, with 4:00 in the running application. Use [the walkthroughs](../use-cases.md) for the exact controls and expected outcomes.

## Rehearsal and submission

1. Pin the demo commit. Build on the presenter’s machine using INSTALL.md and verify required device credentials.
2. Prepare consenting volunteers and distinct synthetic roster entries. Test camera framing and screen sharing.
3. Run UC-01 through UC-05 on actual hardware. Record failures as well as successes. Choose edge cases that fit the 1:45 slot.
4. Time the complete talk, including app switching. Verify four minutes remain live. Show actual outcomes if the system fails and use the documented recovery controls.
5. Run the prompt fixtures separately. An LLM evaluation and a working Android recognition demo provide different evidence. The rubric’s integrated LLM/Agent requirement still needs the team’s implementation decision.
6. Replace statements about unverified hardware behavior with measured rehearsal results before presenting.
7. Submit the repo link and requested summary through the course assignment. The supplied page lists Thursday 11:30 PM for the assignment and Friday 9:00 AM for the forum. Confirm the course dates and timezone.
8. Confirm receipt in both required destinations. Submission remains a team action.

## Proposed CP4 evaluation

Propose Track B to the team. Establish a fixed set of consented enrolled/unknown trials. Separate threshold-calibration trials from held-out trials. Vary lighting and pose, include an empty roster, and report false-match rate, missed-match rate and median/p95 end-to-end latency with denominators and device details. For prompt evaluation, measure approved-field groundedness, abstention and privacy failures. Set sample sizes and acceptance thresholds before collecting evaluation results.

## Suggested forum text

“ContextLens helps professors recall consenting students’ preferred names and approved context. Our repository contains the Android recognition implementation, setup instructions, architecture and logging documentation, and a versioned prompt evaluation package. Our demonstration covers enrollment, recognition, unknown-person handling, deletion and recovery. The slides identify implementation gaps and propose a CP4 benchmark.”

Add the verified demo commit and actual rehearsal outcomes before posting. Repository link:
https://github.com/lunana-7/is492-llm-wearable-project/tree/main/checkpoint3
