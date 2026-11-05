# Unit Tests — CameraAccess (Checkpoint 3)

**Owner / Assignment:** Min Kim coordinates testing; Aman Joshi is responsible for recognition, local student data storage, consent and deletion tests; Steven handles UI and session-state tests; Neha handles prompt and schema regression tests.

## Overview

CameraAccess is an Android application that uses Meta AI glasses, ML Kit face detection, TensorFlow Lite face embeddings, and encrypted local student records.

The application currently performs recognition and student storage locally, so a separate backend or SQL database is not required for these unit tests.

## Test Cases

| Test ID | Test Case | Expected Result |
|---|---|---|
| UT-01 | Enroll a student | Student profile and face embedding are saved successfully |
| UT-02 | Recognize an enrolled student | Matching student is identified when the similarity threshold is satisfied |
| UT-03 | Recognize an unknown person | No enrolled student name is returned |
| UT-04 | Test recognition threshold | Matches below the configured threshold are rejected |
| UT-05 | Delete a student profile | Student record and associated embedding are removed from local storage |
| UT-06 | Clear all student profiles | All locally stored roster records are deleted |
| UT-07 | Test encrypted storage | Student records are encrypted before persistence |
| UT-08 | Test consent requirement | Enrollment without consent should be blocked by the enrollment gate |
| UT-09 | Start and stop recognition | Recognition state changes correctly through phone controls |
| UT-10 | Test recognition timeout | Recognition stops after the configured timeout |
| UT-11 | Test consecutive matches | A student name is displayed only after three consecutive matching observations |
| UT-12 | Test display errors | The application handles glasses display failures without crashing |

## Testing Framework

- JUnit for Kotlin unit tests.
- AndroidX Test for Android-specific behavior.
- MockK or Mockito for mocking external dependencies, where configured.
- Android Studio and Gradle for executing tests.

## Running Tests

From `checkpoint3/app/CameraAccess/`:

```bash
# Windows
gradlew.bat :app:testDebugUnitTest

# macOS / Linux
./gradlew :app:testDebugUnitTest
```

Android instrumentation tests, if implemented, can be executed using:

```bash
./gradlew :app:connectedDebugAndroidTest
```

A connected Android device or emulator is required for instrumentation tests.

## Current Status

The test cases above define the planned coverage. They are **not claims that automated tests have already been implemented or passed**.

The Android roster tests now exercise consent enforcement and the reviewed-note lifecycle. Hardware-dependent behavior, including the name appearing on Meta glasses, must be verified through integration testing on compatible hardware.

## Checkpoint 3 Testing Goal

Verify that student enrollment, face recognition, local data protection, profile deletion and recognition-session management behave correctly, including unknown-person and error scenarios.

Record actual test results before the final Checkpoint 3 submission.

Min’s speech unit tests, HTTP integration tests and Android roster tests now have executable commands in the [speech guide](../../app/speech/README.md). The enrollment UI and storage call enforce explicit consent. The table above records the broader test plan.
