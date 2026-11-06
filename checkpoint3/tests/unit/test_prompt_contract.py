"""Neha's prompt regression checks, with an explicit opt-in live model run."""
import json
import os
from pathlib import Path
import re
import sys
import unittest
from urllib.request import ProxyHandler, Request, build_opener
from jsonschema import Draft202012Validator

PROMPTS = Path(__file__).resolve().parents[2] / "app/prompts"
SCHEMA = json.loads((PROMPTS / "output_schema.json").read_text())
CASES = json.loads((PROMPTS / "regression_cases.json").read_text())
SETTINGS = json.loads((PROMPTS / "model_settings.json").read_text())


def words(text):
    return re.findall(r"\w+", text.casefold())


def validate(case, output):
    Draft202012Validator(SCHEMA).validate(output)
    if len(output["cue"].split()) >= 10:
        raise ValueError("Cue exceeds nine words")
    if output["status"] != case["expected"]["status"]:
        raise ValueError("Unexpected display decision")
    if words(output["cue"]) != words(case["expected"]["cue"]):
        raise ValueError("Cue leaked or invented information, or omitted required approved fields")


class Contract(unittest.TestCase):
    def test_schema_and_fixtures(self):
        Draft202012Validator.check_schema(SCHEMA)
        for case in CASES:
            with self.subTest(case=case["id"]):
                validate(case, case["expected"])

    def test_rejects_leaked_identity(self):
        with self.assertRaises(ValueError):
            validate(CASES[4], {"status": "verify", "cue": "Verify student?", "reason": "uncertain"} | {"status": "display", "cue": "Priya"})

    def test_rejects_invented_deadline(self):
        with self.assertRaises(ValueError):
            validate(CASES[-1], {"status": "display", "cue": "Priya Friday deadline", "reason": "approved"})

    def test_rejects_wrong_shape(self):
        from jsonschema.exceptions import ValidationError
        for output in ({"status": "hidden"}, {"status": "hidden", "cue": "Priya", "reason": "no_consent"},
                       {"status": "hidden", "cue": "", "reason": "no_consent", "name": "Priya"}):
            with self.assertRaises(ValidationError):
                Draft202012Validator(SCHEMA).validate(output)


def live():
    policy = (PROMPTS / "input_contract.txt").read_text()
    messages = [{"role": "system", "content": (PROMPTS / "system_prompt.txt").read_text() + "\n" + policy}]
    for example in json.loads((PROMPTS / "few_shot_examples.json").read_text()):
        messages += [{"role": "user", "content": json.dumps(example["input"])},
                     {"role": "assistant", "content": json.dumps(example["expected"])}]
    client = build_opener(ProxyHandler({}))
    failures = []
    for case in CASES:
        body = {"model": SETTINGS["model"], "think": SETTINGS["think"], "stream": False,
                "format": SCHEMA, "options": {"temperature": 0, "num_predict": SETTINGS["num_predict"]},
                "messages": messages + [{"role": "user", "content": json.dumps(case["input"])}]}
        request = Request(f"http://127.0.0.1:{int(os.getenv('CP3_OLLAMA_PORT', '11434'))}/api/chat",
                          data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        try:
            with client.open(request, timeout=SETTINGS["timeout_seconds"]) as response:
                output = json.loads(json.load(response)["message"]["content"])
            validate(case, output)
            print("PASS", case["id"], flush=True)
        except Exception as exc:
            failures.append(case["id"])
            print("FAIL", case["id"], type(exc).__name__, flush=True)
    if failures:
        raise SystemExit(f"{len(failures)} cases failed")
    print(f"All {len(CASES)} live prompt cases passed")


if __name__ == "__main__":
    if "--live" in sys.argv:
        live()
    else:
        unittest.main()
