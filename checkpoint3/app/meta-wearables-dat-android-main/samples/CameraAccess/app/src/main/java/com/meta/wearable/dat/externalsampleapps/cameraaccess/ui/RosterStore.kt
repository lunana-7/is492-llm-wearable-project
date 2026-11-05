package com.meta.wearable.dat.externalsampleapps.cameraaccess.ui

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

object RosterStore {
    class Person(val name: String, val description: String, val embeddings: MutableList<FloatArray>)

    // Placeholder. We will set this from your same-person vs different-person numbers.
    var threshold = 0.60f

    private val people = mutableListOf<Person>()
    private var loaded = false

    private fun load(context: Context) {
        if (loaded) return
        loaded = true
        val stored = context.getSharedPreferences("roster", Context.MODE_PRIVATE)
            .getString("data", null) ?: return
        val raw = try { RosterCrypto.decrypt(stored) } catch (e: Exception) { stored }
        val arr = try { JSONArray(raw) } catch (e: Exception) { return }
        for (i in 0 until arr.length()) {
            val o = arr.getJSONObject(i)
            val embs = mutableListOf<FloatArray>()
            val ea = o.getJSONArray("embeddings")
            for (j in 0 until ea.length()) {
                val v = ea.getJSONArray(j)
                embs.add(FloatArray(v.length()) { k -> v.getDouble(k).toFloat() })
            }
            people.add(Person(o.getString("name"), o.getString("description"), embs))
        }
    }

    private fun save(context: Context) {
        val arr = JSONArray()
        for (p in people) {
            val o = JSONObject()
            o.put("name", p.name)
            o.put("description", p.description)
            val ea = JSONArray()
            for (e in p.embeddings) {
                val v = JSONArray()
                for (x in e) v.put(x.toDouble())
                ea.put(v)
            }
            o.put("embeddings", ea)
            arr.put(o)
        }
        context.getSharedPreferences("roster", Context.MODE_PRIVATE)
            .edit().putString("data", RosterCrypto.encrypt(arr.toString())).apply()
    }

    fun enroll(context: Context, name: String, description: String, emb: FloatArray) {
        load(context)
        val existing = people.firstOrNull { it.name.equals(name, ignoreCase = true) }
        if (existing != null) existing.embeddings.add(emb)
        else people.add(Person(name, description, mutableListOf(emb)))
        save(context)
    }

    fun count(context: Context): Int { load(context); return people.size }

    fun clear(context: Context) {
        people.clear()
        save(context)
    }
    fun all(context: Context): List<Person> {
        load(context)
        return people.toList()
    }

    fun delete(context: Context, name: String) {
        load(context)
        people.removeAll { it.name.equals(name, ignoreCase = true) }
        save(context)
    }
    /** Returns (person or null if below threshold, best score). */
    fun match(context: Context, emb: FloatArray): Pair<Person?, Float> {
        load(context)
        var best: Person? = null
        var bestScore = -1f
        for (p in people) for (e in p.embeddings) {
            if (e.size != emb.size) continue
            val s = FaceEmbedder.similarity(e, emb)
            if (s > bestScore) { bestScore = s; best = p }
        }
        return if (best != null && bestScore >= threshold) Pair(best, bestScore)
        else Pair(null, bestScore)
    }
}