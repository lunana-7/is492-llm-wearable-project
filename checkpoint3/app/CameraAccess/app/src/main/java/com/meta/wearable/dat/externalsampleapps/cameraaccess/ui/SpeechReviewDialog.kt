package com.meta.wearable.dat.externalsampleapps.cameraaccess.ui

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import kotlinx.coroutines.*

@Composable
internal fun SpeechReviewDialog(
    person: RosterStore.Person,
    capture: suspend () -> ByteArray = ::recordNote,
    close: () -> Unit,
) {
    val context = LocalContext.current
    val lifecycle = LocalLifecycleOwner.current.lifecycle
    val scope = rememberCoroutineScope()
    var stage by remember { mutableStateOf("consent") }
    var note by remember { mutableStateOf("") }
    var message by remember { mutableStateOf("") }
    val permission = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        message = if (granted) "Ready. Tap the consent button to record." else "Microphone permission is needed to record."
    }
    DisposableEffect(lifecycle) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_STOP) close()
        }
        lifecycle.addObserver(observer)
        onDispose { lifecycle.removeObserver(observer) }
    }
    AlertDialog(
        onDismissRequest = close,
        title = { Text("Follow-up for ${person.name}") },
        text = {
            Column {
                when (stage) {
                    "consent" -> Text("Hand the phone to the student. With everyone’s permission, record 8 seconds on the phone. The paired laptop transcribes it and selects a quote. You can edit or discard it before saving to this profile.")
                    "recording" -> Text("Recording for 8 seconds…")
                    "processing" -> Text("Preparing a draft on the paired laptop…")
                    "review" -> OutlinedTextField(value = note, onValueChange = { if (it.length <= 180) note = it },
                        label = { Text("Review before sharing on the recognition card") })
                }
                if (message.isNotEmpty()) Text(message)
            }
        },
        confirmButton = {
            when (stage) {
                "consent" -> TextButton(onClick = {
                    if (context.checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                        permission.launch(Manifest.permission.RECORD_AUDIO)
                    } else {
                        stage = "recording"
                        message = ""
                        scope.launch {
                            try {
                                val audio = withTimeout(12000) { withContext(Dispatchers.IO) { capture() } }
                                stage = "processing"
                                val result = withContext(Dispatchers.IO) { requestDraft(audio) }
                                if (result.isBlank()) {
                                    message = "No supported follow-up found. You can record again."
                                    stage = "consent"
                                } else {
                                    note = result
                                    stage = "review"
                                }
                            } catch (e: TimeoutCancellationException) {
                                message = "Microphone timed out. Try again."
                                stage = "consent"
                            } catch (e: CancellationException) { throw e }
                            catch (e: Exception) {
                                message = if (e is IllegalStateException && stage == "processing") e.message.orEmpty()
                                    else "Recording or inference unavailable. Check microphone and USB connection."
                                stage = "consent"
                            }
                        }
                    }
                }) { Text("I consent · Record") }
                "review" -> TextButton(enabled = note.isNotBlank(), onClick = {
                    if (RosterStore.setNote(context, person, note.trim())) close()
                    else message = "Profile unavailable. Discard this draft."
                }) { Text("Approve and save") }
            }
        },
        dismissButton = { TextButton(onClick = close) { Text("Discard") } }
    )
}
