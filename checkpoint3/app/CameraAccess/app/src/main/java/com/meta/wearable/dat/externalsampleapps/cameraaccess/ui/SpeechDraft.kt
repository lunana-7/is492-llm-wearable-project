package com.meta.wearable.dat.externalsampleapps.cameraaccess.ui

import android.annotation.SuppressLint
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.delay
import kotlinx.coroutines.ensureActive
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.Proxy
import java.net.URL
import java.nio.ByteBuffer
import java.nio.ByteOrder

/** The dialog checks permission and obtains consent immediately before each recording. */
@SuppressLint("MissingPermission")
internal suspend fun recordNote(): ByteArray {
    val rate = 16000
    val channel = AudioFormat.CHANNEL_IN_MONO
    val format = AudioFormat.ENCODING_PCM_16BIT
    val minimum = AudioRecord.getMinBufferSize(rate, channel, format)
    check(minimum > 0)
    val recorder = AudioRecord(MediaRecorder.AudioSource.MIC, rate, channel, format, maxOf(minimum, 8192))
    try {
        recorder.startRecording()
        check(recorder.recordingState == AudioRecord.RECORDSTATE_RECORDING)
        val pcm = ByteArray(rate * 2 * 8)
        var position = 0
        while (position < pcm.size) {
            currentCoroutineContext().ensureActive()
            val n = recorder.read(pcm, position, minOf(8192, pcm.size - position), AudioRecord.READ_NON_BLOCKING)
            check(n >= 0)
            position += n
            if (n == 0) delay(20)
        }
        return ByteBuffer.allocate(44 + pcm.size).order(ByteOrder.LITTLE_ENDIAN).apply {
            put("RIFF".toByteArray()); putInt(36 + pcm.size); put("WAVEfmt ".toByteArray())
            putInt(16); putShort(1); putShort(1); putInt(rate); putInt(rate * 2)
            putShort(2); putShort(16); put("data".toByteArray()); putInt(pcm.size); put(pcm)
        }.array()
    } finally {
        recorder.release()
    }
}

internal fun requestDraft(audio: ByteArray): String {
    val connection = URL("http://127.0.0.1:8765/draft").openConnection(Proxy.NO_PROXY) as HttpURLConnection
    try {
        connection.requestMethod = "POST"
        connection.instanceFollowRedirects = false
        connection.connectTimeout = 3000
        connection.readTimeout = 100000
        connection.doOutput = true
        connection.setRequestProperty("Content-Type", "audio/wav")
        connection.setRequestProperty("X-Recording-Consent", "yes")
        connection.setFixedLengthStreamingMode(audio.size)
        connection.outputStream.use { it.write(audio) }
        when (connection.responseCode) {
            200 -> return JSONObject(connection.inputStream.bufferedReader().use { it.readText() }).getString("draft")
            429 -> error("Another draft is running. Try again shortly.")
            else -> error("Draft unavailable. Check the laptop models and try again.")
        }
    } finally {
        connection.disconnect()
    }
}
