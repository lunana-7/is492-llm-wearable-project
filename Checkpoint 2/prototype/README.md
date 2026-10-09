# ContextLens — Checkpoint 2 Prototype

**IS 492 | Consent-Based Recognition for Classroom Name Learning**

**Team:** Aman Joshi, Steven Wang, Min Kim, Neha Manishankar  
**Repository:** https://github.com/lunana-7/is492-llm-wearable-project

## Overview

ContextLens explores how smart glasses and a connected mobile phone could help professors remember students' names while preserving consent, privacy, and natural classroom interaction. The aim is **not** to replace a professor's effort to learn names: recognition should be a temporary memory aid.

## Current Prototype — Checkpoint 2

The current prototype **shows facial recognition results on the Android phone**. When the phone detects and recognizes an enrolled test participant, their identity is displayed on the phone. **The name and description are not yet displayed inside the smart glasses.**

### Current demo workflow

```text
Consenting test participant
          ↓
Face detected by current phone-based prototype
          ↓
Face matched against enrolled test profiles
          ↓
Recognition result displayed on Android phone
```

### How to present the prototype

1. Open the current Android prototype and show its face-recognition screen.
2. Demonstrate recognition with a consenting test participant who has been enrolled for the demo.
3. Show the identity result appearing **on the phone**, and explain the current limitations.
4. Introduce the planned glasses display, where a professor would see a brief, student-approved name and description without checking their phone.

**Suggested narration:** “For Checkpoint 2, we have a phone-based prototype that displays a person's identity when their face is recognized. Our next goal is to bring this experience directly into the smart glasses, so a professor can see an opted-in student's preferred name and a short description in their field of view. The phone display is what we are demonstrating today; the in-glasses display is future work.”

## Future Vision — Recognition and Display in Smart Glasses

```text
Student opts in and creates an approved profile
                      ↓
Smart glasses camera observes the student
                      ↓
Face matching against consented profiles
                      ↓
Confidence and consent checks
          ├── High (≥80%): show short name/profile card
          ├── Medium (50–79%): request verification
          └── Low (<50%) / not enrolled: show nothing
                      ↓
Name, pronunciation and brief description
appear directly in the glasses' heads-up display (HUD)
```

The thresholds above are **proposed design requirements**, not calibrated performance measurements. Recognition processing could involve the phone or supported on-device hardware; the exact architecture remains to be validated. The intended in-glasses experience is a future capability, **not part of the current live demo**.

## Checkpoint 2 Research and Design Decisions

The team conducted **eight speed-dating interviews** and refined the concept from cafe customer recognition into a classroom memory aid. The interviews highlighted four changes:

- **Human connection first:** the professor should visibly learn names, rather than silently rely on AI.
- **Learning Mode:** identity cards should fade as the professor becomes familiar with students.
- **Meaningful consent:** opting out should be invisible and have no academic consequences.
- **Student-controlled profiles:** preferred names, pronunciation, and pronouns take priority over roster defaults.

The team also evaluated prompting behavior across **three AI tools and ten scenarios** (typical tasks, edge cases, and failure probes). Results informed safeguards against hallucinated details, uncertain identity, and prompt injection.

## Intended User Experience

- **High-confidence match:** show a compact card with a student's preferred name and relevant student-approved details.
- **Uncertain match:** ask the professor to verify before using the suggested identity.
- **Non-enrolled or unmatched face:** show no identity card and discard the frame.
- **Correction and dismissal:** allow the professor to reject or hide a card.
- **Learning Mode:** gradually reduce prompts to encourage genuine name recall.

The future glasses HUD is designed to use short peripheral cards to preserve eye contact. A future design goal is **under 1.2 seconds end-to-end**, including **under 200 ms for a cached card**; these are targets, not measured prototype performance.

## Privacy and Safety Principles

- Only recognize people who explicitly opt in.
- Do not infer identities for non-enrolled people.
- Do not link recognition to attendance or grading.
- Use a visible recording indicator and a clear consent process.
- Let students edit their own profile information and request deletion.
- Sanitize untrusted QR, badge, or other external text before passing it to an LLM.
- Verify applicable institutional and FERPA requirements before real classroom deployment.

## Prototype Scope and Limitations

This repository's `prototype/` directory contains prototype-related materials. The user-reported current prototype displays recognition results on the phone. The presentation documents **concept validation and the proposed in-glasses experience**, but does not specify a verified build command, Android package, face-recognition model, glasses SDK integration, or measured live recognition accuracy. Those details should be added after checking the actual source code and testing the demonstration.

Do not interpret conceptual storyboard images as evidence of completed hardware.

## Next Steps — Checkpoint 3

- Build an interactive recognition → card → correction/dismissal clickthrough.
- Integrate a supported glasses camera and validate the recognition pipeline with consenting test participants.
- Implement and test a name-and-description overlay **inside the glasses**, rather than only on the phone.
- Empirically calibrate the proposed 80% / 50% confidence boundaries.
- Interview professors and evaluate whether the interface supports natural interaction.
- Test privacy, opt-out, latency, and error-handling safeguards.

## Project Context

**Course:** IS 492  
**Project:** ContextLens  
**Milestone:** Checkpoint 2 — Prompt-Based Validation and Speed-Dating for Concept Design

This README is based on the Checkpoint 2 presentation. Implementation-specific instructions should be updated once the Android project and live demo have been verified.
