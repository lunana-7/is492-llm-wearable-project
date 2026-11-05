package com.meta.wearable.dat.externalsampleapps.cameraaccess

import android.Manifest
import androidx.compose.runtime.*
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.test.platform.app.InstrumentationRegistry
import com.meta.wearable.dat.externalsampleapps.cameraaccess.ui.*
import org.junit.*
import java.util.UUID

class SpeechReviewUiTest {
    @get:Rule val rule = createComposeRule()

    @Test fun studentCanDiscardThenEditAndApprove() {
        Assume.assumeTrue(InstrumentationRegistry.getArguments().getString("liveSpeech") == "true")
        val instrument = InstrumentationRegistry.getInstrumentation()
        val context = instrument.targetContext
        instrument.uiAutomation.grantRuntimePermission(context.packageName, Manifest.permission.RECORD_AUDIO)
        val name = "Synthetic UI " + UUID.randomUUID()
        try {
            RosterStore.enroll(context, name, "Original", floatArrayOf(1f, 0f, 0f), true)
            val student = RosterStore.all(context).single { it.name == name }
            val clip = instrument.context.assets.open("office-hours.wav").use { it.readBytes() }
            rule.setContent {
                    var open by remember { mutableStateOf(true) }
                    if (open) SpeechReviewDialog(student, capture = { clip }) { open = false }
                    else androidx.compose.material3.TextButton(onClick = { open = true }) {
                        androidx.compose.material3.Text("Another follow-up")
                    }
            }
            fun recordAndWait() {
                rule.onNodeWithText("I consent · Record").performClick()
                rule.waitUntil(110000) {
                    rule.onAllNodesWithText("Approve and save").fetchSemanticsNodes().isNotEmpty()
                }
            }
            recordAndWait()
            rule.onNodeWithText("Discard").performClick()
            rule.runOnIdle { Assert.assertEquals("Original", student.cardText) }
            rule.onNodeWithText("Another follow-up").performClick()
            recordAndWait()
            rule.onNode(hasSetTextAction()).performTextReplacement("Bring the chart")
            rule.onNodeWithText("Approve and save").performClick()
            rule.runOnIdle { Assert.assertEquals("Bring the chart", student.cardText) }
        } finally {
            RosterStore.delete(context, name)
        }
    }
}
