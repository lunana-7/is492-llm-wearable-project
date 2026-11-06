# ContextLens prompt package

**Owner — Neha Manishankar.** This package turns the system-prompt draft into versioned files for integration and evaluation.

| File | Purpose |
|---|---|
| system_prompt.txt | Preserves the classroom memory assistant rules from the uploaded draft |
| input_contract.txt | Input precedence and deterministic fixture rendering used by the evaluator |
| output_schema.json | Required JSON output and permitted status/reason values |
| model_settings.json | Local evaluation model, generation settings and proposed confidence policy |
| few_shot_examples.json | Synthetic demonstrations of approved, missing, uncertain and hostile fields |
| regression_cases.json | Eleven synthetic input/output cases for evaluation |

## Integration contract

The caller supplies `consent` (active/missing/revoked), `confidence_percent` (0–100), `hud_state` (visible/hidden/standby), a `profile` object, an `approved_fields` array and `profile_conflict` (boolean). Send only approved fields to the model in the eventual application. The hostile-field fixture intentionally probes behavior if filtering fails.

Combine system_prompt.txt and input_contract.txt into the system message. Add the few-shot examples as paired user JSON and assistant JSON messages. Put the actual structured input in a separate user message. Supply the output schema as the model's structured-output format. Validate the result against the schema, count fewer than ten whitespace-separated cue words, and check that displayed information comes from approved fields. Reject unsafe or malformed results with an empty cue. Consent, field access and display gating also belong in application code.

The Android source currently performs TFLite matching and renders roster text directly. Its 0.60 similarity threshold and three-match streak are separate from this prompt's proposed 80/50 percent policy. A similarity score must not be presented as a calibrated probability. The application needs an explicit integration and calibration decision before using these settings.

## Run the evaluation

From `checkpoint3/`:

```sh
python3 -m pip install -r tests/unit/requirements-prompts.txt
python3 -m unittest discover -s tests/unit -p 'test_prompt_contract.py'
python3 tests/unit/test_prompt_contract.py --live
```

The live command requires a running local Ollama server with `qwen3:8b` downloaded. Set `CP3_OLLAMA_PORT` for a different local port. It runs the eleven fixtures through the model, validates the response schema and compares status/cue against the expected result. It prints a result for every case and exits unsuccessfully if any case fails. Passing fixtures measure this prompt evaluation only. They do not establish Android integration or general injection resistance.

## Verification on November 5, 2026

Four contract tests passed. All eleven fixtures also passed with the actual local qwen3:8b model through Ollama, using the system prompt plus input contract and the included few-shot examples. The model settings and fixtures are reproducible inputs. These eleven outcomes are a small synthetic evaluation, with no claim about broader robustness or device performance.
