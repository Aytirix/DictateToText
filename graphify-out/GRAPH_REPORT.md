# Graph Report - py  (2026-05-03)

## Corpus Check
- 16 files · ~11,170 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 413 nodes · 617 edges · 33 communities detected
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 201 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]

## God Nodes (most connected - your core abstractions)
1. `HistoryWindow` - 104 edges
2. `SettingsWindow` - 82 edges
3. `AppConfig` - 65 edges
4. `DictatePTTApplication` - 20 edges
5. `HistoryManager` - 17 edges
6. `Config` - 14 edges
7. `KeyboardHandler` - 11 edges
8. `AudioRecorder` - 10 edges
9. `TranscriptionWorker` - 9 edges
10. `NotificationService` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Main application orchestrator` --uses--> `AppConfig`  [INFERRED]
  application.py → app_config.py
- `Main application orchestrator` --uses--> `AppConfig`  [INFERRED]
  application.py → app_config.py
- `Show persistent recording notification.` --uses--> `AppConfig`  [INFERRED]
  application.py → app_config.py
- `Stop the toggle recording reminder.` --uses--> `AppConfig`  [INFERRED]
  application.py → app_config.py
- `Create hidden CTk root when a graphical display is available.` --uses--> `AppConfig`  [INFERRED]
  application.py → app_config.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.03
Nodes (60): _enable_mousewheel_scroll(), HistoryWindow, Enable mousewheel scrolling for a widget and all its children, Clear all history with confirmation, Schedule periodic status updates, Update transcription status indicator, Update history content with optional search, Update system statistics (+52 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (49): History window with CustomTkinter - Modern Design, Clear all history with confirmation, Schedule periodic status updates, Update transcription status indicator, Update history content with optional search, Update system statistics, Update GPU information - supports NVIDIA, AMD, Intel, Toggle real-time logs (+41 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (51): AudioRecorder, Audio recording component, Handle audio recording, Start audio input stream, Stop audio input stream, Audio callback for recording, Start recording audio, Stop recording and save to file (+43 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (19): Config, get_config_instance(), load_config(), Sauvegarde la configuration dans le fichier JSON, Récupère une valeur de configuration, Définit une valeur de configuration et sauvegarde, Met à jour plusieurs valeurs, Réinitialise à la configuration par défaut (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (18): DictatePTTApplication, _display_number(), Main application orchestrator, Keyboard event loop (runs in daemon thread), Show persistent recording notification., Stop the toggle recording reminder., Show or focus history window (called on main thread), Main application orchestrator (+10 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (13): HistoryManager, History management component, Return a snapshot of items (thread-safe), Update maximum history size, Attach an observer to be notified of changes, Notify all observers of changes (thread-safe for Tkinter), Manage transcription history, Transcription worker thread (+5 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (13): Switch to a different settings category, Show interface settings, Show Whisper settings, Show history settings, Show notification settings, Show behavior settings, Create category title, Create an option menu with label (+5 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (15): ClipboardService, Handle clipboard operations, Copy text to clipboard using wl-copy, _build_command(), NotificationService, Handle system notifications, send(), _send_replace() (+7 more)

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (1): Send a system notification without blocking

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): Show persistent listening notification.

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Show persistent transcribing notification.

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): Show short success notification.

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): Show short error notification.

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): Close the currently tracked notification when the server supports it.

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Send a notification, optionally replacing the previous app notification.

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): Send a replacing notification and return its fresh ID.

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): Build the notify-send command.

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): Run whisper-cli and handle timeouts.

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Return True when whisper.cpp failed because CUDA ran out of memory.

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Keyboard event loop (runs in daemon thread)

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Show or focus history window (called on main thread)

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Handle system notifications

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Send a system notification without blocking

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Show persistent listening notification.

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Show persistent transcribing notification.

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Show short success notification.

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Show short error notification.

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Send a notification, optionally replacing the previous app notification.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Keyboard event loop (runs in daemon thread)

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Show or focus history window (called on main thread)

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Validate configuration paths

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Update logs widget from queue (called from main thread)

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Send a system notification without blocking

## Knowledge Gaps
- **139 isolated node(s):** `Keyboard event loop (runs in daemon thread)`, `Show or focus history window (called on main thread)`, `Parse a DISPLAY value like :1 or :1.0 into its numeric display id.`, `Gestionnaire de configuration`, `Charge la configuration depuis le fichier JSON` (+134 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 8`** (1 nodes): `Send a system notification without blocking`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (1 nodes): `Show persistent listening notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `Show persistent transcribing notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `Show short success notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `Show short error notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `Close the currently tracked notification when the server supports it.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Send a notification, optionally replacing the previous app notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `Send a replacing notification and return its fresh ID.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `Build the notify-send command.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `Run whisper-cli and handle timeouts.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `Return True when whisper.cpp failed because CUDA ran out of memory.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `Keyboard event loop (runs in daemon thread)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `Show or focus history window (called on main thread)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Handle system notifications`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Send a system notification without blocking`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Show persistent listening notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Show persistent transcribing notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Show short success notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Show short error notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Send a notification, optionally replacing the previous app notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Keyboard event loop (runs in daemon thread)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Show or focus history window (called on main thread)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Validate configuration paths`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `Update logs widget from queue (called from main thread)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Send a system notification without blocking`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HistoryWindow` connect `Community 0` to `Community 1`, `Community 3`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.503) - this node is a cross-community bridge._
- **Why does `DictatePTTApplication` connect `Community 4` to `Community 2`, `Community 7`?**
  _High betweenness centrality (0.388) - this node is a cross-community bridge._
- **Why does `SettingsWindow` connect `Community 1` to `Community 0`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.273) - this node is a cross-community bridge._
- **Are the 74 inferred relationships involving `HistoryWindow` (e.g. with `SettingsWindow` and `Settings window with CustomTkinter - Modern Design`) actually correct?**
  _`HistoryWindow` has 74 INFERRED edges - model-reasoned connections that need verification._
- **Are the 43 inferred relationships involving `SettingsWindow` (e.g. with `HistoryWindow` and `History window with CustomTkinter - Modern Design`) actually correct?**
  _`SettingsWindow` has 43 INFERRED edges - model-reasoned connections that need verification._
- **Are the 59 inferred relationships involving `AppConfig` (e.g. with `DictatePTTApplication` and `Main application orchestrator`) actually correct?**
  _`AppConfig` has 59 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `DictatePTTApplication` (e.g. with `AppConfig` and `Application entry point`) actually correct?**
  _`DictatePTTApplication` has 3 INFERRED edges - model-reasoned connections that need verification._