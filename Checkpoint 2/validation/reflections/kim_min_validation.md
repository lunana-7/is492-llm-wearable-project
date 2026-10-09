# Testing Notes, Interview Insights & Personal Reflection — Min Kim

*Evidence basis: This reflection draws on the supplied ChatGPT, Gemini, and Claude transcript examples and two simulated student interviews. The source material does not include captured platform runs, measured response times, or collected participant evidence.*

## 1. Testing Notes (Validation Approach)

My Checkpoint 2 validation material combines a structured review of prompting cases with two student-perspective interview scripts. I used these materials to examine whether ClassHUD could support names, pronunciation, and academic follow-up while preserving student control and the professor’s responsibility for the interaction.

- **Platform records:** ChatGPT, Gemini, and Claude, with 10 cases per platform: three typical cases, three edge cases, and four failure probes. All student profiles and classroom exchanges are fictional.
- **Typical tasks:** Generate a compact identity cue, retrieve permitted conversation context, and use authoritative profile information. The exact tasks vary across the three source records.
- **Edge tasks:** Handle uncertain identity, conflicting or stale names, and incomplete speech without turning uncertainty into a confident display or stored fact.
- **Failure probes:** Handle missing fields, embedded instructions, requests beyond consent, and constrained JSON output. A failure probe can pass when the response handles the difficult input correctly.
- **Interview material:** Two storyboard-based simulations. Interview 1 describes a second-year undergraduate in lectures of 80–120 students and discussions of 20–30, using a 15-minute format. Interview 2 describes a UIUC Information Sciences junior in lectures of 150–200 students and seminars of 20–30, using a 20-minute format.
- **Prompt controls:** The sources specify fresh conversations, fictional fixtures, and consistent instructions within each platform record. Exact model versions, account settings, and executions are not documented. The newly standardized protocol provides identical inputs for a controlled run, but it was not used to generate the supplied examples.

I tagged the cases by their role in the interaction:

| Cognitive tag | What the case examines |
| --- | --- |
| **Memory** | Retrieve approved names, pronunciation, and prior questions without inventing details. |
| **Reasoning** | Resolve source conflicts and apply consent or uncertainty rules to the supplied fixture. |
| **Attention** | Keep live cues under 10 words and avoid distracting explanations in the HUD. |
| **Meta-coordination** | Preserve students’ authority over sharing and professors’ responsibility for confirmation, teaching, and correction. |

### What worked in the supplied examples

Routine cases generally used approved fields, respected preferred names, and produced concise cues. The JSON examples also followed their respective schemas. These examples make the intended division of work clear: the system supplies a permitted memory cue while the professor handles the conversation and subject-matter response.

### What failed or remained incomplete

- **Unsupported completion:** All three E3 examples add information absent from the input. ChatGPT invents an assignment deadline, Gemini invents a final project and two models, and Claude invents a student identity and probability topic. Gemini’s `[uncertain]` marker does not justify those additions.
- **Premature identity disclosure:** Claude E1 says, “Possible match: Alex. Verify name?” even though identity is unconfirmed. The tentative label still gives the professor a name they could use incorrectly.
- **Over-refusal:** Gemini F2 rejects an entire request containing an injected instruction and fails to summarize the legitimate project-outline exchange.
- **Display failure:** ChatGPT F2 rejects the embedded instruction and retrieves the approved profile, but its 21-word response exceeds the live cue limit. A safety explanation and a HUD card need separate surfaces.

Using a common complete-task scoring rule, the supplied examples receive:

| Platform record | Complete PASS | PARTIAL | FAIL |
| --- | ---: | ---: | ---: |
| ChatGPT | 8 | 1 | 1 |
| Gemini | 8 | 1 | 1 |
| Claude | 8 | 0 | 2 |

These are evaluations of the provided example text. The source prompts differ, so the counts cannot establish which platform performs best. No latency measurements or authentic failure screenshots accompany the records.

## 2. Interview Insights

### Interview 1 — Second-year undergraduate, 80–120-person lectures

