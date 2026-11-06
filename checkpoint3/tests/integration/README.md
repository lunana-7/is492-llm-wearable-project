# Critical-path integration tests

**Owner — Min Kim.** Component owners resolve failures in their implementation.

## Automated Android suite

[MinSafetyIntegrationTest.kt](android/MinSafetyIntegrationTest.kt) calls the existing CameraAccess classes on Android. The opt-in Gradle init script includes these tests from this directory. It changes the test source set for this invocation.

Use a dedicated emulator or test device, JDK 17 and the Android SDK described in INSTALL.md. From `checkpoint3/app/CameraAccess/`:

```sh
bash gradlew -I ../../tests/integration/with-tests.gradle :app:connectedDebugAndroidTest \
  -Pandroid.testInstrumentationRunnerArguments.class=com.meta.wearable.dat.externalsampleapps.cameraaccess.MinSafetyIntegrationTest
```

On Windows, use `gradlew.bat` with the same arguments. Select a device with `ANDROID_SERIAL` if multiple devices are connected.

| Test method | Verified behavior |
|---|---|
| enrollmentPersistsEncryptedAndReloadsForRetrieval | Name/description/embedding persistence, encrypted serialization, object reload and matched description |
| unknownAndWrongDimensionReturnNoIdentity | Empty roster, orthogonal input and incompatible embedding dimensions |
| thresholdBoundaryIsApplied | Rejection below 0.60 and acceptance at 0.60 |
| deletedEntryStaysDeletedAfterReload | Individual deletion, remaining-profile preservation and no subsequent deleted-profile match |
| clearAllPersistsEmptyRoster | Clearing and reloading an empty roster |
| ciphertextTamperingIsRejectedByCrypto | AES-GCM rejects modified ciphertext |
| stopIsIdempotentAndSignalsSessionOwner | Start/stop state and a single callback for repeated stops |
| bundledEmbeddingModelRunsOnSyntheticPixels | Actual bundled TFLite execution, finite normalized embedding and small-crop rejection |

Tests use a test-specific SharedPreferences namespace and synthetic input. Test-only reflection clears the roster singleton between checks, so rerun this suite in a dedicated instrumentation process. Object reload exercises decoding from SharedPreferences; a cold process restart remains a separate device check. The encryption test uses the application's Keystore helper.

Results and environment are recorded in [RESULTS.md](RESULTS.md).

## Manual checks

Record actual outcomes, including failures, against the [use-case walkthroughs](../../docs/use-cases.md).

| ID | Procedure | Required safety outcome | Current evidence |
|---|---|---|---|
| M-01 | Enroll a consenting participant, then start live recognition | Correct identity after three valid matching observations | Hardware run required |
| M-02 | Show an unknown person for a fresh session | No enrolled identity, then stop after about 30 seconds | Matching unit boundary covered; timer/lens pending |
| M-03 | Delete an entry and restart recognition | Deleted identity never appears again | Storage/matching automated; lens pending |
| M-04 | End session or disconnect while a name is visible | Processing stops and stale identity clears | Stop callback automated; device behavior pending |
| M-05 | Successful enrollment photo, followed by empty or group photo | Failed/ambiguous capture cannot reuse earlier face | Known source risk; owner fix and device check required |
| M-06 | Attempt enrollment without explicit consent | Enforced refusal | Implementation gap; reminder is currently the only UI control |
| M-07 | Force crop/frame failure after a valid candidate | Streak resets and old identity clears | Source-review concern; device check required |
| M-08 | Close video preview and inspect local cache, then inspect a shared photo | Retention matches the documented behavior | Device/storage audit required |
| M-09 | Feed malformed/legacy roster data in an isolated test build | Safe error and no unauthorized identity | Loader-hardening work remains |
| M-10 | Attempt summary save without student approval and simulate service outage | Save blocked, controlled retry | Pending speech/summary integration |

For every trial, record commit, date, device/firmware, synthetic trial ID, steps, expected result, actual result, pass/fail and issue owner. The automated suite covers available methods. Missing safeguards remain open requirements.
