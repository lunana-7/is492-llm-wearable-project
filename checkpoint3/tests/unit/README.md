# Unit and component tests

**Owner — Min Kim coordinates.** Aman owns storage/recognition fixes, Steven owns UI/session fixes, and Neha owns prompt/schema behavior.

## Executable prompt checks

From `checkpoint3/`:

```sh
python3 -m pip install -r tests/unit/requirements-prompts.txt
python3 -m unittest discover -s tests/unit -p 'test_prompt_contract.py'
```

Four tests validate the output schema and fixtures, reject identity disclosure during uncertainty, reject fabricated deadlines and reject invalid response shapes. The optional live-model command is documented in [the prompt package](../../app/prompts/README.md).

## Android component checks

The [Android integration suite](../integration/README.md) executes actual roster, crypto, model and recognition-control methods. Android dependencies and Keystore require a device or emulator. It covers enrollment persistence, encrypted retrieval, known/unknown matching, threshold boundaries, deletion, clear-all, ciphertext tampering, idempotent stop and the bundled embedding model.

The original planned cases map to the new suite as follows.

| Planned coverage | Executable evidence or remaining step |
|---|---|
| Enrollment and matching | enrollmentPersistsEncryptedAndReloadsForRetrieval |
| Unknown input and threshold | unknownAndWrongDimensionReturnNoIdentity; thresholdBoundaryIsApplied |
| Individual and full deletion | deletedEntryStaysDeletedAfterReload; clearAllPersistsEmptyRoster |
| Encryption | enrollmentPersistsEncryptedAndReloadsForRetrieval; ciphertextTamperingIsRejectedByCrypto |
| Consent | Explicit enforced-consent behavior remains an implementation gap |
| Start/stop | stopIsIdempotentAndSignalsSessionOwner |
| Timeout and three-match streak | Device-dependent LiveRecognizer loop; manual M-01/M-02 |
| Display failures | Manual M-04/M-07 on compatible hardware |

See [the current results](../integration/RESULTS.md). Passing tests establish only the behavior each test exercises.

## Speech review and persistence

Min’s test_speech_workflow.py contains ten tests covering consent, mismatched approval, discard, transcript changes invalidating drafts, safe edit/save/delete, no-overwrite behavior, unsupported or sensitive summaries, invalid/truncated audio, instruction overrides and empty summaries. Run it with:

```sh
python3 -m unittest discover -s tests/unit -p 'test_speech_workflow.py'
```

Install app/speech/requirements.txt first. These tests exercise the production review and validation code. The real models are exercised separately by tests/integration/live_speech.py.
