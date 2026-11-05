package com.meta.wearable.dat.externalsampleapps.cameraaccess.ui

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

/** On/off switch for face recognition. Off = the glasses behave normally. */
object RecognitionControl {
    const val SHOW_NAME_MS = 8_000L          // how long a name stays on the lens
    const val NO_MATCH_TIMEOUT_MS = 30_000L  // give up if nobody is recognized

    var active by mutableStateOf(false)
        private set
    var startedAt = 0L
        private set

    /** Set by CameraViewModel: ends the glasses session when recognition stops. */
    var onStop: (() -> Unit)? = null

    fun start() {
        startedAt = System.currentTimeMillis()
        active = true
    }

    fun stop() {
        if (!active) return
        active = false
        onStop?.invoke()
    }
}