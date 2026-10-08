# ContextLens / ClassHUD — Human–AI Complementarity Theory Lens

## 1. Working theory claim

ContextLens (called ClassHUD in the classroom validation materials) proposes wearable smart glasses that help instructors remember enrolled students' preferred names, pronunciations, and other information the students explicitly approve. **Our hypothesis is that the human–AI hybrid will outperform both an instructor working alone and an AI system operating without instructor judgment** on accurate, timely, consent-respecting name recognition during classroom interactions. AI contributes fast retrieval and compact presentation of authorized information; instructors contribute contextual judgment, teaching expertise, relationship-building, and final decisions about whether to use a suggestion.

Following the complementarity framework of Gonzalez et al. (2026), the aim is not simply to automate remembering names. It is to coordinate different strengths across **reasoning, memory, and attention** while making **meta-coordination**—who decides, verifies, and escalates—explicit. This is a claim to test, not an outcome already demonstrated.

## 2. Cognitive diagnosis and role ownership

| Cognitive pillar | AI role | Human role | Coordination rule |
| --- | --- | --- | --- |
| **Reasoning** | Retrieve and format relevant, student-approved profile fields; do not invent student facts or answer course questions on the instructor's behalf. | Interpret the classroom context, teach, answer questions, and decide whether mentioning a detail is appropriate. | The instructor owns all pedagogical and interpersonal decisions. |
| **Memory** | Match an enrolled face to a consented profile and retrieve a preferred name, pronunciation guide, or approved note. | Learn names over time, notice mismatches, and correct or disregard reminders. | Student-edited information takes precedence over imported roster defaults; do not infer missing fields. |
| **Attention** | Show a short, peripheral reminder only when useful; avoid flooding the display. | Maintain eye contact, follow the discussion, and prioritize students over the display. | The instructor can dismiss or ignore reminders at any time. |
| **Meta-coordination** | Indicate confidence/uncertainty and suppress unapproved or ambiguous matches. | Verify uncertainty, decide what to say, and fall back to asking a student directly. | No automatic attendance, grading, or participation judgments; the instructor retains final control. |

### Approval, consent, and escalation rules

1. **Before recognition:** Students must affirmatively opt in and control which fields they share, including preferred names and pronunciation guides. Nonparticipants must not receive identity cards. The proposed design discards non-enrolled frames without logging them and provides a visible recording/status indicator. Opting out must not affect treatment or grading.
2. **When recognition is uncertain:** The team's *proposed*, not yet calibrated, thresholds are high confidence (at least 80%) for an approved reminder, medium confidence (50–79%) for a discreet **“Verify name?”** cue, and low confidence (below 50%) for no identity display. These cutoffs require empirical calibration; even high confidence is not proof of identity.
3. **Before using a reminder:** The instructor retains the choice to act, ignore, or verify. If a name conflicts with what the student says, the instructor should ask rather than assert the AI's guess; the student should be able to correct the source profile.
4. **For errors or sensitive requests:** Suppress unsupported fields and escalate to a normal human conversation. Do not repurpose recognition for attendance, grading, or surveillance. Access controls, deletion at the end of the course term, and a clear consent/withdrawal process are proposed safeguards that need implementation and testing.

## 3. Evidence → theory → design connections

These are **interview receipts and design proposals**, not measured AI-platform failures. The team should add prompting transcript links if available.

