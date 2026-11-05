package com.meta.wearable.dat.externalsampleapps.cameraaccess.ui

import android.content.Context
import android.graphics.Bitmap
import android.os.Handler
import android.os.Looper
import android.view.PixelCopy
import android.view.Surface
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import kotlin.coroutines.resume
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.suspendCancellableCoroutine

object LiveRecognizer {
    var text by mutableStateOf("")
    private val handler = Handler(Looper.getMainLooper())

    private suspend fun grab(surface: Surface, w: Int, h: Int): Bitmap? =
        suspendCancellableCoroutine { cont ->
            val bmp = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
            try {
                PixelCopy.request(surface, bmp, { result ->
                    if (cont.isActive) {
                        cont.resume(if (result == PixelCopy.SUCCESS) bmp else null)
                    }
                }, handler)
            } catch (e: Exception) {
                if (cont.isActive) cont.resume(null)
            }
        }

    private suspend fun faces(bmp: Bitmap) =
        suspendCancellableCoroutine<List<android.graphics.Rect>> { cont ->
            FaceDetectorHelper.detectFaces(
                bmp,
                onResult = { if (cont.isActive) cont.resume(it) },
                onError = { if (cont.isActive) cont.resume(emptyList()) }
            )
        }

    suspend fun run(context: Context, surface: Surface, viewW: Int, viewH: Int) {
        if (viewW <= 0 || viewH <= 0) return
        val bw = 640
        val bh = (bw.toFloat() * viewH / viewW).toInt().coerceAtLeast(1)
        var failures = 0
        var candidate: String? = null
        var streak = 0
        while (currentCoroutineContext().isActive && surface.isValid) {
            try {
                val bmp = grab(surface, bw, bh)
                if (bmp == null) {
                    failures++
                    if (failures >= 3) text = "Frame copy failed"
                } else {
                    failures = 0
                    val found = faces(bmp)
                    val biggest = found.maxByOrNull { it.width() * it.height() }
                    if (biggest == null) {
                        candidate = null
                        streak = 0
                        text = ""
                    } else {
                        val crop = FaceEmbedder.cropFace(bmp, biggest)
                        if (crop == null) {
                            text = "Face too small"
                        } else {
                            val emb = FaceEmbedder.embed(context, crop)
                            val (person, score) = RosterStore.match(context, emb)
                            val name = person?.name
                            if (name != null && name == candidate) streak++
                            else { candidate = name; streak = 1 }
                            text = when {
                                person == null -> "Unknown (best %.2f)".format(score)
                                streak >= 3 ->
                                    "${person.name} - ${person.description} (%.2f)".format(score)
                                else -> "Checking..."
                            }
                        }
                    }
                }
            } catch (e: Exception) {
                text = "Error: ${e.message}"
            }
            delay(500)
        }
        text = ""
    }
}