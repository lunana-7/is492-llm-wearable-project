# **ContextLens: A Wearable AI Assistant for Recognition and Contextual Memory**

## **Project Title & Tagline**

**ContextLens  
A wearable AI platform that helps service employees recognize consented
customers, retrieve relevant context, and deliver faster, more
personalized interactions.**

## **Team Members & Roles**

\* Highlighted members are the leads of each responsibilities

<table>
<colgroup>
<col />
<col />
<col />
</colgroup>
<thead>
<tr class="header">
<th><strong>Team Member</strong></th>
<th><strong>Responsibilities</strong></th>
<th><strong>Email</strong></th>
</tr>
<tr class="odd">
<th><strong>Aman</strong>, Steven</th>
<th>Facial-recognition system, database schema, and backend
integration</th>
<th><p>abj4@illinois.edu</p>
<p>steven43@illinois.edu</p></th>
</tr>
<tr class="header">
<th><strong>Aman</strong>, <strong>Steven</strong></th>
<th>Wearable hardware, camera, audio, and display integration</th>
<th><p>abj4@illinois.edu</p>
<p>steven43@illinois.edu</p></th>
</tr>
<tr class="odd">
<th><strong>Steven</strong>, Min</th>
<th>Frontend application and user interface</th>
<th><p>steven43@illinois.edu</p>
<p>mink4@illinois.edu</p></th>
</tr>
<tr class="header">
<th><strong>Neha,</strong> Aman,</th>
<th>Speech recognition, summarization, and user testing</th>
<th><a
href="mailto:abj4@illinois.edu"><u>abj4@illinois.edu</u></a><br />
nmani7@illinois.edu</th>
</tr>
<tr class="odd">
<th><strong>Min</strong>, Neha</th>
<th>Product design, documentation, and project coordination</th>
<th><p>mink4@illinois.edu</p>
<p>nmani7@illinois.edu</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## **Problem Statement & Motivation**

Employees in cafÃ©s, restaurants, hotels, retail stores, conferences, and
enterprise service environments often interact with many customers or
coworkers in a short period of time.

Remembering names, preferences, previous conversations, and
organizational roles can be difficult, especially during busy periods.

For example:

- A **barista** may recognize a regular customer but not remember their
  > usual order. An event employee may meet hundreds of attendees but
  > struggle to recall previous conversations.

- A **receptionist** may need to search through a database before
  > finding basic information about a visitor.

Current systems require employees to stop working, access a computer or
mobile device, and manually search for information.  
= This slows down service and creates inconsistent customer experiences.

ContextLens addresses this problem by combining programmable glasses,
computer vision, speech recognition, and contextual AI.

The system will allow authorized employees to receive relevant
information hands-free while maintaining user consent, privacy, and
human control.

## **Commercial Target Users & Personas**

ContextLens will be commercialized as a B2B wearable AI platform for
organizations where employees interact with many customers, coworkers,
or event participants.

### **Persona 1: Customer-Facing Service Employees**<img src="images/image3.jpg"

Examples include baristas, restaurant staff, hotel employees,
receptionists, and retail workers.

They use ContextLens to:

- Recognize consented regular customers or coworkers.

- Retrieve approved preferences, such as a regular order.

- Reduce the time spent searching through a POS or customer database.

- Provide faster and more personalized service.

### **Persona 2: Enterprise Operations and Customer-Experience Managers**
*These are the organizational buyers who manage employee productivity,
customer experience, and internal systems.*

They use ContextLens to:

- Create and manage consent-based employee or customer profiles.

- Connect wearable interactions with existing CRM, HR, or point-of-sale
  > systems.

- Monitor whether the system reduces lookup time and improves service
  > efficiency.

- Establish privacy, access-control, and data-retention policies.

### **Persona 3: Event and Conference Staff**

Event organizers, conference teams, university career fairs, and
professional networking organizations often manage large numbers of
participants in a short period of time.

They use ContextLens to:

- Recognize registered attendees who have opted into the system.

- Retrieve names, organizations, roles, and approved networking
  > information.

- Help staff remember previous conversations.

- Generate short summaries after meetings or networking interactions.

## **Core Commercial Tasks**

The first commercial version of ContextLens will focus on three primary
tasks:

