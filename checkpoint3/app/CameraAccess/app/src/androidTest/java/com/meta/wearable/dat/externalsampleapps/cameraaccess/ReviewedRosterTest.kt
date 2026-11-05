package com.meta.wearable.dat.externalsampleapps.cameraaccess

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.meta.wearable.dat.externalsampleapps.cameraaccess.ui.RosterStore
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ReviewedRosterTest {
    @Test fun realDraftFromPairedHostReachesOnlyApprovedProfile() {
        org.junit.Assume.assumeTrue(InstrumentationRegistry.getArguments().getString("liveSpeech") == "true")
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val audio = instrumentation.context.assets.open("office-hours.wav").use { it.readBytes() }
        val context = instrumentation.targetContext
        val name = "Synthetic office hours " + java.util.UUID.randomUUID()
        val embedding = floatArrayOf(0f, 0f, 1f)
        try {
            RosterStore.enroll(context, name, "Original", embedding, true)
            val person = RosterStore.all(context).single { it.name == name }
            val draft = com.meta.wearable.dat.externalsampleapps.cameraaccess.ui.requestDraft(audio)
            assertTrue(draft.contains("office hours", ignoreCase = true))
            assertEquals("Original", person.cardText)
            assertTrue(RosterStore.setNote(context, person, draft))
            assertEquals(draft, RosterStore.match(context, embedding).first!!.cardText)
        } finally {
            RosterStore.delete(context, name)
        }
        assertNull(RosterStore.match(context, embedding).first)
    }

    @Test fun consentMatchApproveDeleteAndRejectStaleDraft() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val vector = floatArrayOf(1f, 0f)
        val name = "Synthetic CP3 " + java.util.UUID.randomUUID()
        try {
            try {
                RosterStore.enroll(context, name, "", vector, false)
                fail("Consent must be required")
            } catch (_: IllegalArgumentException) {}
            assertFalse(RosterStore.all(context).any { it.name == name })
            RosterStore.enroll(context, name, "Original", vector, true)
            val student = RosterStore.all(context).single { it.name == name }
            assertEquals(student, RosterStore.match(context, vector).first)
            assertNull(RosterStore.match(context, floatArrayOf(0f, 1f)).first)
            assertEquals("Original", student.cardText)
            assertTrue(RosterStore.setNote(context, student, "Bring chart"))
            assertEquals("Bring chart", RosterStore.match(context, vector).first!!.cardText)
            assertTrue(RosterStore.setNote(context, student, ""))
            assertEquals("Original", student.cardText)
            RosterStore.delete(context, name)
            assertNull(RosterStore.match(context, vector).first)
            RosterStore.enroll(context, name, "", vector, true)
            assertFalse(RosterStore.setNote(context, student, "Obsolete draft"))
        } finally {
            RosterStore.delete(context, name)
        }
    }
}
