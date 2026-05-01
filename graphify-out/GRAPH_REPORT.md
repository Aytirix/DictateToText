# Graph Report - py  (2026-05-02)

## Corpus Check
- 16 files · ~10,948 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 387 nodes · 600 edges · 23 communities detected
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 190 edges (avg confidence: 0.53)
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

## God Nodes (most connected - your core abstractions)
1. `HistoryWindow` - 104 edges
2. `SettingsWindow` - 82 edges
3. `AppConfig` - 54 edges
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
Nodes (52): HistoryWindow, Clear all history with confirmation, Schedule periodic status updates, Update transcription status indicator, Update history content with optional search, Update system statistics, Update GPU information - supports NVIDIA, AMD, Intel, Modern history window with CustomTkinter (+44 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (43): Clear all history with confirmation, Schedule periodic status updates, Update transcription status indicator, Update history content with optional search, Update system statistics, Update GPU information - supports NVIDIA, AMD, Intel, Toggle real-time logs, Start real-time log streaming (+35 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (40): AudioRecorder, Audio recording component, Handle audio recording, Start audio input stream, Stop audio input stream, Audio callback for recording, Start recording audio, Stop recording and save to file (+32 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (19): Config, get_config_instance(), load_config(), Sauvegarde la configuration dans le fichier JSON, Récupère une valeur de configuration, Définit une valeur de configuration et sauvegarde, Met à jour plusieurs valeurs, Réinitialise à la configuration par défaut (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (18): DictatePTTApplication, _display_number(), Main application orchestrator, Show persistent recording notification., Stop the toggle recording reminder., Show or focus history window (called on main thread), Main application orchestrator, Create hidden CTk root when a graphical display is available. (+10 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (13): HistoryManager, History management component, Return a snapshot of items (thread-safe), Update maximum history size, Attach an observer to be notified of changes, Notify all observers of changes (thread-safe for Tkinter), Manage transcription history, Transcription worker thread (+5 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (12): ClipboardService, Handle clipboard operations, Copy text to clipboard using wl-copy, NotificationService, Handle system notifications, _clean_output(), _is_gpu_oom(), Transcription service using Whisper (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (13): History window with CustomTkinter - Modern Design, _enable_mousewheel_scroll(), _format_key_combo(), _get_base_model_name(), _get_quantization_suffix(), _is_modifier_key(), _parse_key_combo(), Settings window with CustomTkinter - Modern Design (+5 more)

### Community 8 - "Community 8"
Cohesion: 0.14
Nodes (8): _enable_mousewheel_scroll(), Enable mousewheel scrolling for a widget and all its children, Refresh the list of audio files, Delete a single audio file, Delete all audio files, Update window title with history size, Add the audio files tab dynamically, Setup the modern user interface

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (6): Show Whisper models management, Return models supported by the local whisper.cpp install, plus installed files., Sort current and installed models first, then keep whisper.cpp order., Select a different Whisper model, Download a Whisper model, Uninstall a Whisper model

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Send a system notification without blocking

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): Show persistent listening notification.

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): Show persistent transcribing notification.

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): Show short success notification.

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Show short error notification.

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): Send a notification, optionally replacing the previous app notification.

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): Run whisper-cli and handle timeouts.

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): Return True when whisper.cpp failed because CUDA ran out of memory.

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Keyboard event loop (runs in daemon thread)

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Show or focus history window (called on main thread)

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Validate configuration paths

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Update logs widget from queue (called from main thread)

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Send a system notification without blocking

## Knowledge Gaps
- **116 isolated node(s):** `Keyboard event loop (runs in daemon thread)`, `Show or focus history window (called on main thread)`, `Parse a DISPLAY value like :1 or :1.0 into its numeric display id.`, `Gestionnaire de configuration`, `Charge la configuration depuis le fichier JSON` (+111 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (1 nodes): `Send a system notification without blocking`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `Show persistent listening notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `Show persistent transcribing notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `Show short success notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Show short error notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `Send a notification, optionally replacing the previous app notification.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `Run whisper-cli and handle timeouts.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `Return True when whisper.cpp failed because CUDA ran out of memory.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `Keyboard event loop (runs in daemon thread)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `Show or focus history window (called on main thread)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `Validate configuration paths`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Update logs widget from queue (called from main thread)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Send a system notification without blocking`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HistoryWindow` connect `Community 0` to `Community 1`, `Community 3`, `Community 4`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.538) - this node is a cross-community bridge._
- **Why does `DictatePTTApplication` connect `Community 4` to `Community 2`, `Community 6`?**
  _High betweenness centrality (0.398) - this node is a cross-community bridge._
- **Why does `SettingsWindow` connect `Community 1` to `Community 0`, `Community 3`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.302) - this node is a cross-community bridge._
- **Are the 74 inferred relationships involving `HistoryWindow` (e.g. with `SettingsWindow` and `Settings window with CustomTkinter - Modern Design`) actually correct?**
  _`HistoryWindow` has 74 INFERRED edges - model-reasoned connections that need verification._
- **Are the 43 inferred relationships involving `SettingsWindow` (e.g. with `HistoryWindow` and `History window with CustomTkinter - Modern Design`) actually correct?**
  _`SettingsWindow` has 43 INFERRED edges - model-reasoned connections that need verification._
- **Are the 48 inferred relationships involving `AppConfig` (e.g. with `DictatePTTApplication` and `Main application orchestrator`) actually correct?**
  _`AppConfig` has 48 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `DictatePTTApplication` (e.g. with `AppConfig` and `Application entry point`) actually correct?**
  _`DictatePTTApplication` has 3 INFERRED edges - model-reasoned connections that need verification._