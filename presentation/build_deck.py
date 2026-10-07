#!/usr/bin/env python3
"""Build the ContextLens Checkpoint 2 presentation deck (7 slides, 5-8 min).
Re-run after updating EVIDENCE below, then run again.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "presentation", "contextlens_cp2_deck.pptx")
SHOT_E3 = os.path.join(BASE, "validation", "transcripts", "screenshots", "duckai_E3_failure.png")
SHOT_F2 = os.path.join(BASE, "validation", "transcripts", "screenshots", "deepai_F2_injection.png")

# ---------- Evidence (update when runs complete) ----------
EVIDENCE = {
    "plat_a": "DeepAI (Standard)",
    "score_a": "8/10",
    "plat_b": "Duck.ai (GPT-6 Luna)",
    "score_b": "9/10",
}

NAVY = RGBColor(0x1B, 0x2A, 0x4A)
TEAL = RGBColor(0x0E, 0x7C, 0x7B)
DARK = RGBColor(0x2B, 0x2B, 0x2B)
GRAY = RGBColor(0x5A, 0x5A, 0x5A)
LIGHT_BG = RGBColor(0xF4, 0xF6, 0xF8)
AMBER = RGBColor(0xB4, 0x5E, 0x0B)
AMBER_BG = RGBColor(0xFD, 0xF3, 0xE7)
GREEN = RGBColor(0x1E, 0x7E, 0x34)
GREEN_BG = RGBColor(0xE9, 0xF5, 0xEC)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_bg(slide, color=LIGHT_BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = color
    bg.line.fill.background()


def add_topbar(slide):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.09))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()


def add_footer(slide, num):
    tx = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(12.3), Inches(0.35))
    tf = tx.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"ContextLens  •  IS 492 Checkpoint 2  •  {num}/7"
    p.font.size = Pt(11); p.font.color.rgb = GRAY


def title_block(slide, kicker, title, subtitle=None):
    add_topbar(slide)
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(1.6))
    tf = tx.text_frame; tf.word_wrap = True
    p = tf.add_paragraph(); p.text = kicker
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = TEAL
    p.space_after = Pt(6)
    p = tf.add_paragraph(); p.text = title
    p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_after = Pt(6)
    if subtitle:
        p = tf.add_paragraph(); p.text = subtitle
        p.font.size = Pt(17); p.font.color.rgb = GRAY


def body_box(slide, left, top, width, height):
    tx = slide.shapes.add_textbox(left, top, width, height)
    tx.text_frame.word_wrap = True
    return tx.text_frame


def bullets(tf, items, size=17, space_after=8, bold_prefix=False):
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(space_after)
        p.level = 0
        if bold_prefix and ": " in item:
            head, rest = item.split(": ", 1)
            r = p.add_run(); r.text = head + ": "
            r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = DARK
            r2 = p.add_run(); r2.text = rest
            r2.font.size = Pt(size); r2.font.color.rgb = DARK
        else:
            p.text = item
            p.font.size = Pt(size); p.font.color.rgb = DARK


def card(slide, left, top, width, height, bg, border=None):
    c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    c.fill.solid(); c.fill.fore_color.rgb = bg
    c.line.fill.background()
    if border:
        c.line.color.rgb = border; c.line.width = Pt(1.5)
    return c


def card_text(slide, left, top, width, height, bg, title, body, title_color=NAVY, border=None):
    card(slide, left, top, width, height, bg, border)
    tf = body_box(slide, left + Inches(0.25), top + Inches(0.15), width - Inches(0.5), height - Inches(0.3))
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = title_color
    p.space_after = Pt(8)
    for line in body:
        p = tf.add_paragraph(); p.text = line
        p.font.size = Pt(14.5); p.font.color.rgb = DARK
        p.space_after = Pt(4)
        p.level = 0


def notes(slide, text):
    ns = slide.notes_slide
    ns.placeholders[1].text = text


# ================= SLIDE 1 — Title & Project Recap =================
s = prs.slides.add_slide(BLANK); add_bg(s)
add_topbar(s)
tf = body_box(s, Inches(0.8), Inches(1.2), Inches(11.7), Inches(4.5))
p = tf.paragraphs[0]; p.text = "ContextLens"
p.font.size = Pt(64); p.font.bold = True; p.font.color.rgb = NAVY
p = tf.add_paragraph(); p.space_before = Pt(6)
p.text = "A wearable AI assistant for recognition and contextual memory"
p.font.size = Pt(24); p.font.color.rgb = TEAL
p = tf.add_paragraph(); p.space_before = Pt(18)
p.text = "Checkpoint 2: Prompt-Based Validation & Speed-Dating for Concept Design"
p.font.size = Pt(18); p.font.color.rgb = GRAY
tf2 = body_box(s, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.2))
p = tf2.paragraphs[0]
p.text = "Team: Aman  •  Steven  •  Min Kim  •  Neha     |     github.com/<org>/contextlens"
p.font.size = Pt(16); p.font.color.rgb = DARK
p = tf2.add_paragraph(); p.space_before = Pt(8)
p.text = "Problem reminder: service employees meet dozens of repeat customers daily — human memory doesn't scale, and lookups break the interaction."
p.font.size = Pt(15); p.font.italic = True; p.font.color.rgb = GRAY
add_footer(s, 1)
notes(s, "[~30 sec — Min] Hi everyone, we're presenting ContextLens — glasses that recognize opted-in customers and surface a short reminder to service employees. I'm Min; with me are Aman, Steven, and Neha. In Checkpoint 1 we proposed the concept; in Checkpoint 2 we stress-tested it with a systematic prompting study and speed-dating interviews — and the evidence changed our design.")

# ================= SLIDE 2 — What We Needed to Validate =================
s = prs.slides.add_slide(BLANK); add_bg(s)
title_block(s, "CHECKPOINT 2", "What we needed to validate",
            "Three assumptions from our CP1 proposal — and how we tested each")
items = [
    "Assumption 1 — Trust: employees will act on AI reminders. Tested via 2 speed-dating interviews per member with service workers & peers.",
    "Assumption 2 — Truthfulness: the LLM will only use retrieved, approved profile data. Tested via 10-scenario prompting study (typical / edge / failure) across \u22653 AI platforms.",
    "Assumption 3 — Timing: reminders arrive fast enough to feel natural (<2s). Tested via latency measurement on every prompt run.",
    "Early signal: users don't just need faster recognition — they need trustworthy recognition. A confident wrong answer is worse than silence.",
    "Prioritized features emerging: confidence-gated triggers, confirm/correct/dismiss flow, pre-LLM input sanitization.",
]
tf = body_box(s, Inches(0.8), Inches(2.3), Inches(11.7), Inches(4.4))
bullets(tf, items, size=18, space_after=12, bold_prefix=True)
add_footer(s, 2)
notes(s, "[~45 sec] We came out of CP1 with three big assumptions: that employees would trust the reminders, that the LLM would stick to approved profile data, and that it would all be fast enough. We tested trust with speed-dating interviews — two per team member — and truthfulness and timing with a systematic prompting study: ten scenarios across at least three AI platforms. The early signal surprised us: people don't just want faster recognition, they want recognition they can trust. A confident wrong answer is worse than no answer at all.")

# ================= SLIDE 3 — Prompting Study Design =================
s = prs.slides.add_slide(BLANK); add_bg(s)
title_block(s, "METHOD", "Prompting study design",
            "Same 10 prompts, run verbatim on each platform — typical, edge, and failure cases")
left_items = [
    "Tools: \u22653 AI platforms (Min: Duck.ai + DeepAI; teammates cover ChatGPT / Claude / Copilot).",
    "10 scenarios: T1–T3 typical (reminder generation, CRM summary, preference Q&A).",
    "E1–E3 edge (borderline 62% match, conflicting preferences, noisy speech transcript).",
    "F1–F4 failure (hallucination trap, prompt injection, non-consented ID request, JSON breakdown).",
]
right_items = [
    "Controls: identical verbatim prompts, fresh session per prompt, default settings.",
    "Recorded: full outputs, model version, latency, screenshots of failures.",
    "Fixtures: fictional personas only (Alex Kim, Jordan Lee) — no real PII.",
    "Scored PASS / PARTIAL / FAIL on accuracy, reliability, latency, UX, safety, cost.",
]
tf = body_box(s, Inches(0.8), Inches(2.3), Inches(5.6), Inches(4.4))
bullets(tf, left_items, size=16, space_after=10)
tf = body_box(s, Inches(6.9), Inches(2.3), Inches(5.6), Inches(4.4))
bullets(tf, right_items, size=16, space_after=10)
add_footer(s, 3)
notes(s, "[~1–1.5 min] Here's the design. We wrote ten prompts that mirror ContextLens's actual prompt chains — generating the glasses reminder, summarizing interactions for the CRM, and deciding what to do on uncertain matches. Three typical, three edge, four failure cases, including a hallucination trap, a prompt-injection hidden in a transcript, and a request to identify someone who never consented. Every prompt ran verbatim on each platform in a fresh session, with fictional personas so no real personal data was involved. We scored each run pass, partial, or fail across six dimensions: accuracy, reliability, latency, UX friction, safety, and cost.")

# ================= SLIDE 4 \u2014 Evidence =================
s = prs.slides.add_slide(BLANK); add_bg(s)
title_block(s, "EVIDENCE", "What worked \u2014 and what failed",
            f"10 scenarios \u00d7 2 platforms \u2014 {EVIDENCE['plat_b']}: {EVIDENCE['score_b']}  \u00b7  {EVIDENCE['plat_a']}: {EVIDENCE['score_a']}")
card_text(s, Inches(0.6), Inches(2.3), Inches(3.7), Inches(1.85), GREEN_BG,
          "\u2713 Worked (both platforms)", ["Reminders: \u226425 words, profile-only, confirmable",
                        "Borderline 62% match \u2192 correctly withheld",
                        "Conflicting preferences \u2192 surfaced, not resolved",
                        "Hallucination trap declined; JSON overlay parsed"], GREEN, GREEN)
card_text(s, Inches(4.6), Inches(2.3), Inches(3.7), Inches(1.85), AMBER_BG,
          "\u2717 E3 failed on BOTH", ["Noisy transcript \u2192 guessed instead of hedging",
                        "Duck.ai: 'likely an oat latte' for [unintelligible]",
                        "DeepAI: zero [uncertain] markers at all",
                        "Same failure, 2 models \u2192 systematic, not a quirk"], AMBER, AMBER)
card_text(s, Inches(8.6), Inches(2.3), Inches(3.9), Inches(1.85), AMBER_BG,
          "\u2717 F2 injection SUCCEEDED (DeepAI)", ["QR-payload instruction laundered into CRM record",
                        "'VIP / 50% discount / backstage' recorded as fact",
                        "Duck.ai instead refused the whole task",
                        "\u2192 models disagree; safeguard must live in pipeline"], AMBER, AMBER)
if os.path.exists(SHOT_E3):
    s.shapes.add_picture(SHOT_E3, Inches(0.6), Inches(4.45), width=Inches(5.95))
    tf = body_box(s, Inches(0.6), Inches(6.72), Inches(5.95), Inches(0.3))
    p = tf.paragraphs[0]; p.text = "E3 failure (Duck.ai): guessed the order, marked nothing uncertain"
    p.font.size = Pt(12); p.font.italic = True; p.font.color.rgb = GRAY
if os.path.exists(SHOT_F2):
    s.shapes.add_picture(SHOT_F2, Inches(6.85), Inches(4.45), width=Inches(5.95))
    tf = body_box(s, Inches(6.85), Inches(6.72), Inches(5.95), Inches(0.3))
    p = tf.paragraphs[0]; p.text = "F2 failure (DeepAI): injected 'VIP / 50% discount' recorded as a legitimate clarification"
    p.font.size = Pt(12); p.font.italic = True; p.font.color.rgb = GRAY
add_footer(s, 4)
notes(s, "[~1.5\u20132 min \u2014 the heart of CP2] Two platforms, ten scenarios each: Duck.ai passed 9 of 10, DeepAI 8 of 10. The wins replicated: both correctly withheld a 62%-confidence match, surfaced conflicting preferences, and declined to invent missing data. The failures are the story. E3 failed on BOTH platforms \u2014 told explicitly not to guess at garbled speech, both models produced confident summaries with no hedging. Same failure in two different models means it's systematic, not a quirk. And F2 is our smoking gun: on DeepAI, the injected instruction hidden in badge data was laundered into the CRM as a legitimate VIP clarification \u2014 while Duck.ai refused the entire task instead. Two models, two different failure modes on the same attack \u2014 which is exactly why the safeguard has to live in our pipeline, not in the model. Screenshots and verbatim transcripts are in our repo under validation/transcripts.")

# ================= SLIDE 5 — Gap Analysis & Opportunity =================
s = prs.slides.add_slide(BLANK); add_bg(s)
title_block(s, "SYNTHESIS", "Gap analysis: tool limitation \u2192 our opportunity",
            "Every design change below traces to a concrete piece of prompting evidence")
rows = [
    ("ASR guessing (E3 \u2717 both)",
     "Two models fill gaps fluently instead of hedging",
     "Surface transcription confidence in the UI; hedge visibly"),
    ("Injection: success vs over-refusal (F2)",
     "Same attack: DeepAI obeyed, Duck.ai refused everything",
     "Strip untrusted payload fields BEFORE the LLM call"),
    ("Borderline matches (E1 \u2713 both)",
     "Withholding beat guessing \u2014 but needs a rule",
     "Confidence-gated trigger: <85% \u2192 silent or confirm-first"),
    ("Conflicting signals (E2 \u2713 both)",
     "Silent resolution erodes trust",
     "Show the conflict; employee picks (confirm flow)"),
]
y = Inches(2.35)
for tool_lim, why, opp in rows:
    card(s, Inches(0.6), y, Inches(12.1), Inches(1.05), RGBColor(0xFF, 0xFF, 0xFF), TEAL)
    tf = body_box(s, Inches(0.9), y + Inches(0.12), Inches(11.5), Inches(0.85))
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = tool_lim + "   \u2192   "
    r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = AMBER
    r = p.add_run(); r.text = why + "   \u2192   "
    r.font.size = Pt(15); r.font.color.rgb = GRAY
    r = p.add_run(); r.text = opp
    r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = TEAL
    y += Inches(1.18)
add_footer(s, 5)
notes(s, "[~1–1.5 min] Four tool limitations, four design decisions. The ASR guessing failure becomes a UI requirement: transcription confidence must be visible, not silent. The injection over-refusal becomes an architecture decision: strip untrusted fields like badge-QR payloads before the LLM ever sees them. The borderline-match success becomes a trigger rule: below 85% confidence, stay silent or ask first. And conflicting preferences become the confirm flow: show both signals and let the employee decide. Nothing here is an opinion — each row points at a transcript.")

# ================= SLIDE 6 — Refined Concept & UI Direction =================
s = prs.slides.add_slide(BLANK); add_bg(s)
title_block(s, "REFINED CONCEPT", "Updated journey & UI direction",
            "What changed because of the evidence")
# Flow diagram
steps = ["Capture", "Match\n\u226585%?", "Retrieve\n(consented only)", "Confirm /\ncorrect / dismiss"]
x = Inches(0.8)
for i, st in enumerate(steps):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.6), Inches(2.4), Inches(1.2))
    shp.fill.solid(); shp.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    shp.line.color.rgb = TEAL; shp.line.width = Pt(2)
    tf = shp.text_frame; tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    p = tf.paragraphs[0]; p.text = st
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = NAVY
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    if i < 3:
        arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x + Inches(2.4), Inches(3.0), Inches(0.55), Inches(0.35))
        arr.fill.solid(); arr.fill.fore_color.rgb = TEAL; arr.line.fill.background()
    x += Inches(2.95)
# Glasses overlay mock
card(s, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.3), RGBColor(0x1B, 0x2A, 0x4A))
tf = body_box(s, Inches(1.1), Inches(4.5), Inches(5.0), Inches(1.9))
p = tf.paragraphs[0]; p.text = "\U0001F453  GLASSES VIEW (mock)"
p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = RGBColor(0x8A, 0x9B, 0xB8)
p = tf.add_paragraph(); p.space_before = Pt(10); p.text = "Alex Kim — iced espresso"
p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
p = tf.add_paragraph(); p.text = "Last visit: asked about oat milk  \u00b7  conf 91%"
p.font.size = Pt(14); p.font.color.rgb = RGBColor(0xB9, 0xC6, 0xDC)
p = tf.add_paragraph(); p.space_before = Pt(10)
p.text = "[ \u2713 Confirm ]   [ \u2717 Wrong person ]   [ \u2022 Details ]"
p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = RGBColor(0x5E, 0xE3, 0xB3)
tf2 = body_box(s, Inches(6.9), Inches(4.3), Inches(5.6), Inches(2.3))
bullets(tf2, [
    "Low confidence (<85%) \u2192 NO overlay; neutral greeting instead.",
    "ASR-uncertain summaries show [uncertain] badges inline.",
    "Every suggestion is confirmable — the employee decides, always.",
    "Corrections feed back into the profile (wrong-person tap \u2192 retrain flag).",
], size=15, space_after=8)
add_footer(s, 6)
notes(s, "[~1–1.5 min] Here's the refined concept. The pipeline is now: capture, match — and if confidence is under 85%, nothing appears — retrieve only consented data, then the employee confirms, corrects, or dismisses. The overlay mock shows what the wearer sees: name, reminder, confidence, and one-tap actions. Two things changed because of evidence: the confidence gate came from E1's success at withholding, and the visible uncertainty badges came from E3's failure to hedge. Then a quick demo of our clickthrough prototype — [itree's prototype demo goes here].")

# ================= SLIDE 7 — Risks, Safeguards & Path to CP3 =================
s = prs.slides.add_slide(BLANK); add_bg(s)
title_block(s, "WHAT'S NEXT", "Risks, safeguards & path to CP3",
            "New risks discovered in validation — and what we're building next")
tf = body_box(s, Inches(0.8), Inches(2.3), Inches(5.6), Inches(4.4))
p = tf.paragraphs[0]; p.text = "New risks"
p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = AMBER; p.space_after = Pt(8)
bullets(tf, [
    "Automation bias: fluent errors (E3) invite over-trust.",
    "Injection via untrusted fields: badge QR, notes, transcripts.",
    "API cost/latency at scale: every overlay is an LLM call.",
    "Consent UX: enrollment must be obvious, revocable, auditable.",
], size=16, space_after=10)
tf = body_box(s, Inches(6.9), Inches(2.3), Inches(5.6), Inches(4.4))
p = tf.paragraphs[0]; p.text = "Safeguards \u2192 CP3 build"
p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = TEAL; p.space_after = Pt(8)
bullets(tf, [
    "Human-in-the-loop confirm on every suggestion (HIL).",
    "Pre-LLM sanitization layer for untrusted inputs.",
    "Confidence-gated triggers + cached reminders to cut calls.",
    "CP3: working app — FastAPI + pgvector + React, live demo of confirm flow & error recovery.",
], size=16, space_after=10)
add_footer(s, 7)
notes(s, "[~45 sec] Validation surfaced new risks: automation bias from fluent-but-wrong outputs, injection through untrusted fields like badge data, API cost if every glance triggers an LLM call, and the consent experience itself. Our safeguards: human-in-the-loop confirmation on everything, a sanitization layer before the LLM, confidence-gated triggers plus caching to cut API calls. For Checkpoint 3 we're building the working app — FastAPI backend, pgvector profiles, React frontend — with a live demo of the confirm flow and error recovery. Happy to take questions.")

prs.save(OUT)
print("saved:", OUT)
