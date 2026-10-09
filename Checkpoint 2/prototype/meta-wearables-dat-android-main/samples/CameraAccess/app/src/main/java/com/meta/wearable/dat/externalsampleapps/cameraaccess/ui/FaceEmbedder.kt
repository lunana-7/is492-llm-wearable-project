package com.meta.wearable.dat.externalsampleapps.cameraaccess.ui

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Rect
import android.util.Log
import java.io.FileInputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.channels.FileChannel
import kotlin.math.max
import kotlin.math.min
import kotlin.math.sqrt
import org.tensorflow.lite.Interpreter

object FaceEmbedder {
    private var interpreter: Interpreter? = null
    private var inputSize = 160
    private var outputSize = 128
    var lastEmbedding: FloatArray? = null

    private fun ensureLoaded(context: Context) {
        if (interpreter != null) return
        val fd = context.assets.openFd("face_model.tflite")
        val buffer = FileInputStream(fd.fileDescriptor).channel
            .map(FileChannel.MapMode.READ_ONLY, fd.startOffset, fd.declaredLength)
        val interp = Interpreter(buffer)
        val inShape = interp.getInputTensor(0).shape()
        val outShape = interp.getOutputTensor(0).shape()
        inputSize = inShape[1]
        outputSize = outShape[1]
        Log.d("FaceEmbedder", "input=${inShape.toList()} output=${outShape.toList()}")
        interpreter = interp
    }

    fun cropFace(bitmap: Bitmap, rect: Rect): Bitmap? {
        val left = max(0, rect.left)
        val top = max(0, rect.top)
        val right = min(bitmap.width, rect.right)
        val bottom = min(bitmap.height, rect.bottom)
        if (right - left < 20 || bottom - top < 20) return null
        return Bitmap.createBitmap(bitmap, left, top, right - left, bottom - top)
    }

    fun embed(context: Context, face: Bitmap): FloatArray {
        ensureLoaded(context)
        val scaled = Bitmap.createScaledBitmap(face, inputSize, inputSize, true)
        val pixels = IntArray(inputSize * inputSize)
        scaled.getPixels(pixels, 0, inputSize, 0, 0, inputSize, inputSize)

        val values = FloatArray(inputSize * inputSize * 3)
        var i = 0
        for (p in pixels) {
            values[i++] = ((p shr 16) and 0xFF).toFloat()
            values[i++] = ((p shr 8) and 0xFF).toFloat()
            values[i++] = (p and 0xFF).toFloat()
        }
        val mean = values.average().toFloat()
        var variance = 0f
        for (v in values) variance += (v - mean) * (v - mean)
        val std = max(sqrt(variance / values.size), 1f / sqrt(values.size.toFloat()))

        val input = ByteBuffer.allocateDirect(values.size * 4).order(ByteOrder.nativeOrder())
        for (v in values) input.putFloat((v - mean) / std)
        input.rewind()

        val output = Array(1) { FloatArray(outputSize) }
        interpreter!!.run(input, output)

        val emb = output[0]
        var norm = 0f
        for (v in emb) norm += v * v
        norm = sqrt(norm)
        if (norm > 0f) for (k in emb.indices) emb[k] = emb[k] / norm
        return emb
    }

    fun similarity(a: FloatArray, b: FloatArray): Float {
        var dot = 0f
        for (k in a.indices) dot += a[k] * b[k]
        return dot
    }
}