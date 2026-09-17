## Paper 1: Handwriting Velcro

### 1. Full Citation & Link
Fang, F., Zhang, H., Zhan, L., Guo, S., Zhang, M., Lin, J., Qin, Y., & Fu, H. (2022). Handwriting Velcro: Endowing AR glasses with personalized and posture-adaptive text input using flexible touch sensor. *Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies*, 6(4), Article 163, 1–31. https://doi.org/10.1145/3569461

### 2. Structured Summary
Entering text on AR glasses is difficult because voice input, mid-air gestures, and small touch interfaces are not equally comfortable or practical across everyday situations. The researchers developed Handwriting Velcro, a flexible touch sensor that attaches to different body locations and lets users write characters with a finger. They explored how sensor placement interacts with body posture and developed a convolutional neural network that recognizes 36 characters, with active learning to personalize recognition through users’ corrections. User studies evaluated recognition, input speed, comfort, and social acceptance, including comparisons with TEXTile and a physical mini keyboard. Among six participants with higher initial error rates in the personalization study, average total error rate fell from 3.1% to 0.5% after six sessions. Separate comparison studies found average input speeds of about 12.3 words per minute, suggesting that the approach is useful for short text entry in varied contexts.

### 3. Three Key Insights
*   **Posture is part of interface design.** I usually think about an interface in terms of what appears on the screen, but this paper shows that where an input device sits on the body also shapes usability. An interaction that feels comfortable while sitting may become awkward while walking.
*   **Corrections can help a system adapt to its user.** The personalization approach uses corrections made during interaction to improve recognition. I like the idea of letting the system learn someone’s existing habits instead of requiring the person to learn a completely new input language.
*   **The best input method depends on the situation.** Voice input may be convenient in one setting and disruptive in another. For AR glasses, I would evaluate whether an interaction fits the environment alongside its speed and accuracy.

### 4. Two Limitations or Risks
*   **The prototype is not yet a complete everyday wearable.** It connects to a desktop computer through USB, and the authors acknowledge that its strip-based design can be inconvenient outside the study. Wireless operation, smaller electronics, and integration into clothing would need further development and evaluation.
*   **The strongest personalization result has a narrow scope.** The 0.5% error rate comes from six participants analyzed within a ten-person study using a repeated phrase while seated with the sensor on the forearm. I would not assume that result applies to unfamiliar text, other languages, or long-term use; the demonstrated character set is also limited to A–Z and 0–9.

### 5. One Concrete Inspiration
For our AR glasses project, I would prototype a quiet annotation feature using a small touch patch on the forearm. A user could explicitly activate the patch, write a short keyword to tag a captured image or saved explanation, and confirm the recognized text on the display. Corrections could gradually personalize recognition. This would give users a way to add notes during a lecture or in a shared space without speaking aloud.

---

## Paper 2: Efficient Depth Estimation for Unstable Stereo Camera Systems on AR Glasses

### 1. Full Citation & Link
Liu, Y., & Kwon, H. (2025). Efficient depth estimation for unstable stereo camera systems on AR glasses. In *2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)* (pp. 6252–6261). IEEE. https://doi.org/10.1109/CVPR52734.2025.00586

### 2. Structured Summary
AR glasses need accurate, fast depth estimation, but limited computing resources and changes in stereo camera alignment make this difficult. The researchers identified image rectification and cost-volume computation, which compares features between camera views, as major sources of processing delay. They developed MultiHeadDepth using hardware-friendly operations and extended it into HomoDepth, which predicts camera-view alignment and incorporates it through rectification positional encoding instead of requiring a separate image-rectification step. They evaluated the models using datasets including SceneFlow, Aria Digital Twin, and DTU, with latency measurements on a laptop and two edge platforms. Compared with Argos, MultiHeadDepth achieved reported accuracy improvements of 11.8–30.3% and latency reductions of 22.9–25.2%, while HomoDepth could directly process unrectified stereo images. These findings show that redesigning the surrounding processing pipeline can improve both efficiency and robustness, although the measured speeds still varied substantially across devices.

### 3. Three Key Insights
*   **Responsiveness depends on the whole pipeline.** Making a neural network faster does not solve delays caused by preparing its inputs. For our project, I would measure the time from camera capture to the displayed response, rather than relying only on model inference time.
*   **Wearable systems should expect physical changes.** Camera alignment can change when glasses bend or shift. This paper made me think of calibration as something a wearable system must accommodate during use, rather than a condition that stays fixed after setup.
*   **Hardware compatibility matters as much as model size.** The researchers improved efficiency by choosing operations that existing hardware and software handle well. A model with fewer parameters is not automatically the fastest option on the device we actually use.

### 4. Two Limitations or Risks
*   **Testing on proxy devices does not establish real-time performance on glasses.** The authors measured latency on a laptop, Jetson Orin Nano, and Snapdragon smartphone rather than deploying the complete system on AR glasses. HomoDepth took about 203 ms on the Orin GPU and 893 ms on the Snapdragon GPU, both above the paper’s stated target of under 100 ms.
*   **The evaluation does not cover every kind of everyday instability.** Some misalignment conditions were simulated through image transformations, and the models were trained separately for different datasets. I would want additional testing under rapid head movement, motion blur, and changing lighting before trusting the system to place information accurately in an unfamiliar environment.

### 5. One Concrete Inspiration
For an object-identification feature in our AR glasses project, I would prototype a label that appears beside the selected physical object using depth estimates. If the estimated position changes sharply across frames, the interface would temporarily show the information in a fixed display panel until the estimate stabilizes. This fallback is my design extension, not a feature evaluated in the paper, and would help prevent an unstable label from appearing to identify the wrong object. Implementing the depth-based version would require access to stereo camera images on the chosen hardware.