1.  **Consent-based identity recognition  
    > **The system recognizes enrolled customers, employees, or event
    > participants and displays or speaks their name.

2.  **Context and preference retrieval  
    > **The system provides limited, approved information such as
    > customer preferences, job roles, previous interactions, or service
    > history.

3.  **Interaction summarization  
    > **The system records authorized conversations and creates short
    > summaries that can be reviewed or added to an organizationâ€™s CRM
    > system.

## **Competitive Landscape**

| **Existing Tool or System**                   | **Strength**                                          | **Limitation**                                                               |
|-----------------------------------------------|-------------------------------------------------------|------------------------------------------------------------------------------|
| Smart glasses                                 | Provide cameras, audio, and sometimes visual displays | Often lack **organization-specific memory** and structured profile retrieval |
| Facial-recognition APIs                       | Detect and match faces                                | Do not provide a **complete wearable workflow** or business-specific context |
| CRM and point-of-sale systems                 | Store customer preferences and service history        | Require employees to manually search for information                         |
| LinkedIn and employee directories             | Provide professional identity information             | Are not designed for real-time, hands-free recognition                       |
| Voice assistants and note-taking applications | Record and summarize speech                           | Do not connect spoken interactions to **authorized identity data**           |
| Manual notes and employee memory              | Flexible and familiar                                 | Slow, inconsistent, and difficult to access during active work               |

ContextLens differentiates itself by combining <u>identity recognition,
contextual retrieval, wearable interaction, and conversation
summarization in one organization-controlled system</u>.

## **Initial Concept & Value Proposition**

ContextLens is a wearable AI system consisting of programmable glasses,
a companion application, a recognition backend, and a secure
organization-managed database.

When the glasses capture an image, the system will:

1.  Detect whether a person is present.

2.  Generate a facial embedding using an approved recognition model.

3.  Compare the embedding with enrolled, consented profiles.

4.  Retrieve only the information the employee is authorized to access.

5.  Return the personâ€™s name and relevant information through audio or
    > display.

6.  Allow the employee to confirm, correct, or dismiss the result.

### **Example Customer-Service Scenario**

A regular customer visits an internal cafÃ©. The customer has opted into
a profile containing limited information about their usual order. When
the customer is recognized, the employee may receive a prompt such as:

> â€œAlex Kim â€” regular iced espresso. Confirm order?â€

The employee remains in control of the interaction. The system does not
automatically place an order, expose sensitive information, or identify
individuals who have not enrolled.

### **Example Event Scenario**

A conference attendee who has opted into ContextLens approaches an event
staff member. The glasses display the attendeeâ€™s name, organization, and
previously approved networking information. After the conversation,
ContextLens generates a short summary that the staff member can review
and save to the eventâ€™s CRM system.

### **Technical Architecture**

- **Wearable hardware:** Programmable glasses with a camera, microphone,
  > audio output, and optional projection or display.

- **Face detection and recognition:** InsightFace with an ArcFace-based
  > facial-embedding model.

- **Backend:** Python/FastAPI service for image processing, profile
  > retrieval, and system logic.

- **Database:** PostgreSQL with pgvector for storing and comparing
  > facial embeddings.

- **Frontend:** React-based web or companion application.

- **Speech-to-text:** Whisper or another approved speech-recognition
  > model.

- **Summarization:** A language model that creates short, structured
  > interaction summaries.

- **Connectivity:** Bluetooth or Wi-Fi connection between the glasses,
  > companion device, and backend.

- **Processing:** Cloud processing during the prototype phase, with
  > future investigation into local or edge processing.

### **Privacy and Safety Design**

Because ContextLens involves biometric information, privacy will be a
central design requirement.

The prototype will:

- Use only consented participants and images.

- Avoid identifying unknown people.

- Store the minimum information necessary.

- Provide profile deletion and correction controls.

- Require user confirmation before important actions.

- Restrict access based on organizational permissions.

- Test performance across different angles and lighting conditions.

- Clearly communicate when the camera or audio recording is active.

- Avoid unrestricted scraping of Instagram, LinkedIn, or other public
  > websites.

## **Initial Commercialization Strategy**

