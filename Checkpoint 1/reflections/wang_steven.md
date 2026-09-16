## Paper 1: Wang et al. (2026) — Technical Architecture and Agentic AI

### 1. Full Citation & Link
Wang, J., Jeon, S., & Jeon, G. (2026). The Evolution of Consumer-Grade AR Smart Glasses. IEEE Consumer Electronics Magazine, 1–9. https://doi.org/10.1109/MCE.2026.3718153

### 2. Structured Summary
Consumer-grade augmented reality smart glasses are undergoing a fundamental transition from tethered, screen-mirroring display peripherals into autonomous, spatially aware cognitive assistants. To address the computational, thermal, and power constraints of executing computer vision and generative AI on wearable hardware, the authors propose a closed-loop, three-layer split-processing architecture consisting of Perception, Processing, and Interaction layers. The processing layer evaluates a dual-track strategy combining a Native C++/NCNN track running an INT8-quantized, NMS-free YOLO26-nano model for low-latency object detection with a Unity 6/C# track handling XR SLAM tracking and stereoscopic 3D spatial rendering via a JNI bridge. Furthermore, an agentic AI framework (OpenClaw) is integrated to interpret semantic detection streams from the object detector and orchestrate context-aware, multi-step tasks using Large Language Models. Through benchmarks and an illustrative proactive dietary assistant use case, the evaluation confirms that local on-device neural network execution can sustain real-time spatial consistency and proactive assistance without relying on heavy cloud infrastructure.

### 3. Three Key Insights
1. **Heterogeneous Split-Processing Architecture**: Decoupling lightweight display optics from an external compute unit via USB-C keeps the wearable glasses comfortable while sustaining intense edge-AI inference workloads.
2. **Dual-Track Runtime Optimization**: Separating real-time neural network inference (Native C++/NCNN track) from spatial UI rendering and SLAM anchoring (Unity 6/C# track) resolves the conflict between computational throughput and spatial development velocity.
3. **Proactive Agentic Workflows**: Combining lightweight computer vision object detection with autonomous LLM agent frameworks (OpenClaw) transforms AR glasses from passive displays into proactive assistants that retrieve and present contextual domain knowledge.

### 4. Two Limitations or Risks
1. **Hardware Thermal and Power Envelope Constraints**: Running continuous high-performance neural inference alongside wireless data streaming generates significant thermal dissipation and power demands, requiring careful management of microdisplay and compute power usage.
2. **Susceptibility to Visual Information Manipulation and Agent Reasoning Errors**: Relying on visual perception and visual token compression introduces vulnerabilities to visual manipulation attacks, object misclassifications, and agentic reasoning hallucinations during real-time tasks.

### 5. One Concrete Inspiration
* **Decoupled Local Edge-Agent Co-Pilot Pattern**: Implementing a native C++ object detection pipeline that passes detected product bounding boxes via a JNI bridge to an agentic LLM layer, automatically displaying anchored 3D floating specification cards in Unity.

## Paper 2: Pfeifer et al. (2023) — In-Store Retail & Decision Support

### 1. Full Citation & Link
Pfeifer, P., Hilken, T., Heller, J., Alimamy, S., & Di Palma, R. (2023). More than meets the eye: In-store retail experiences with augmented reality smart glasses. Computers in Human Behavior, 146, 107816. https://doi.org/10.1016/j.chb.2023.107816


### 2. Structured Summary
While mobile touchscreen augmented reality is widely used in retail, empirical research remains sparse regarding whether hands-free AR smart glasses provide superior decision support in physical store environments. Grounding their study in embodied cognition theory and technological embodiment, the authors conducted a controlled laboratory experiment with 308 participants comparing Magic Leap One AR smart glasses against an iPad AR touchscreen app in an in-store furniture shopping scenario. The data were analyzed using the PROCESS macro to evaluate parallel and sequential mediation chains linking technological embodiment to consumer purchase intentions. Results demonstrate that the higher technological embodiment of AR smart glasses creates lower mental product intangibility and higher immersion compared to touchscreen devices. This enhanced interface evaluation sequentially improves customer decision comfort, satisfaction, and ease of evaluation, directly increasing consumer purchase intentions in retail environments.

### 3. Three Key Insights
1. **Superiority of Technological Embodiment**: Head-mounted optical displays place digital product holograms in closer psychological and sensory proximity to the human body than handheld touchscreen devices.
2. **Reduction of Mental Product Intangibility**: Viewing life-sized digital product overlays through natural head movements reduces the cognitive effort required for shoppers to mentally imagine how products look and fit in physical space.
3. **Sequential Uplift in Decision Comfort and Purchase Intentions**: Higher interface immersion and tangible product visualization translate into elevated decision comfort, shopping satisfaction, and evaluation ease, directly driving final purchase commitment.

### 4. Two Limitations or Risks
1. **Ergonomic Compatibility Issues for Eyeglass Wearers**: Participants wearing prescription glasses experienced physical alignment and fitting difficulties when wearing optical see-through smart glasses over their frames.
2. **Sample Homogeneity and Novelty Bias**: The study relied exclusively on a university student sample, whose initial excitement for novel AR smart glass hardware may exaggerate positive evaluations compared to broader consumer demographics.

### 5. One Concrete Inspiration
* **Hands-Free Spatial Retail Assistance Overlay**: Designing an AR heads-up display that identifies physical store items or vacant store locations and projects life-sized 3D product variations with interactive pricing, customization, and stock information directly in the user's field of view.