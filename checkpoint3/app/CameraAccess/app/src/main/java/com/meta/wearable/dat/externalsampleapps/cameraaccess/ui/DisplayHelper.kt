package com.meta.wearable.dat.externalsampleapps.cameraaccess.ui
import com.meta.wearable.dat.core.session.DeviceSession
import android.util.Log
import com.meta.wearable.dat.core.*
import com.meta.wearable.dat.display.*
import com.meta.wearable.dat.display.types.*
import com.meta.wearable.dat.display.views.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

object DisplayHelper {
    private const val TAG = "DisplayHelper"
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
    private var display: Display? = null
    private var lastKey: String? = null
    private var lastSentAt = 0L
    private var attaching = false

    /** Call once the device session is STARTED. Safe to call more than once. */
    fun attach(session: DeviceSession) {
        if (display != null || attaching) return
        attaching = true
        scope.launch {
            try {
                val d = session.addDisplay(DisplayConfiguration()).getOrThrow()
                d.state.first { it == DisplayState.STARTED }
                display = d
                lastKey = null
                Log.d(TAG, "Display ready")
            } catch (e: Exception) {
                Log.e(TAG, "Display attach failed: ${e.message}")
            } finally {
                attaching = false
            }
        }
    }

    /** Call when the session ends. */
    fun detach(session: DeviceSession?) {
        display = null
        lastKey = null
        attaching = false
        if (session == null) return
        scope.launch {
            try {
                session.removeDisplay()
            } catch (e: Exception) {
                Log.e(TAG, "detach failed: ${e.message}")
            }
        }
    }

    /** Shows a recognized person on the lens. */
    fun show(name: String, description: String) {
        val d = display ?: return
        val key = "show|$name|$description"
        if (!shouldSend(key)) return
        scope.launch {
            d.sendContent {
                flexBox(direction = Direction.COLUMN, gap = 8, paddingTop = 16, paddingBottom = 16, paddingStart = 16, paddingEnd = 16) {
                    text(name, style = TextStyle.HEADING)
                    if (description.isNotBlank()) {
                        text(description, style = TextStyle.BODY, color = TextColor.SECONDARY)
                    }
                }
            }.fold(
                onSuccess = { },
                onFailure = { error, _ ->
                    lastKey = null
                    Log.e(TAG, "sendContent failed: $error")
                }
            )
        }
    }

    /** Shows the waiting message when nobody is recognized. */
    fun clear() {
        val d = display ?: return
        if (!shouldSend("clear")) return
        scope.launch {
            d.sendContent {
                flexBox(direction = Direction.COLUMN, paddingTop = 16, paddingBottom = 16, paddingStart = 16, paddingEnd = 16) {
                    text("Looking for students...", style = TextStyle.META, color = TextColor.SECONDARY)
                }
            }.fold(
                onSuccess = { },
                onFailure = { error, _ ->
                    lastKey = null
                    Log.e(TAG, "sendContent failed: $error")
                }
            )
        }
    }

    // Skips repeats, but resends every 15 s because the lens dims at 20 s and sleeps at 25 s.
    private fun shouldSend(key: String): Boolean {
        val now = System.currentTimeMillis()
        if (key == lastKey && now - lastSentAt < 15_000) return false
        lastKey = key
        lastSentAt = now
        return true
    }
}