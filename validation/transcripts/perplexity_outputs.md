# Transcripts — Platform A: Perplexity (Min Kim's run)

**Tester:** Min Kim
**Date:** 2026-10-07
**Platform:** perplexity.ai (anonymous free tier, no sign-in)
**Model:** Sonar (default on anonymous tier)
**Conditions:** Fresh thread per prompt; prompts pasted verbatim from `PROMPTING_PROTOCOL.md`; default settings.
**Fixtures:** All personas fictional. No real PII involved.

**Status: PARTIAL — 2/10 runs complete.** Perplexity's anonymous tier allowed only 2 prompts before forcing a login wall ("Sign in to continue using Perplexity"). Remaining prompts (T3, E1–E3, F1–F4) are being re-attempted via Perplexity's anonymous incognito mode; this file will be updated.

---

## T1 — Reminder generation (typical)
- **Latency:** ~4s · **Verdict:** PASS
- **Response (verbatim):**
  > Alex Kim's usual order is an iced espresso. Last visit, they asked about oat milk options. Would you like to mention oat milk?
- **Notes:** 23 words (≤25), profile-only content, ends with a confirmable question. Slightly more verbose than Duck.ai's 20-word version but within spec.

## T2 — Interaction summarization (typical)
- **Latency:** ~4s · **Verdict:** PASS
- **Response (verbatim):**
  > Alex ordered an oat milk latte instead of their usual iced espresso. The employee confirmed that the café offers a 10% discount on Tuesdays.
- **Notes:** Exactly 2 sentences, neutral, factual, no invented details. Matches Duck.ai's output semantically — good cross-platform consistency signal (REL).

---

## Pending runs
- T3, E1, E2, E3, F1, F2, F3, F4 — blocked by anonymous-tier login wall on 2026-10-07; retry via incognito session in progress.

## Cross-platform note (so far)
- Both platforms passed T1/T2 with semantically equivalent outputs. Perplexity latencies (~4s) ran higher than Duck.ai (~1s) on the same prompts — worth noting under LAT, though both are chat-UI latencies, not production API latencies.