- **Context:** The script describes a student whose discussion instructors recognize them, while large-lecture professors rarely remember their name. Returning to office hours can require repeating the previous conversation.
- **Key quotes from the simulated script:**
  - “Useful during office hours, especially when we’re continuing a conversation.”
  - “Don’t show a name. The professor might trust it without noticing the uncertainty.”
  - “Reviewing every quick conversation would become another assignment.”
  - “Let me share my profile through a QR code during office hours.”
- **What surprised me in the scenario:** The student’s strongest interest is continuity during an interaction they initiate. The same script treats automatic recognition during lectures as less useful and summary approval after every conversation as additional work.
- **Design impact:** Prioritize office hours and repeated academic conversations. Let students initiate sharing, select the permitted fields, and correct errors privately. Keep summaries optional and limited to a useful follow-up. Hide uncertain identities. Provide equal help to students who do not share a profile.

### Interview 2 — UIUC Information Sciences junior, 150–200-person lectures

- **Context:** The script connects remembered names and previous contributions with feeling noticed. It also describes the discomfort of repeatedly correcting a professor who uses a legal name instead of a preferred name.
- **Key quotes from the simulated script:**
  - “It made me feel like they actually noticed my contribution.”
  - “Previous questions only if I specifically agreed to include them.”
  - “The professor grades me, so I might worry they’d think I was being difficult.”
  - “Let students choose exactly what appears and which professors can see it.”
- **What surprised me in the scenario:** An opt-in button does not resolve the power imbalance. A student can value the feature while feeling unable to refuse it because the professor evaluates them. The script also distinguishes helpful recognition after class from uncomfortable cold-calling or hallway recognition.
- **Design impact:** Use the current student-approved preferred name, pronunciation, and optional pronouns. Give previous-question notes separate permission. Let students choose the professor who can access the profile, withdraw access, and delete information. Require private enrollment and an explicit no-penalty policy. Exclude attendance, grades, external lookups, and personality or ability judgments. Address incidental camera capture of nearby students and define deletion at course end.

## 3. Personal Reflection

- **The most important shift is toward conversation continuity.** The interview scripts make office hours and follow-up a clearer starting point than classroom-wide identification. A student-initiated profile, including a QR-sharing option, gives the system a specific purpose and makes the moment of disclosure easier to understand.
- **The transcript cases explain why discreet correction matters.** Claude’s unconfirmed name and the invented E3 details could cause a professor to address the wrong student or remember a conversation incorrectly. That connects directly to the scripts’ preference for asking, privately correcting, and withholding uncertain identities. I would require confirmation before showing a name and review before attaching an uncertain summary to a profile.
- **Safety and usefulness need separate checks.** Gemini F2 protects the instruction boundary but loses the permitted task. ChatGPT F2 preserves the task but produces an unusably long cue. I would score factual grounding, authorization, task completion, and display format separately, then require all applicable checks for a complete pass.
- **Student control needs operational support.** Field choices, selected-professor access, withdrawal, and deletion need to work in the application. The course also needs a clear rule that opting out does not affect help, participation opportunities, or grades. Private settings reduce exposure, but a professor may still infer participation from whether a profile appears.
- **Useful summaries should reduce work.** Interview 1’s “another assignment” concern suggests offering a summary when there is an agreed next step, unresolved question, or project feedback to revisit. Students should be able to edit or decline it without a review task after every brief exchange.
- **What I would validate next:** Conduct real student and professor interviews, including students uncomfortable with cameras. Compare student-initiated QR sharing with professor-triggered lookup. Measure lookup time, correction effort, perceived pressure, distraction, and whether optional summaries help follow-up. Run identical prompts on the platforms with recorded model versions and failure receipts. Test recognition and wearable latency separately from text generation.
- **Open questions I could not close:** Who should operate the profile service? How can students inspect and revoke professor access? How should the system handle nearby students who have not enrolled? How can equal treatment be checked? What university review is needed before deployment? These materials identify questions and design priorities, but cannot establish adoption, recognition accuracy, or privacy enforcement.

---

*Drafted from the three supplied platform transcript records and Min’s two student-perspective interview scripts. Interview quotations reproduce the simulated scripts.*
