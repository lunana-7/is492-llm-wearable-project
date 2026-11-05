# Safety and privacy · Min Kim

Ask everyone who will speak before recording. The CLI waits for explicit consent before accessing the microphone or sending audio. Use the synthetic fixture for repeatable testing. The service checks the consent header before inference; this is a demo control on a trusted laptop, not identity authentication.

The microphone clip is eight seconds. The service validates mono PCM16 WAV, sample rate and duration, rejects requests from browser origins, and allows one inference at a time. Whisper and Qwen run locally. The service keeps audio and transcript in memory and logs model timing and token counts. Email addresses and common digit-based phone numbers are redacted before summarization. Names and spoken numbers can still pass through.

Qwen selects an exact quote from the redacted transcript. The validator rejects unsupported text and some explicit instruction overrides. ASR errors and misleading excerpts can still occur. The student reviews and can edit or discard the draft. Only explicit approval writes the final text to a new owner-only file. It is plaintext on the laptop, so use synthetic or explicitly consented demo material and delete the file after rehearsal. The service never transmits roster data or writes the follow-up to the team’s app.

See the [test commands](../README.md#verify). For a failure demonstration, stop the model service, attempt a new draft, verify no output file was created, then restart and retry.
