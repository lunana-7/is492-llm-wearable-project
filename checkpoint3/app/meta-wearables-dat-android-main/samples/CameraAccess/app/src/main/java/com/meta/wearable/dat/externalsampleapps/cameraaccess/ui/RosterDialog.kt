package com.meta.wearable.dat.externalsampleapps.cameraaccess.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext

@Composable
fun RosterDialog(onDismiss: () -> Unit) {
    val context = LocalContext.current
    var people by remember { mutableStateOf(RosterStore.all(context)) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Enrolled people (${people.size})") },
        confirmButton = { TextButton(onClick = onDismiss) { Text("Close") } },
        dismissButton = {
            if (people.isNotEmpty()) {
                TextButton(onClick = {
                    RosterStore.clear(context)
                    people = RosterStore.all(context)
                }) { Text("Delete all") }
            }
        },
        text = {
            if (people.isEmpty()) {
                Text("No one is enrolled.")
            } else {
                LazyColumn {
                    items(people) { p ->
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(p.name)
                                Text("${p.description} - ${p.embeddings.size} photo(s)")
                            }
                            IconButton(onClick = {
                                RosterStore.delete(context, p.name)
                                people = RosterStore.all(context)
                            }) {
                                Icon(Icons.Filled.Delete, contentDescription = "Delete ${p.name}")
                            }
                        }
                    }
                }
            }
        }
    )
}