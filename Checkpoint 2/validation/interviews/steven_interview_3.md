# Interview 3

* **Interviewee:** International CS student in large ~80 person lecture halls. Frequently participates, but his name is constantly mispronounced by instructors and TAs.

#### 1. Accuracy & Hallucinations
> *"Getting called the wrong name is a lot more embarrassing than just asking 'What was your name again?'"*
* **Analysis:** Face misclassification in large halls (due to distance, lighting, or partial face occlusion) severely damages trust. False-positive gesture detection creates social awkwardness during live lectures.

#### 2. Reliability & Consistency
> *"Yeah I feel it'd be hard to detect faces from so far away especially behind people, but professors don't call by name in big lectures anyway."*
* **Analysis:** Variations in distance, lighting, and occlusion can interfere with facial recognition. Our project is more relevant for smaller lectures where calling by name is more common, which naturally eases some concerns from above.

#### 3. Latency & Performance
> *"Does the professor just stare at me for a few seconds and then glance down at some text? That would feel really strange I think."*
* **Analysis:** Facial embedding lookup + HUD rendering latency is very important avoid awkward staring, and the way text is displayed should be more discreet.

#### 4. UX Friction & Human–AI Teaming
> *"I like the idea of a pronunciation guide."*
* **Analysis:** Strong endorsement for using AI as a memory augmentation tool to help remember names, pronunciations, pronouns.

#### 5. Safety & Guardrails
> *"I would only participate if there is strict opt-in consent. Also, I would be very uncomfortable with participation tracking."*
* **Analysis:** Being clear about consent is very important, and students may fear that identity recognition will be secretly linked to participation grading or other evaluation.

#### 6. Cost & Efficiency
> *"Continuous video processing on smart glasses would probably drain the battery, you could offload the face processing to a phone or something."*
* **Analysis:** Consider a split-processing architecture: capture video frames on glasses, run heavy facial vector matching on an edge device, and send lightweight HUD rendering commands back to the glasses.