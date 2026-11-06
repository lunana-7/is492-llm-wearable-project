# Checkpoint 3 work assignments

Assignments use the original team roles and CP2 contributions, with Min and Neha’s workstreams swapped at Min’s request. This file assigns work; it does not claim that work is done or send notifications to team members.

| Person | Primary ownership | Required handoff / definition of done |
|---|---|---|
| **Aman Joshi** | `app/backend/`, `app/database/`, `app/scripts/`, `app/INSTALL.md`, `app/.env.example`, architecture and observability docs | Working recognition/profile/session APIs and database; consent enforcement, approved-field retrieval, correction/deletion and retention; measured latency/token/cost/error telemetry; clean-machine setup; backend unit tests. Agree request/response contracts with Steven and Min before integration. |
| **Steven Wang** | `app/frontend/`, `app/wearables/` | Real capture-to-backend-to-display flow; enrollment/profile editing/deletion; student field toggles and data-access view; high/medium/low-confidence cards; accept/reject/dismiss, session activation, quiet/on-demand controls and learning mode. Handle connection/loading/error states and test UI transitions. Neha reviews UX. |
| **Min Kim** | `app/speech/`, `tests/`, `docs/safety_privacy.md` | Real consented transcription and LLM summary pipeline; student review/edit/approve before persistence. Own integration suite and safety regression coverage; each developer supplies component tests. Report actual results and limitations. |
| **Neha Manishankar** | `app/prompts/`, `docs/use-cases.md`, `docs/presentation/`; product/UX coordination | Versioned grounded prompts, examples, parameters and output schemas, with Min integrating actual inference. Missing-field, unsupported-claim and injection regression cases. Primary-flow demo script, seven-slide presentation, rehearsal and forum submission; support Steven's UI design. |

## Scope from Checkpoint 2

Use the classroom ContextLens design, not the earlier broad customer-service concept. Core flow: voluntary enrollment → active session → match enrolled profiles → retrieve student-approved fields → show a minimal card → professor confirms/corrects/dismisses. Include profile maintenance/deletion, optional field sharing, learning mode, quiet/on-demand controls, transparency and retention. Min and Neha own the consented summary/approval workflow supported by the prior proposal and CP2 reflections. Do not introduce live AI answers, attendance or grading features.

CP2 documents disagree on HUD density (under ten words versus richer cards) and latency targets (1.2 versus 2 seconds). Neha and Steven must settle the compact-card design; Aman measures actual latency and records the agreed target in architecture.md. These are decisions to resolve, not verified performance claims.

## Handoff order

1. **Contract and scope:** Aman defines APIs/data fields; Steven defines UI/device states; Neha and Min agree model inputs, schemas, consent and summary review states.
2. **Components:** Everyone implements their owned folders and relevant tests. Aman verifies setup; Neha supplies prompt versions before Min integrates inference.
3. **Integration:** Steven + Aman connect capture, recognition and cards; Min + Neha connect real model calls and reviewed summaries. Min runs critical paths; owners fix failures.
4. **Rehearsal and submission:** Neha coordinates a clean-machine run, full demo rehearsal and forum post; everyone verifies their assigned docs reflect running code.

## Presentation ownership — 7.5 minutes

| Segment | Presenter | Time |
|---|---|---|
| Slide 1: title, team, repo, problem | Neha | 0:30 |
| Slide 2: architecture and stack | Aman | 0:45 |
| Slide 3 + live primary flow | Steven | 2:15 |
| Slide 4 + live edge cases and recovery | To be assigned | 1:45 |
| Slide 5: technical choices and prompts | Aman + Neha | 0:45 |
| Slide 6: safety and guardrails | Min | 0:45 |
| Slide 7: limitations and CP4 evaluation | Neha | 0:45 |

Four minutes are live software operation, exceeding half the presentation. Run real inference; do not substitute static screens or recorded outputs. Demonstrate consented enrollment/recognition, approved context and correction, then uncertainty, deletion and at least one recoverable error. Prepare a tested live fallback and explain any hardware limitations.

## Submission checklist

- [ ] All CP2 core features traced to implementation and tests (Neha coordinates).
- [ ] Working end-to-end application and real LLM inference (all).
- [ ] Reproducible INSTALL, environment template, dependency manifests and run commands (Aman; Steven verifies).
- [ ] Versioned prompts/model parameters/output schemas (Neha + Min).
- [ ] Architecture/dataflow and observability reflect actual implementation (Aman).
- [ ] Use-case walkthroughs and tested safety/privacy safeguards (Neha + Min).
- [ ] Passing unit and critical-path integration tests (Min coordinates).
- [ ] 5–8 minute presentation with at least half spent live (all; Neha coordinates).
- [ ] CP4 evaluation track and known limitations documented (Neha + Min).
- [ ] Forum submission before **Week 10 Friday, 9:00 AM** (Neha). Confirm the calendar date and course timezone; the supplied instructions do not specify them.

## Sources

- [Checkpoint 1 team roles](https://github.com/lunana-7/is492-llm-wearable-project/blob/main/Checkpoint%201/README.md)
- [Checkpoint 2 design](https://github.com/lunana-7/is492-llm-wearable-project/blob/main/Checkpoint%202/DESIGN_SPEC.md)
- CP2 validation reflections, prompting protocol and gap analysis in the original repo.
- Checkpoint 3 requirements provided by the user.
