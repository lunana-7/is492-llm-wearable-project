# CameraAccess — Installation and Running (Checkpoint 3)

## Project location

This Android project is at `checkpoint3/app/CameraAccess/`. Open **that directory** as the Android Studio project root, not the surrounding `checkpoint3/app/` directory.

The project is a Kotlin/Jetpack Compose Android application using the Meta Wearables Device Access Toolkit, ML Kit face detection, and a bundled TensorFlow Lite face-embedding model. The current application stores its enrolled roster locally on the phone; recognition runs independently of the optional laptop service. For the CP3 speech demo, also complete [speech setup and USB pairing](speech/README.md).

## Requirements

- Android Studio Narwhal (2025.1.1) or newer (as specified by the source README).
- JDK 17 or newer.
- Android SDK Platform 36, installed through Android Studio's SDK Manager.
- Android device or emulator running Android 12 / API 31 or newer.
- Internet access on first build to resolve Gradle/Maven dependencies.
- For physical-glasses testing: compatible Meta AI glasses, the companion Meta AI app, supported firmware, and Developer Mode enabled. Emulator-only testing does not prove glasses-display functionality.
- Meta Wearables developer application ID and client token if required by your device-registration setup.

The Gradle wrapper declares Gradle **8.14.1**. The Android application uses `compileSdk = 36`, `minSdk = 31`, `targetSdk = 36` and Java/Kotlin target 17.

## Clone and open

```bash
git clone https://github.com/lunana-7/is492-llm-wearable-project.git
cd is492-llm-wearable-project/checkpoint3/app/CameraAccess
```

In Android Studio, select **File → Open** and choose the `CameraAccess` directory. Allow Gradle synchronization to finish. Install missing SDK components if prompted.

## Local configuration

Create `CameraAccess/local.properties` on your own computer (do **not** commit it). Example:

```properties
sdk.dir=C:\\Users\\YOUR_USER\\AppData\\Local\\Android\\Sdk
mwdat_application_id=YOUR_META_APP_ID
mwdat_client_token=YOUR_META_CLIENT_TOKEN
```

On macOS/Linux, use your actual SDK path (for example `/Users/YOU/Library/Android/sdk` or `/home/YOU/Android/Sdk`). Android Studio may create `sdk.dir` automatically. The two `mwdat_*` names are read by `CameraAccess/app/build.gradle.kts` and inserted into Android manifest placeholders; they are **not** automatically read from `.env.example`.

`checkpoint3/app/.env.example` documents these configuration names only. Copying it to `.env` will not configure this Android build. Never commit a real token or your local.properties.

## Build commands

From `checkpoint3/app/CameraAccess/`:

**Windows PowerShell**

```powershell
.\gradlew.bat :app:assembleDebug
.\gradlew.bat :app:testDebugUnitTest
```

**macOS/Linux**

```bash
./gradlew :app:assembleDebug
./gradlew :app:testDebugUnitTest
```

If the repository does not contain the Gradle wrapper JAR or scripts, use Android Studio's Gradle build UI or restore the missing wrapper files from the original project; do not invent or download arbitrary wrapper binaries.

Build output, when successful: `app/build/outputs/apk/debug/app-debug.apk`.

## Run

1. Start a compatible Android device/emulator and grant permissions when requested.
2. In Android Studio, select the `app` run configuration and press **Run**.
3. On a physical glasses setup, enable Developer Mode in the Meta AI companion app.
4. Launch CameraAccess and use **Connect** to complete the device registration flow.
5. Tap **Start Session**, then **Preview** to stream camera frames.
6. Enroll a consenting test person using the app's enrollment UI, entering a name and optional approved description and capturing a usable face sample.
7. Start recognition using the **phone controls**. When a face matches the locally stored roster, the app attempts to display the name and description on the glasses.
8. Stop recognition/preview and end the session from the phone.

Do not describe voice invocation as working until verified on hardware. The current source contains a `VoiceTrigger` state holder, but that alone does not establish a functioning Meta voice integration.

## Recognition behavior in current source

- ML Kit locates faces; TensorFlow Lite produces face embeddings.
- `RosterStore.match()` compares embeddings against an encrypted local roster.
- The similarity threshold defaults to **0.60** and is explicitly a provisional value, not a validated accuracy guarantee.
- `LiveRecognizer` requires **three consecutive matching observations** before displaying a name.
- `RecognitionControl` stops recognition after **30 seconds without a match**, or **8 seconds after a name is displayed**.
- The source does not enforce an exact physical distance such as 1–1.5 meters; test that range rather than claiming it is guaranteed.

## Basic manual smoke tests

1. **Empty roster:** open the roster and confirm it is empty; unknown faces must not display a student's name.
2. **Enrollment:** enroll one consenting test participant and verify roster count increases.
3. **Recognition:** run preview and recognition, observe matching status and lens output on actual glasses.
4. **Unknown face:** show a non-enrolled participant; verify no enrolled name is displayed.
5. **Delete:** delete the enrolled person, then repeat recognition and verify their name is no longer matched.
6. **Stop:** end the session from the phone and verify the app stops sending recognition results.

Record observed results and device versions; the presence of these instructions is not evidence that each test has passed.

## Debugging

View Android logs in **Android Studio → Logcat**. Useful existing tags include `FaceEmbedder` and `DisplayHelper`. Example with Android SDK platform-tools:

```bash
adb logcat -s FaceEmbedder:D DisplayHelper:D AndroidRuntime:E '*:S'
```

This command filters selected tags and is **not** a complete telemetry pipeline. For more detail, remove the filters locally. Avoid sharing logs containing identifiable names, descriptions, face data or credentials.

- **Gradle sync fails:** verify JDK 17, SDK 36, network access, Gradle wrapper files, and Maven repository availability.
- **No device detected:** check Bluetooth, the companion app, Developer Mode, device registration and required permissions.
- **No glasses output:** verify the device session started and the display attachment succeeded; inspect `DisplayHelper` logs.
- **No recognition:** check roster enrollment, camera frames, lighting, face crop, and model asset `app/src/main/assets/face_model.tflite`.
- **Recognition errors:** collect non-sensitive stack traces and reproduce with a consented test participant.
- **Voice command unavailable:** use phone controls; do not claim voice control is supported until confirmed.

## Repository hygiene

Do not commit `.gradle/`, `.idea/`, `.kotlin/`, `build/`, `app/build/`, `local.properties`, secrets, private student photos, or student roster exports. Preserve the bundled `.tflite` model and necessary Gradle configuration. Keep the sibling `checkpoint3/app/meta-wearables-dat-android-main/` unchanged.

## Scope and limitations

Recognition runs on the phone. The debug roster’s **Record follow-up** action calls Whisper and Ollama over a USB tunnel. See the [speech demo](speech/README.md) for exact commands and the [checkpoint review](../docs/checkpoint-review.md) for verification and remaining hardware checks.
