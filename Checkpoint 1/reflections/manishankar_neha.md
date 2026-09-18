# Paper 1: iKnowiSee

## 1. Full Citation & Link

Liang, Q., Chen, Y., Li, W., Lai, M., Ni, W., & Qiu, H. (2024). *iKnowiSee: AR Glasses with Language Learning Translation System and Identity Recognition System Built Based on Large Pre-trained Models of Language and Vision and Internet of Things Technology*. In *Intelligent Networked Things* (pp. 12–24). Springer. https://doi.org/10.1007/978-981-97-3948-6_2

## 2. Structured Summary

The paper presents iKnowiSee, an AR glasses system that combines language-learning translation with identity recognition. The system is built around large pretrained models for language and vision and uses Internet of Things technology to support its AR-glasses-based functionality. The identity-recognition component is especially relevant because it connects visual recognition with information that can be presented through an AR interface. Unlike a system that only performs face recognition, iKnowiSee demonstrates how recognition can be part of a larger wearable AI experience involving language and visual information. This paper is particularly relevant to ContextLens because it shows that combining identity recognition, large AI models, and AR glasses is a technically explored direction rather than treating each component as a separate system.

## 3. Three Key Insights

### 1. Identity recognition can be part of a larger AI interaction

A useful takeaway is that recognizing a person does not have to be the final output. Recognition can serve as the starting point for providing additional information or AI assistance through the wearable interface. This supports our ContextLens pipeline of recognizing a consented person and then retrieving relevant information.

### 2. AR glasses can combine multiple AI capabilities

The paper combines vision and language capabilities within an AR-glasses system rather than treating the glasses as only a display device. This influenced how I think about ContextLens because our project also needs several components—recognition, information retrieval, and language generation—to work together as one interaction.

### 3. Wearable AI should focus on the interaction between components

ContextLens is not just a facial-recognition system or an LLM application. The value comes from connecting recognition with approved contextual information and presenting that information at the right time. iKnowiSee helped reinforce the idea that the overall system architecture and user interaction are just as important as the individual AI models.

## 4. Two Limitations or Risks

### 1. Identity recognition creates privacy concerns

A wearable system that recognizes people can create privacy concerns, particularly if recognition happens without a person's knowledge or permission. For ContextLens, this means recognition should be restricted to people who have explicitly enrolled and consented rather than attempting to identify everyone in the camera's view.

### 2. Combining multiple technologies increases system complexity

A system that combines AR glasses, vision models, language models, and IoT components has more potential points of failure than a single-purpose application. Problems with recognition, network connectivity, model latency, or the wearable interface could affect the entire user experience. ContextLens should therefore keep the initial prototype focused on a small number of reliable functions instead of trying to implement every possible wearable AI capability at once.

## 5. One Concrete Project Inspiration

This paper directly inspired me to think of ContextLens as a complete wearable interaction pipeline rather than just a face-recognition tool. When the glasses recognize a consented customer, the system could retrieve only the approved information associated with that person and use an LLM to turn it into a short reminder, such as their preferred order or a previous conversation topic. The employee could then confirm, correct, or dismiss the suggestion. This keeps the AI useful while keeping the employee in control of what information is actually used.

# Paper 2: GazeMind

## 1. Full Citation & Link

Wang, B., Liu, Y., Newman, B., Fernandes, A. S., Wang, Z., Cavin, R., Cox, M. A., Rajanna, V., Bolte, T., Hunfalvay, M., Bagci, U., & Proulx, M. J. (2026). *GazeMind: A gaze-guided LLM agent for personalized cognitive load assessment*. arXiv. https://arxiv.org/abs/2605.05790

## 2. Structured Summary

The paper addresses the problem that current smart-glasses AI assistants have limited awareness of a user's internal cognitive state and therefore cannot easily determine when a person needs assistance. The researchers propose GazeMind, a gaze-guided LLM agent that uses eye-tracking information as structured input for LLM reasoning about cognitive load. The system uses a task-guidance reasoning approach and incorporates user-specific characteristics and historical information to support personalized predictions without requiring LLM fine-tuning for every task. The researchers also introduce CogLoad-Bench, a gaze-based cognitive-load dataset containing data from 152 participants, more than 40 hours of multimodal recordings, and more than 10,000 real-time annotations. Their experiments report that GazeMind outperformed baseline approaches by more than 20% across the reported evaluation metrics.

## 3. Three Key Insights

### 1. Context can make an AI assistant more useful

The paper shows that an AI system can use behavioral context, such as gaze, instead of relying only on explicit user commands. This is relevant to ContextLens because a service employee should not always have to manually ask the system for help while interacting with a customer.

### 2. Personalization can be built into the reasoning process

GazeMind incorporates user-specific characteristics and historical references when making predictions. This made me think about how ContextLens could use an employee's approved interaction history or preferences to determine which customer information is most relevant rather than showing every piece of stored information.

### 3. Proactive assistance needs a meaningful trigger

The system demonstrates the value of using contextual signals to determine when assistance should happen. For ContextLens, recognition confidence could serve as one trigger, while other signals such as the employee's attention or an active interaction could eventually determine whether a suggestion should appear.

## 4. Two Limitations or Risks

### 1. Incorrect interpretation of behavioral signals could lead to bad assistance

Gaze does not always indicate exactly what a person is thinking or what they need. Looking at something does not necessarily mean that the user is confused or wants assistance. ContextLens would face a similar problem if it tried to infer too much from an employee's behavior.

### 2. The system requires additional sensing hardware

GazeMind relies on eye-tracking information in addition to the normal outward-facing camera capabilities of smart glasses. Adding sensors can increase hardware complexity, cost, power consumption, and calibration requirements. A ContextLens prototype should therefore avoid depending on specialized sensors unless testing shows that they provide enough benefit.

## 5. One Concrete Project Inspiration

This paper inspires a context-aware trigger system for ContextLens. Instead of immediately showing customer information whenever a face is recognized, the system could consider additional signals before displaying a suggestion—for example, whether the employee is currently interacting with the recognized person and whether the recognition confidence is high enough. This could reduce unnecessary notifications and make the AI feel more helpful rather than distracting. In the future, gaze could also be explored as an optional signal for determining which person or object the employee is currently focused on.
