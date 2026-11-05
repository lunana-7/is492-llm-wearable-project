# app/prompts

**Owner / assignment:** Neha Manishankar — versioned system prompts, few-shot examples, model settings and output schemas. Min integrates these into real inference.

The [speech summary prompt](speech-summary-v1.txt) ships with Min’s debug speech flow. The service uses local qwen3:8b, temperature 0 and JSON output containing one string, `quote`. Empty output means abstain. The service validates the selected quote against the redacted transcript. Neha owns further prompt cases and evaluation.
