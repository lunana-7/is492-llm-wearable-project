package com.meta.wearable.dat.externalsampleapps.cameraaccess.ui

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

/** Set when "Hey Meta, start <app name>" reaches the app. CameraScreen reacts to it. */
object VoiceTrigger {
    var requested by mutableStateOf(false)
        private set

    fun request() { requested = true }
    fun consume() { requested = false }
}