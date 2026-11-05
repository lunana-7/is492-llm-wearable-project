# Run Min’s speech and summary demo

Use a trusted laptop, a debug build of CameraAccess and a USB-connected Android device. Recognition can run independently. The speech demo uses the phone microphone. Audio travels through a USB tunnel to the laptop, where Whisper transcribes it and Qwen selects a short follow-up quote. Only the reviewed text returns to the roster after the student approves it on the phone.

From the repository root, prepare the laptop with Python 3.12 and Ollama installed. First-time setup downloads both local models. Allow several GB of free space for Qwen.

```sh
cd checkpoint3
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r app/speech/requirements.txt
ollama serve                         # leave running in its own terminal if needed
```

In another terminal, from `checkpoint3/`:

```sh
ollama pull qwen3:8b
.venv/bin/python app/speech/server.py
```

In a third terminal, with the debug APK installed and the phone connected:

```sh
adb reverse tcp:8765 tcp:8765
.venv/bin/python tests/integration/live_speech.py
```

The last command runs the supplied synthetic recording through both models and checks for “chart” and “office hours”. If Ollama runs on a different loopback port, set `CP3_OLLAMA_PORT` before starting the service. Keep the model server local and use the specified local model.

1. Enroll one consenting participant using the photo preview. Open **Roster → Record follow-up** under their name. Hand the phone to that participant and confirm the selected name.
2. Obtain consent from everyone who will speak. Tap **I consent · Record** and grant microphone permission if prompted. Say “I will bring the revised water quality chart to office hours” during the eight-second recording.
3. Read the draft. Edit the wording and tap **Approve and save**, or **Discard**. An approved follow-up is shown in place of the description on the next matched card. Removing the note restores the description.
4. For the recovery demo, disconnect the tunnel, record a new draft and observe the retry message. The previous approved note stays intact. Restore the tunnel, record again, then remove the follow-up or delete the profile.

Run automated checks from `checkpoint3/`:

```sh
.venv/bin/python -m unittest discover -s tests/unit
.venv/bin/python -m unittest discover -s tests/integration
cd app/CameraAccess
bash gradlew :app:connectedDebugAndroidTest \
  -Pandroid.testInstrumentationRunnerArguments.class=com.meta.wearable.dat.externalsampleapps.cameraaccess.ReviewedRosterTest,com.meta.wearable.dat.externalsampleapps.cameraaccess.SpeechReviewUiTest \
  -Pandroid.testInstrumentationRunnerArguments.liveSpeech=true
```

Use a dedicated test device/emulator for the instrumented checks. The live instrumentation case also requires the running service and `adb reverse`. Remove the tunnel with `adb reverse --remove tcp:8765` after the demo.
