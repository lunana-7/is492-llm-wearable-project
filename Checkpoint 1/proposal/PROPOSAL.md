# Project Proposal

### Problem Significance

Customer-facing service employees often interact with many people throughout a workday but have limited ability to remember names, preferences, previous conversations, or relevant organizational information. In settings such as cafés, retail stores, hotels, conferences, and other service environments, employees may recognize a returning customer without remembering the details that would allow them to provide personalized service. Existing systems such as CRM, POS, loyalty, and employee-management tools can store useful information, but employees typically have to stop what they are doing, open a device, and manually search for that information. This creates friction and can slow down interactions.

ContextLens proposes a wearable AI system that helps service employees recognize consented, enrolled customers, retrieve approved contextual information, and receive a concise reminder while continuing the interaction. The goal is not to replace the employee’s judgment, but to reduce the effort required to access information and support more consistent, personalized service.

### Prior Work and Gap

Our literature review identified several technologies that address pieces of this problem. Research on AR glasses and wearable AI demonstrates the potential for hands-free interaction, proactive assistance, personalized interfaces, and on-device or edge processing. Other work explores privacy and consent challenges associated with always-on visual sensing, while facial-recognition research provides methods for matching faces to known identities.

However, these technologies do not directly address our specific workflow: connecting consent-based identity recognition with organization-controlled customer context and delivering that information through a wearable interface during a live service interaction. Existing CRM and POS systems provide structured customer information but generally require manual lookup, while wearable devices can provide cameras, microphones, and displays without necessarily connecting those capabilities to an organization’s approved customer context. ContextLens aims to connect these components into one human-AI interaction.

### Technical Approach

Our initial prototype will simulate a wearable glasses system using a camera feed and a software interface. The system will first detect and recognize an enrolled person using facial embeddings generated with ArcFace and compare them against stored profiles. Only people who have explicitly consented to enrollment will be eligible for recognition.

After a successful match, the system will retrieve approved contextual information associated with that profile from a backend database. The retrieved information may include preferences, previous interaction notes, event or organizational information, or other context approved for use. A generative AI model will then transform the relevant retrieved information into a short, readable reminder for the employee. For example, approved information about a returning customer could be converted into a concise reminder such as: “Alex Kim — regular iced espresso. You met at CS orientation.”

The planned architecture includes a Python/FastAPI backend, PostgreSQL with pgvector for profile and vector storage, a React-based interface, speech-to-text for future voice interaction, and a wearable or simulated wearable display. We will initially use cloud processing for the prototype while considering edge processing as a future direction.

### Checkpoint 2 Validation Plan

In Checkpoint 2, we plan to evaluate both the technical behavior and usefulness of ContextLens. We will conduct a systematic prompting study using at least three existing AI tools and test typical use cases, edge cases, and failure cases. We will examine issues such as hallucinated information, inconsistent responses, formatting problems, latency, and inappropriate safety behavior. Team members will also conduct speed-dating interviews with potential users or peers to identify usability problems and expectations around wearable assistance.

Our validation will help determine which capabilities provide meaningful value and which assumptions about the system need to change. Recognition accuracy and response latency will also be measured as supporting engineering metrics.

### Risks and Mitigation

Privacy is a primary risk because the system involves facial recognition and potentially sensitive customer information. We will restrict recognition to consented participants, avoid identifying unknown bystanders, minimize stored information, provide profile correction and deletion mechanisms, and use access controls for organizational data. The system will also communicate when sensing capabilities are active.

Another risk is incorrect recognition or hallucinated context. To reduce this risk, the LLM will receive retrieved, approved information rather than unrestricted personal data, and the employee will remain responsible for deciding whether to act on the recommendation. We will test different lighting conditions, viewing angles, and interaction scenarios to identify recognition failures. Finally, system latency and wearable hardware limitations may affect usability, so we will investigate event-driven processing and a split between wearable capture and external computation.
