# Critical paths

Run the [speech guide’s test commands](../../app/speech/README.md). The HTTP suite injects model errors to exercise consent, invalid input, busy responses and retries. The live CLI and opt-in Android test use both real models. The Android roster test covers consent, known/unknown matches, approved context retrieval, note removal, deletion and rejection of drafts for deleted identities. Physical capture and lens behavior require the [team’s hardware checks](../../docs/checkpoint-review.md).
