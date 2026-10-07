# Gap Analysis Matrix: ClassHUD System Validation (Interviews 1–4)


## 1. Executive Summary & Methodology

To validate the ClassHUD wearable AR smart glasses concept, our team conducted 8 interviews.

Using the **Gonzalez et al. (2026)** Human–AI Complementarity Framework, we systematically analyzed observed user feedback across six core dimensions (**Accuracy & Hallucinations**, **Reliability & Consistency**, **Latency & Performance**, **UX Friction & Teaming**, **Safety & Guardrails**, and **Cost & Efficiency**). Each insight is mapped to underlying cognitive pillars (**Reasoning**, **Memory**, **Attention**, **Meta-Coordination**) to derive explicit design requirements for the ContextLens system.

---

## 2. Interviews

| Interviewee | Class Context | Key Identity Needs | Core Attitudes & Insights |
| :--- | :--- | :--- | :--- |
| **1** | ~30-person class | Name mispronounced; no pronouns; shares previous questions only | Values instructor's *human effort* to learn names; wants glasses as a pronunciation coach; demands ironclad no-penalty opt-out guarantees. |
| **2** | 40–60 person class | Student leader; name mispronounced; shares name, major, project, notes | Feels recognized when known by name; fears cognitive over-reliance ("makes functional memory worse"); worried about automated attendance tracking. |
| **3** | ~80-person lecture | Large hall; name constantly mispronounced; needs phonetic guide | Highlights high embarrassment of face misclassification in large halls; rejects AI-generated answers; advocates offloading processing to save battery. |
| **4** | 12–25 person seminar | Small seminar; prefers nickname, pronouns (`they/them`) | Rejects official LMS/Canvas name defaults; fears HUD visual occlusion breaking eye contact in small circles; wants visible camera recording LED. |

---

## 3. Comprehensive Gap Analysis Matrix

| Dimension | Empirical Failure & Interview Insights | Theoretical Reading (Gonzalez et al. 2026 & Literature) | Design Decision & System Requirement |
| :--- | :--- | :--- | :--- |
| **1. Accuracy & Hallucinations** | **Interviewee 3:** *"Getting called the wrong name is a lot more embarrassing than just asking 'What was your name again?'"*<br><br>**Interviewee 1:** *"If the prof isn't able to still pronounce my name after telling them, then the glasses can be used to teach them how to pronounce it."* | **Memory Infrastructure & Interrogation Failure:** Confident false assertions or default LMS name overwrites damage user trust and cause acute social embarrassment. Uncalibrated AI memory lacks confidence indicators and student authority over profiles. | **Confidence-Tiered Badging & Student Profile Authority:** High confidence (≥80%) displays automatically; medium (50–79%) prompts *"Verify name?"*; low (<50%) displays nothing. Input allows students 100% authority to set preferred nicknames and phonetic guides, overriding Canvas defaults. |
| **2. Reliability & Consistency** | **Interviewee 3:** *"Yeah I feel it'd be hard to detect faces from so far away especially behind people."*<br><br>**Interviewee 2:** *"If we become overly dependent on this assistance, it might make our functional memory not as good."* | **Knowledge Infrastructure Break & Cognitive Offloading:** Dynamic seating, profile face angles, and long distances degrade facial recognition models. Excessive automation risks cognitive atrophy (*Gonzalez et al. 2026*). | **Multi-Angle Embeddings & Learning Mode:** Support multi-angle enrollment and fallback spatial grid seat mapping. Implement a **Learning Mode** where HUD cards fade after repeated successful uses, acting as a pronunciation coach rather than a permanent crutch. |
| **3. Latency & Performance** | **Interviewee 3:** *"Does the professor just stare at me for a few seconds and then glance down at some text? That would feel really strange I think."*<br><br>**Interviewee 4:** *"I think a delay before saying someone's name would sound super unnatural."* | **Temporal Attention Misalignment:** Processing delays force unnatural stares, breaking the synchronized conversational cadence between human and AI during real-time lecture delivery (*GazeMind* / *Wang et al. 2026*). | **Sub-1.2s Latency Budget & Peripheral Caching:** Enforce a strict **<1.2 second end-to-end latency budget** for face detection and HUD rendering. Pre-warm session feature caches for enrolled students so cards render in <200ms upon gaze fixation. |
| **4. UX Friction & Human–AI Teaming** | **Interviewee 1:** *"Would be cool, but I would want to be able to interact with the prof so it shows they're putting in effort to learn my name."*<br><br>**Interviewee 2:** *"If they knew my name, I would be more compelled to ask questions even through informal email because I feel that they would respond with care."* | **Attention Overload & Role Partitioning Gap:** Visual occlusion destroys eye contact and interpersonal rapport. Users demand strict role boundaries: AI owns **memory retrieval**, while human faculty retains **reasoning ownership**. | **Calm Peripheral HUD & Role Boundaries:** Limit HUD cards to **under 10 words** in top peripheral display space. Remove live AI answer generation entirely. Focus strictly on student-approved memory fields (name, phonetics, pronouns). |
| **5. Safety & Guardrails** | **Interviewee 1:** *"Want complete guarantee that sharing such information won't be used against me in any way and if I were to opt out also, it doesn't go against me."*<br><br>**Interviewee 2:** *"I would be worried if I did not attend class and the tech can verify that."* | **Contextual Integrity & Surveillance Risk:** Function creep (linking face recognition to attendance or grading) creates surveillance anxiety and destroys data fidelity (*Gonzalez et al. 2026* / *ContextLens*). | **ContextLens Consent Protocol & Hardware LED:** Non-enrolled student video frames are discarded immediately without logging. Isolate telemetry from Canvas gradebooks. Require a physical **hardware recording LED** on glasses and provide a no-penalty opt-out guarantee. |
| **6. Cost & Efficiency** | **Interviewee 3:** *"Continuous video processing on smart glasses would probably drain the battery, you could offload the face processing to a phone or something."* | **Heterogeneous Split Architecture & Operational Efficiency:** Continuous egocentric video processing causes severe thermal throttling and battery exhaustion on wearable frames (*Wang et al. 2026* / *ProAgent*). | **Split-Processing Architecture:** Capture frames on glasses, offload heavy facial vector matching to a companion smartphone/edge device via Bluetooth/Wi-Fi, and return lightweight display commands to the HUD. Terminate and delete all session data at term end. |

---

## 4. Theoretical Synthesis & Design Evolution

### A. Working Complementarity Claim
> *"ContextLens achieves human-AI complementarity by delegating **spatial tracking, memory retrieval (names, phonetics, pronouns), and aggregate attention filtering** to the AI agent, while preserving **sole subject-matter reasoning and pedagogical rapport** for the human instructor."*

### B. Shift in Assumptions Post-Validation
1. **From AI Answers to Memory Aids:** Initial designs considered generating live AI answers on the HUD. Interviewees overwhelmingly rejected this: students want human faculty expertise, leading us to restrict the AI to calm memory retrieval (names, phonetics, pronouns).
2. **From Canvas Overwrites to Student Profile Authority:** Interviewee 4 noted Canvas names are often inaccurate for nicknames. ContextLens grants students 100% control over their displayed profile.
3. **From Tool Dependence to Learning Mode:** Interviewees 1 and 2 raised concerns about professors over-relying on glasses and losing genuine effort. We introduced a **Learning Mode** where HUD cards fade as the professor learns the student's name, acting as a coach rather than a permanent crutch.
4. **From Always-On Glasses Processing to Split Architecture:** Interviewee 3 highlighted thermal and battery constraints. We adopted a split-processing pipeline offloading heavy compute to a companion device (*Wang et al. 2026*).
