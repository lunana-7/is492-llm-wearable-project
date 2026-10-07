## Interview 4

* **Interviewee:** Music student in small, interactive 15-person discussion seminars. Prefers a nickname.

#### 1. Accuracy & Hallucinations
> *"Wouldn't the glasses call me by whats on Canvas instead of (nickname)? What if the AI hallucinates a nickname?"*
* **Analysis:** It's important for students to be able to decide and edit information about themselves, and for our project to only use information given by students.

#### 2. Reliability & Consistency
> *"We sit in small groups sometimes that don't face the front of class, and the professor walks around."*
* **Analysis:** Facial recognition needs to be able work while the professor is moving and be able to recognize faces at different angles.

#### 3. Latency & Performance
> *"I think a delay before saying someone's name would sound super unnatural."*
* **Analysis:** Facial embedding lookup + HUD rendering latency is very important avoid unnatural pauses, and the way text is displayed should be more discreet.

#### 4. UX Friction & Human–AI Teaming
> *"I wouldn't mind a nickname reminder, sometimes when a professor forgets a couple times I give up."*
* **Analysis:** Strong endorsement for using AI as a memory augmentation tool to help remember names, pronunciations, pronouns.

#### 5. Safety & Guardrails
> *"I don't think I would opt-in, but I guess I'd be fine with it if my face wasn't tracked and I knew it was happening."*
* **Analysis:** Clear consent and physical visual indicators like a LED status light are necessary for social comfort.

#### 6. Cost & Efficiency
> *"What about professors with long or back-to-back lectures (running out of battery)?"*
* **Analysis:** Consider a split-processing architecture: capture video frames on glasses, run heavy facial vector matching on an edge device, and send lightweight HUD rendering commands back to the glasses to reduce battery drain.