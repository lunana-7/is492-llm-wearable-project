# Opportunity Framing - ContextLens

**Owner:** Aman | **Evidence base:** 2 student interviews
(`validation/interviews/aman_interview_1.md`, `aman_interview_2.md`) plus test
transcripts (`validation/transcripts/`). `[FILL]` marks cells that still need
test evidence or a teammate's data.

## 1. Where we started vs. where we are
**Checkpoint 1:** a wearable AI agent that helps service employees recognize customers.

**Checkpoint 2:** a professor wears AR glasses that recognize students who have
**opted in**, showing a student-approved card (name, pronunciation, past
questions, optional note) so the professor can address students personally,
especially in larger classes.

## 2. Changed assumptions

| # | Assumption | What we found (evidence) | Theory | New direction |
|---|---|---|---|---|
| A1 | Students want to be recognized by name | **Supported, mainly emotionally.** Both felt "seen" or "recognized" when known; one would ask more questions. Neither reported a participation change. (Int. 1 Q2, Q4; Int. 2 Q2, Q4) | Belonging; student-faculty interaction | Pitch the value as "being known," not "being identified" |
| A2 | The value is the lookup itself | **Challenged.** Int. 1 wants to "interact with the prof so it shows they're putting in effort"; Int. 2 fears over-reliance weakening memory. (Int. 1 Q6; Int. 2 Q7) | Cognitive offloading; perceived effort | Add a learning mode: card fades as the professor learns the name, and acts as a pronunciation coach |
| A3 | Opt-in makes consent sufficient | **Partly.** Neither fears refusing, but Int. 1 wants a guarantee that opting out "doesn't go against me," and wants proof from another student before trusting it. (Int. 1 Q12, Q16, Q17) | Power asymmetry; informed consent | No-penalty statement, professor cannot see decliners, peer demo |
| A4 | Minimal info (name, pronunciation, pronouns) is enough | **Different, not smaller.** Both accept *previous questions/interactions*; Int. 2 also accepts major and project. Both reject location, photos, social media. (Q8, Q9) | Data minimization; contextual integrity | Student-approved fields, including past questions, each toggleable |
| A5 | Camera capture of non-enrolled students is tolerable | **Conditional.** Int. 1: "doesn't seem fair." Int. 2: acceptable only if nothing personal is extracted and nothing stored until consent. (Q14) | Contextual integrity | Discard non-enrolled frames immediately, visible active indicator |
| A6 | Attendance/grade linkage should be off | **Split.** Int. 1 finds it "scary" and wants a guarantee; Int. 2 sees accuracy benefits but would worry if it exposed a skipped class. (Q17) | Function creep; surveillance | Off by default and out of scope; document as an explicit guardrail |
| A7 | Who controls the data | **Split.** Int. 1: the student, for the semester only. Int. 2: the professor, securely, with FERPA in mind. (Q13) | Data governance | Student owns and can delete the profile; professor has access during the term; confirm FERPA with instructor |
| A8 | Accuracy and fairness are the main technical risk | **Not tested by interviews.** Neither raised it. Use `transcripts/` and the literature. `[FILL]` | Algorithmic fairness; automation bias | Confidence tiers, test across skin tones and lighting |
| A9 | Professors want cards constantly | **Not tested (students only).** Both said comfort depends on context. (Q15) | Cognitive load | Session-based, quiet by default; consider a professor/TA interview |

## 3. Feature ranking

| Rank | Feature | Evidence | Theory | Decision |
|---|---|---|---|---|
| 1 | Student-controlled opt-in, opt-out, deletion, term-limited, no-penalty guarantee | Int. 1 Q12-13, Q17; Int. 2 Q13, Q15-16 | Informed consent; power asymmetry | Build in prototype |
| 2 | Non-enrolled students: no card, frames discarded | Int. 1 Q14; Int. 2 Q14 | Contextual integrity | Build in prototype |
| 3 | Student-approved context card: name, pronunciation, past questions, optional note | Int. 1 Q8; Int. 2 Q8 | Data minimization | Build in prototype |
| 4 | Learning mode and pronunciation coach (card fades with use) | Int. 1 Q6-7; Int. 2 Q7 | Cognitive offloading; perceived effort | Build in prototype |
| 5 | Confirm / correct / dismiss with confidence tiers | Int. 1 Q10; Int. 2 Q10; `[FILL: transcripts]` | Trust calibration; automation bias | Build in prototype |
| 6 | Session-based activation and indicator (large lecture first) | Int. 1 Q15; Int. 2 Q15 | Contextual integrity | Show in clickthrough |
| 7 | Transparency: who can access, access log, plain-language policy | Int. 1 Q16; Int. 2 Q15-16 | Trust | Show in clickthrough |
| 8 | Guardrail: no location, photos, social media; no attendance or grades | Int. 1 Q9, Q17; Int. 2 Q9 | Function creep | Document |

## 4. Where GenAI actually matters
Recognition is the embedding match. The LLM turns the student's *approved*
fields into one glanceable line, e.g. *"Priya Shah, say PREE-yah. Last asked
about your capstone idea."* It must not invent facts or infer anything the
student did not provide.

## 5. Opportunity statement
Professors in larger classes want to make students feel known, and students
say being known by name makes them feel recognized. But students want the
professor's *effort* to stay visible and want strict control over the data.
ContextLens lets students opt in to a minimal, student-approved profile that
helps professors learn and correctly say names, with a no-penalty opt-out and
no storage for anyone who hasn't opted in.

## 6. Limitations of this evidence
- Only 2 interviews for this section; both are the interviewer's friends, so
  politeness bias is possible.
- Both interviewees are confident about refusing; quieter students may feel
  more pressure, which our results may understate.
- No professor perspective yet (A9).
- One answer ("add in some bias towards students who have opted in") was
  ambiguous and should be clarified.

## 7. Open questions
- FERPA: confirm with your instructor whether this prototype needs review.
- Which IS 492 theories should replace the tags above?
