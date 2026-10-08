# Testing Notes, Interview Insights & Personal Reflection


## 1. Testing Notes (Minimal Prototype Validation)
Given our early project stage, we conducted minimal testing to focus on quick feasibility checks:
* **Prompting & HUD UI Checks**: Tested basic text cards. Confirmed HUD text must remain under 10 words in the top peripheral display to avoid visual occlusion and awkward eye-contact loss.
* **Facial Recognition**: Implemented basic facial recognition paired with a user-inputted note. Confirmed good accuracy in controlled lighting and distance situations.

## 2. Interview Insights

### Interview 3 (Large Lecture Hall, ~80 Students)
* **Context**: CS student whose name is frequently mispronounced by instructors.
* **Key Insights**:
  * **Accuracy**: High fear of misidentification (*"Getting called the wrong name is a lot more embarrassing than asking"*).
  * **Privacy & Battery**: Demanded strict opt-in consent, no participation tracking, and offloaded processing to save battery.
  * **UX**: Strongly endorsed phonetic guides as a memory tool.

### Interview 4 (Small Seminar, ~15 Students)
* **Context**: Music student using a preferred nickname.
* **Key Insights**:
  * **Profile Authority**: Rejected default Canvas names; insisted students must have 100% control over profile info.
  * **Latency & Friction**: Delay in name rendering sounds unnatural; required dynamic multi-angle face recognition and visible recording LEDs.


## 3. Personal Reflection
* **Pivot to Calm Memory Aid**: Shifted from generating live AI answers to simple memory assistance (names, phonetics, pronouns).
* **Student Data Authority**: Learned that official data is often wrong for nicknames; student opt-in and control are essential.
* **Complementarity over Reliance**: AI should serve as a temporary pronunciation coach (Learning Mode) rather than a permanent crutch or surveillance tool.
