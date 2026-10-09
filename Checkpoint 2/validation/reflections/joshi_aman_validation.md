# Testing Notes, Interview Insights & Personal Reflection — Aman Joshi

## 1. Testing Notes (Validation Approach)

My validation work for Checkpoint 2 ran through interviews rather than prompting (Min covered the systematic prompting study). I conducted 2 speed-dating interviews, then converted the findings into the team's opportunity framing and design spec:

- **Interviews:** 2 students (30-person and 40–60-person class contexts), 15 minutes each, using the team's storyboard frames.
- **Opportunity framing:** Wrote `OPPORTUNITY_FRAMING.md` — 9 assumption shifts (A1–A9) with interview evidence, an 8-item ranked feature list, and the opportunity statement. Cells marked `[FILL]` are where I need teammates' data or test evidence.
- **Design spec:** Wrote `DESIGN_SPEC.md` (draft) — personas (Dr. Rivera, Priya, Marcus, Sam), the recognition and enrollment task flows, and the three HUD wireframe states (high confidence, medium "verify", not enrolled).

## 2. Interview Insights

### Interview 1 — Sneha, international student, ~30-person classes

- **Context:** Only one professor knows her by name; others know her by face. Name often mispronounced; does not use pronouns.
- **Key quotes:**
  - "would be cool but I would want to be able to interact with the prof so it shows they're putting in effort to learn my name"
  - "if the prof isn't able to still pronounce my name after telling them, then the glasses can be used to teach them how to pronounce it"
  - "Want complete guarantee that sharing such information won't be used against me in any way and if I were to opt out also, it doesn't go against me"
- **What surprised me:** She liked the idea ("would be cool") but would still not opt in. Attitude and action split — which means adoption depends on trust mechanics, not just appeal.
- **Design impact:** This interview is why the opportunity framing pitches "being known, not being identified" and why the spec requires a no-penalty opt-out the professor cannot see.

### Interview 2 — Chantrice, student leader, 40–60-person classes

- **Context:** Professors usually know her name because of leadership roles. Name often mispronounced; she corrects people and doesn't mind.
- **Key quotes:**
  - "if they knew my name, I would be more compelled to ask questions even through informal email because I feel that they would respond with care"
  - "if we become overly dependent on this assistance, it might make our functional memory not as good"
  - "I would be worried if I did not attend class and the tech can verify that"
- **What surprised me:** She is open to opting in ("whynot!") and even sees attendance accuracy as a benefit — the opposite of Interview 1 on almost every axis. Same concept, two students, two verdicts.
- **Design impact:** Her over-reliance worry shaped the Learning Mode requirement (card fades as the professor learns). Her attendance-verification worry is why the spec documents "no attendance or grades" as an explicit guardrail, not just an omission.

## 3. Personal Reflection

- **The two interviews disagreed with each other, and that is the finding.** Interview 1 will not opt in without an ironclad guarantee; Interview 2 opts in eagerly and wants richer data. A consent design that only serves one of them fails. That is why the feature ranking puts student-controlled opt-in/opt-out/deletion first and why the enrollment flow keeps every field toggleable.
- **Assumption shift I owned:** I started CP2 thinking the value was recognition itself. Both interviews reframed it: the value is the feeling of being known, and the professor's visible effort is part of the product. A silent lookup that replaces effort is worse than no tool. This is documented as A2 in the opportunity framing.
- **What I would test next:** My evidence is student-only (2 interviews, both acquaintances — politeness bias possible). The professor perspective is the biggest gap: do professors actually want cards, or would they find them distracting? That is CP3 work, along with calibrating the confidence thresholds the design spec proposes but does not validate.
- **Open questions I could not close:** FERPA implications of professor-accessible student profiles; who exactly can see the access log; whether "bias toward opted-in students" (one ambiguous answer) means anything we should design for.

---
*Drafted from interview notes (aman_interview_1.md, aman_interview_2.md), OPPORTUNITY_FRAMING.md, and DESIGN_SPEC.md. Aman: please review and edit before submission.*
