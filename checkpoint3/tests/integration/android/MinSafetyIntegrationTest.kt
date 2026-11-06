package com.meta.wearable.dat.externalsampleapps.cameraaccess

import android.content.Context
import android.content.ContextWrapper
import android.content.SharedPreferences
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Rect
import android.util.Base64
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.meta.wearable.dat.externalsampleapps.cameraaccess.ui.*
import org.json.JSONArray
import org.junit.*
import org.junit.runner.RunWith

/** Test-only preference namespace; production roster files are never cleared. */
@RunWith(AndroidJUnit4::class)
class MinSafetyIntegrationTest {
    private lateinit var context: Context
    private var originalThreshold = 0.60f

    private fun forgetMemory() {
        val people = RosterStore::class.java.getDeclaredField("people").apply { isAccessible = true }
        (people.get(RosterStore) as MutableList<*>).clear()
        RosterStore::class.java.getDeclaredField("loaded").apply { isAccessible = true }
            .setBoolean(RosterStore, false)
    }

    @Before fun setup() {
        val target = InstrumentationRegistry.getInstrumentation().targetContext
        context = object : ContextWrapper(target) {
            override fun getSharedPreferences(name: String, mode: Int): SharedPreferences =
                super.getSharedPreferences("min_cp3_test_" + name, mode)
        }
        context.getSharedPreferences("roster", Context.MODE_PRIVATE).edit().clear().commit()
        forgetMemory()
        originalThreshold = RosterStore.threshold
        RosterStore.threshold = 0.60f
        RecognitionControl.onStop = null
        RecognitionControl.stop()
    }

    @After fun cleanup() {
        context.getSharedPreferences("roster", Context.MODE_PRIVATE).edit().clear().commit()
        forgetMemory()
        RosterStore.threshold = originalThreshold
        RecognitionControl.onStop = null
        RecognitionControl.stop()
    }

    @Test fun enrollmentPersistsEncryptedAndReloadsForRetrieval() {
        RosterStore.enroll(context, "Synthetic A", "Chart discussion", floatArrayOf(1f, 0f))
        val stored = context.getSharedPreferences("roster", 0).getString("data", null)!!
        Assert.assertFalse(stored.contains("Synthetic A"))
        val decoded = JSONArray(RosterCrypto.decrypt(stored))
        Assert.assertEquals("Chart discussion", decoded.getJSONObject(0).getString("description"))
        forgetMemory()
        val match = RosterStore.match(context, floatArrayOf(1f, 0f)).first!!
        Assert.assertEquals("Synthetic A", match.name)
        Assert.assertEquals("Chart discussion", match.description)
    }

    @Test fun unknownAndWrongDimensionReturnNoIdentity() {
        Assert.assertNull(RosterStore.match(context, floatArrayOf(1f, 0f)).first)
        RosterStore.enroll(context, "Synthetic A", "", floatArrayOf(1f, 0f))
        Assert.assertNull(RosterStore.match(context, floatArrayOf(0f, 1f)).first)
        Assert.assertNull(RosterStore.match(context, floatArrayOf(1f)).first)
    }

    @Test fun thresholdBoundaryIsApplied() {
        RosterStore.enroll(context, "Synthetic A", "", floatArrayOf(1f, 0f))
        Assert.assertNull(RosterStore.match(context, floatArrayOf(0.59f, 0.807403f)).first)
        Assert.assertNotNull(RosterStore.match(context, floatArrayOf(0.60f, 0.80f)).first)
    }

    @Test fun deletedEntryStaysDeletedAfterReload() {
        RosterStore.enroll(context, "Synthetic A", "", floatArrayOf(1f, 0f))
        RosterStore.enroll(context, "Synthetic B", "", floatArrayOf(0f, 1f))
        RosterStore.delete(context, "Synthetic A")
        forgetMemory()
        Assert.assertEquals(1, RosterStore.count(context))
        Assert.assertNull(RosterStore.match(context, floatArrayOf(1f, 0f)).first)
        Assert.assertEquals("Synthetic B", RosterStore.match(context, floatArrayOf(0f, 1f)).first!!.name)
    }

    @Test fun clearAllPersistsEmptyRoster() {
        RosterStore.enroll(context, "Synthetic A", "", floatArrayOf(1f, 0f))
        RosterStore.clear(context)
        forgetMemory()
        Assert.assertEquals(0, RosterStore.count(context))
        Assert.assertNull(RosterStore.match(context, floatArrayOf(1f, 0f)).first)
    }

    @Test fun ciphertextTamperingIsRejectedByCrypto() {
        val encoded = RosterCrypto.encrypt("Synthetic test text")
        val bytes = Base64.decode(encoded, Base64.NO_WRAP)
        bytes[bytes.lastIndex] = (bytes.last().toInt() xor 1).toByte()
        try {
            RosterCrypto.decrypt(Base64.encodeToString(bytes, Base64.NO_WRAP))
            Assert.fail("Tampered ciphertext must fail authentication")
        } catch (_: java.security.GeneralSecurityException) {}
    }

    @Test fun stopIsIdempotentAndSignalsSessionOwner() {
        var stopCount = 0
        RecognitionControl.onStop = { stopCount++ }
        RecognitionControl.start()
        Assert.assertTrue(RecognitionControl.active)
        Assert.assertTrue(RecognitionControl.startedAt > 0)
        RecognitionControl.stop()
        RecognitionControl.stop()
        Assert.assertFalse(RecognitionControl.active)
        Assert.assertEquals(1, stopCount)
    }

    @Test fun bundledEmbeddingModelRunsOnSyntheticPixels() {
        val bitmap = Bitmap.createBitmap(160, 160, Bitmap.Config.ARGB_8888)
        try {
            for (x in 0 until 160) for (y in 0 until 160)
                bitmap.setPixel(x, y, Color.rgb(x, y, (x + y) % 256))
            Assert.assertNull(FaceEmbedder.cropFace(bitmap, Rect(0, 0, 10, 10)))
            val vector = FaceEmbedder.embed(context, bitmap)
            Assert.assertTrue(vector.isNotEmpty())
            Assert.assertTrue(vector.all { it.isFinite() })
            Assert.assertEquals(1f, FaceEmbedder.similarity(vector, vector), 0.001f)
        } finally { bitmap.recycle() }
    }
}
