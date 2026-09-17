### 3\. /reflections/ — Individual Reflections

## **Paper 1**

### **1\. Full Citation & Link**

Liu, X., Lee, D., Gonzalez, E. J., Gonzalez-Franco, M., & Suzuki, R. (2026). *VisionClaw: Always-on AI agents through smart glasses* (arXiv:2604.03486). arXiv. [https://arxiv.org/abs/2604.03486](https://arxiv.org/abs/2604.03486)

### **2\. Structured Summary**

**Research problem:** Existing AI agents can either act autonomously on digital tasks (web, email, calendar) or perceive the physical world through smart glasses, but not both at once — so glasses-based assistants stay limited to answering questions rather than actually completing tasks for the wearer. **Methodology:** The authors built VisionClaw on Meta Ray-Ban glasses, combining continuous visual/audio perception with an agent framework (OpenClaw) that can take real-world actions from speech commands; they tested it in a controlled lab study (N=12) comparing it against an always-on-only condition and an agent-only condition, then ran a longitudinal field deployment (N=4–5) over an average of \~14 days per participant. **Main findings:** Combining perception and execution cut task completion time by 13–37% and lowered perceived difficulty by 7–46% versus the two baselines; the field deployment additionally revealed that, once given a fully integrated system, users shifted toward opportunistically delegating tasks mid-activity rather than issuing discrete one-off commands.

### 

### 

### **3 Insights**

1. Coupling *always-on perception* with *agentic execution* (not just Q\&A) is what actually saves time — the lab study isolates this: perception alone or execution alone underperforms the combination.  
2. Real deployment (N=4–5, \~14 active days, 555 total interactions) surfaced a genuinely new interaction pattern — opportunistic, mid-activity delegation — that the shorter controlled study alone wouldn't have revealed.  
3. Their task categories (adding items to a cart, generating notes from documents, meeting briefings, calendar creation from posters) map closely onto our own "recognize and act on real-world context" goal, just applied to objects/documents rather than people.

### 

### **4 Limitations**

1. The deployment study is very small (N=4–5) — usage patterns may not generalize across broader demographics or longer time horizons.  
2. The system relies on cloud-based multimodal models (Gemini Live) for perception, which raises the same latency and privacy tradeoffs we're grappling with in our own project.

### **5 Project Inspiration**

Their "opportunistic delegation" finding suggests our person-recognition system should support the same passive, mid-conversation triggering rather than requiring the wearer to explicitly ask "who is this?" — the AR overlay should appear automatically once a face is matched, exactly as we implemented it.

---

## **Paper 2**

### **1\. Full Citation & Link**

Yang, B., Xu, L., Zeng, L., Guo, Y., Jiang, S., Lu, W., Liu, K., Xiang, H., Jiang, X., Xing, G., & Yan, Z. (2025). *ProAgent: Harnessing on-demand sensory contexts for proactive LLM agent systems* (arXiv:2512.06721). arXiv. [https://arxiv.org/abs/2512.06721](https://arxiv.org/abs/2512.06721)

### **2\. Structured Summary**

**Research problem:** Most LLM agents are reactive — they only act when the user gives an explicit instruction — which raises both the physical and cognitive effort required to get help, especially in hands-free wearable settings. **Methodology:** The authors propose ProAgent, which uses a tiered, on-demand perception module to sense the environment only when needed (rather than continuously) and extract layered context combining sensory data with the user's persona; a context-aware reasoning module then maps this to predicted user needs and tool calls. They implemented it on AR glasses paired with an edge server (NVIDIA Jetson Orin) and evaluated it across six vision-language models of different sizes (2B–32B parameters), using a real-world testbed, a public benchmark dataset, and a user study. **Main findings:** ProAgent achieved up to 33.4% higher proactive-prediction accuracy and 16.8% higher tool-calling F1 score than state-of-the-art baselines, used 1.79x less memory, and improved user-reported satisfaction by 38.9% across five dimensions of proactive assistance.

### 

### 

### **3 Insights**

1. The "tiered perception" design — sensing the environment only on-demand rather than continuously — directly addresses the compute/battery/privacy cost of always-on cameras, a constraint we've been treating loosely.  
2. The quantified gains held across six VLMs of varying size (2B–32B parameters), showing the approach isn't just a large-model trick.  
3. Their real-world testbed used an AR glasses \+ edge server (Jetson Orin) architecture, which is a concrete, buildable reference point for how our own project could move from webcam simulation to real edge hardware.

### **4 Limitations**

1. Evaluation is testbed-based rather than a long-term in-the-wild deployment, so ecological validity (how well findings hold in messy daily life) is less proven than VisionClaw's approach.  
2. The paper doesn't address what happens when the proactive prediction is wrong or unwanted — a real risk in our person-recognition use case, where a false identification is worse than staying silent.

### **5 Project Inspiration**

Their tiered/on-demand perception model is directly applicable: our system should only run the (comparatively expensive) LLM call when a face-match confidence crosses a threshold, not on every frame \- we already implemented a cooldown cache for this reason, and this paper gives it a stronger justification.