ContextLens will initially target internal cafÃ©s, restaurants,
hospitality businesses, and enterprise service teams. These environments
are attractive early markets because employees interact with many
recurring customers and need to retrieve information quickly.

The initial product will be sold to organizations rather than individual
consumers. Organizations will pay for:

- Wearable device access.

- Secure profile and database management.

- Integration with existing CRM or point-of-sale systems.

- Administrative controls and privacy management.

- Usage-based AI processing and summarization.

The product can later expand into conferences, professional networking,
hotels, retail, and other industries where fast recognition and
contextual memory improve human interactions.

## **Prototype Development Plan**

### **Stage 1: Controlled Recognition Prototype**

The first stage will use approximately four to five consented images per
participant. The system will:

- Store a personâ€™s name and approved profile data.

- Generate facial embeddings.

- Match a captured image to the enrolled database.

- Display or speak the recognized personâ€™s name.

- Record confidence scores.

- Allow the employee to reject incorrect matches.

### **Stage 2: Context and Interaction Prototype**

The second stage will add:

- Images from different angles and lighting conditions.

- Additional approved profile information.

- Customer preferences or event information.

- Audio capture and speech-to-text.

- Short interaction summaries.

- A wearable or simulated wearable interface.

- A basic CRM or point-of-sale integration.

## **Milestones Roadmap to Checkpoint 4**

| **Timeline**          | **Milestone**                             | **Deliverables**                                                                                              |
|-----------------------|-------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| Week 1                | Requirements and responsible-use planning | Final commercial scope, user personas, consent process, privacy requirements, and technical architecture      |
| Week 2                | Database and enrollment system            | Database schema, profile form, consent workflow, and pilot participant dataset                                |
| Week 3                | Face-recognition prototype                | Face detection, ArcFace embeddings, similarity matching, confidence scores, and initial accuracy test         |
| Week 4                | Application interface                     | React interface for enrollment, profile management, recognition results, correction, and deletion             |
| Week 5                | Wearable connection                       | Camera capture, audio output, Bluetooth/Wi-Fi connection, and simulated or physical glasses demonstration     |
| Week 6                | Context and summarization features        | Approved preference retrieval, speech-to-text pipeline, and short interaction summaries                       |
| Week 7                | Integrated commercial scenario            | End-to-end demonstration in a cafÃ©, hospitality, enterprise, or event setting                                 |
| Week 8 / Checkpoint 4 | Evaluation and final presentation         | Working prototype, evaluation results, user feedback, privacy review, limitations, and commercialization plan |

## **Evaluation Metrics**

The prototype will be evaluated using the following measures:

- **Recognition accuracy:** At least 90% accuracy for enrolled
  > participants in controlled lighting.

- **False-positive rate:** No more than 5% incorrect matches.

- **Response time:** Name or approved profile information returned
  > within two seconds of image capture.

- **Summarization quality:** Users rate summaries at least 4 out of 5
  > for accuracy and usefulness.

- **Usability:** At least 4 out of 5 average satisfaction among pilot
  > users.

- **Service efficiency:** At least 30% reduction in time spent searching
  > for customer or attendee information.

- **Commercial usefulness:** At least 70% of pilot employees report that
  > ContextLens improves their ability to provide personalized service.

- **Privacy compliance:** 100% of stored profiles must be consented, and
  > users must be able to view, correct, and delete their information.

- **Robustness:** Recognition tested across multiple angles, distances,
  > lighting conditions, and levels of background activity.

## **Expected Outcome**

By Checkpoint 4, our team will deliver an integrated ContextLens
prototype that demonstrates:

1.  Consent-based facial enrollment.

2.  Recognition of approved customers, employees, or event participants.

3.  Name and context retrieval through audio or display.

4.  Basic wearable-device interaction.

5.  Conversation transcription and summarization.

6.  A user-facing application for managing profiles and permissions.

7.  A commercial use-case demonstration.

8.  An evaluation of accuracy, response time, usability, service
    > efficiency, and privacy.

The long-term vision is for ContextLens to become a responsible wearable
AI platform for hospitality, enterprise service, conferences, retail,
and professional networking. Its purpose is not to replace human
judgment, but to help employees remember relevant information and
provide faster, more personalized human interactions.