| Evidence receipt | Complementarity diagnosis | Design implication / requirement |
| --- | --- | --- |
| **Interview 3:** “Getting called the wrong name is a lot more embarrassing than just asking 'What was your name again?'” | **Memory + meta-coordination:** A confident false match undermines trust when the AI's suggestion is treated as a fact rather than interrogated. | Use confidence-tiered reminders, suppress low-confidence identities, and let the instructor verify uncertain names. Test false-match and incorrect-name rates. |
| **Interview 4:** “Wouldn't the glasses call me by whats on Canvas instead of (nickname)? What if the AI hallucinates a nickname?” | **Knowledge infrastructure + memory:** Imported records can conflict with a student's own preferred identity; generative completion must not substitute for authorized data. | Make student-controlled preferred names and pronunciation fields authoritative. Only show approved, stored information; provide correction and deletion controls. |
| **Interview 3:** “Does the professor just stare at me for a few seconds and then glance down at some text? That would feel really strange I think.” **Interview 4:** “I think a delay before saying someone's name would sound super unnatural.” | **Attention orchestration:** Slow or intrusive prompts break conversational timing and draw attention away from the student. | Use brief peripheral HUD cards (team proposal: fewer than 10 words), prefetch where permitted, and measure end-to-end response time. The team's sub-1.2-second goal and sub-200-ms cached-display goal remain unverified engineering targets. |
| **Interview 1:** “would be cool but I would want to be able to interact with the prof so it shows they're putting in effort to learn my name”. **Interview 2:** “if we become overly dependent on this assistance, it might make our functional memory not as good”. | **Role partitioning + learning:** An always-present memory crutch could reduce human effort and perceived rapport rather than complement it. | Keep teaching and relationship-building with the instructor; test a **Learning Mode** that gradually reduces reminders after successful use. |
| **Interview 1:** “Want complete guarantee that sharing such information won't be used against me in any way and if I were to opt out also, it doesn't go against me”. **Interview 3:** “I would only participate if there is strict opt-in consent. Also, I would be very uncomfortable with participation tracking.” | **Goals/constraints + meta-coordination:** Recognition is not legitimate if the data are used outside the student's agreed purpose; fear of surveillance can prevent adoption. | Explicit opt-in, no-penalty opt-out, purpose-limited access, no attendance/grading integration, and a visible camera/status indicator. Test that nonconsenting profiles never appear. |
| **Interview 3:** “Continuous video processing on smart glasses would probably drain the battery, you could offload the face processing to a phone or something.” | **Resource-aware attention and knowledge infrastructure:** Assistance that drains batteries or stalls cannot support real-time teaching. | Prototype split processing between glasses and a companion phone/edge device; benchmark battery use and latency rather than assuming this architecture is superior. |

### How validation changed the concept

The team's gap analysis documents a shift toward **memory assistance rather than live AI-generated academic answers**, **student authority over displayed identity rather than automatic Canvas-name defaults**, **Learning Mode rather than permanent prompting**, and **split processing rather than continuous heavy on-glasses computation**. These changes follow the interviews, but their effectiveness still needs experimental validation. Interviews 1–4 cover different classroom sizes and preferences; they should not be treated as representative of all students.

## 4. Committed principle and Checkpoint 3 evaluation

**Committed principle: Role partitioning**, supported by attention and interrogation orchestration. AI should retrieve only consented information and flag uncertainty; instructors should verify when necessary and own teaching and interpersonal decisions. The interface must make that boundary obvious instead of encouraging uncritical reliance on a name prediction.

### Three-condition comparison

Use the **same standardized, consented classroom scenarios** in three conditions, balancing order and difficulty to reduce practice effects:

| Condition | Task procedure |
| --- | --- |
| **Human-alone** | An instructor recalls a student's preferred name/pronunciation or consults a conventional approved roster, without AI assistance. |
| **AI-alone** | The recognition/retrieval system produces its identity and reminder output without human correction; evaluate the output offline rather than allowing autonomous public identification. |
| **Hybrid** | An instructor receives ContextLens reminders, can verify uncertain matches, and decides whether and how to address the student. |

Include typical cases (enrolled student, clear view), edge cases (nickname differing from roster, side angle, low lighting), and failure cases (lookalike/uncertain match, student opted out, stale or incorrect record). Use volunteers or simulated profiles with explicit consent; do not secretly identify students.

**Measures:** (1) correct preferred-name/pronunciation use and false-name rate; (2) time from identification opportunity to an appropriate response, including delays from verification; (3) consent and privacy violations, with zero unauthorized displays as the target; (4) perceived naturalness, distraction, and trust using brief post-task ratings; and (5) practical latency and battery/compute use. Record sample size, scenario, condition, errors, and uncertainty for each trial.

**Success criterion:** The hybrid demonstrates **complementarity** only if it performs better than *both* human-alone and AI-alone on preselected primary measures (for example, correct consent-respecting name use and response time), **without worsening privacy compliance or interpersonal naturalness**. If it improves accuracy but causes unacceptable delays, distraction, or privacy violations, we should report a trade-off rather than claim complementarity. Thresholds and the Learning Mode should be adjusted using measured results, not assumed effective.

## References

- Gonzalez et al. (2026). *Toward a science of human–AI teaming for decision making: A complementarity framework.* *PNAS Nexus*, 5(3), pgag030. https://academic.oup.com/pnasnexus/article/5/3/pgag030/8490283
- Team *Gap Analysis Matrix: ClassHUD System Validation (Interviews 1–4)* (classroom refinement and proposed requirements).
