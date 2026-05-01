# Graph Report - py  (2026-05-02)

## Corpus Check
- 16 files · ~9,938 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 274 nodes · 465 edges · 17 communities detected
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 107 edges (avg confidence: 0.54)
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

## God Nodes (most connected - your core abstractions)
1. `HistoryWindow` - 63 edges
2. `SettingsWindow` - 56 edges
3. `AppConfig` - 33 edges
4. `DictatePTTApplication` - 18 edges
5. `HistoryManager` - 17 edges
6. `Config` - 14 edges
7. `AudioRecorder` - 10 edges
8. `TranscriptionWorker` - 9 edges
9. `KeyboardHandler` - 9 edges
10. `NotificationService` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Audio recording component` --uses--> `AppConfig`  [INFERRED]
  components/audio_recorder.py → app_config.py
- `Handle audio recording` --uses--> `AppConfig`  [INFERRED]
  components/audio_recorder.py → app_config.py
- `Start audio input stream` --uses--> `AppConfig`  [INFERRED]
  components/audio_recorder.py → app_config.py
- `Stop audio input stream` --uses--> `AppConfig`  [INFERRED]
  components/audio_recorder.py → app_config.py
- `Audio callback for recording` --uses--> `AppConfig`  [INFERRED]
  components/audio_recorder.py → app_config.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (28): KeyboardHandler, Initialize keyboard device, Generator yielding keyboard events, Check if copilot combo is pressed, Check if history combo is pressed, Handle keyboard events and combos, AppConfig, Application configuration (+20 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (15): Audio recording component, HistoryManager, History management component, Return a snapshot of items (thread-safe), Update maximum history size, Attach an observer to be notified of changes, Notify all observers of changes (thread-safe for Tkinter), Manage transcription history (+7 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (16): Config, get_config_instance(), load_config(), Sauvegarde la configuration dans le fichier JSON, Récupère une valeur de configuration, Met à jour plusieurs valeurs, Réinitialise à la configuration par défaut, Retourne toute la configuration (+8 more)

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (12): ClipboardService, Handle clipboard operations, Copy text to clipboard using wl-copy, NotificationService, Handle system notifications, _clean_output(), _is_gpu_oom(), Transcription service using Whisper (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.18
Nodes (9): Switch to a different settings category, Show interface settings, Show history settings, Show notification settings, Show behavior settings, Create category title, Create an option menu with label, Create a slider with label and value display (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (9): HistoryWindow, Clear all history with confirmation, Modern history window with CustomTkinter, Thread that reads logs from journalctl -f, Refresh logs from journalctl, Bring window to front, Remove the audio files tab dynamically, Extract quantization suffix like q5_0 or q8_0 when present. (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (8): Make window modal after it's viewable, Setup modern settings UI, Initialize all configuration variables, Modern settings window with CustomTkinter, Browse for whisper path, Apply all settings with hot-reload, Reset to default settings, SettingsWindow

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (8): _enable_mousewheel_scroll(), Enable mousewheel scrolling for a widget and all its children, Refresh the list of audio files, Delete a single audio file, Delete all audio files, Setup the modern user interface, Update window title with history size, Add the audio files tab dynamically

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (7): AudioRecorder, Handle audio recording, Start audio input stream, Stop audio input stream, Audio callback for recording, Start recording audio, Stop recording and save to file

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (5): Schedule periodic status updates, Update transcription status indicator, Update history content with optional search, Update system statistics, Update GPU information - supports NVIDIA, AMD, Intel

### Community 10 - "Community 10"
Cohesion: 0.17
Nodes (6): Show Whisper models management, Return models supported by the local whisper.cpp install, plus installed files., Sort current and installed models first, then keep whisper.cpp order., Select a different Whisper model, Download a Whisper model, Uninstall a Whisper model

### Community 11 - "Community 11"
Cohesion: 0.24
Nodes (7): History window with CustomTkinter - Modern Design, _enable_mousewheel_scroll(), _get_base_model_name(), _get_quantization_suffix(), Settings window with CustomTkinter - Modern Design, Enable mousewheel scrolling for a widget and all its children, Build a UI-friendly description for a model variant.

### Community 12 - "Community 12"
Cohesion: 0.24
Nodes (4): Show Whisper settings, Create an option menu with help tooltip, Create a slider with help tooltip, Create a switch with help tooltip

### Community 13 - "Community 13"
Cohesion: 0.22
Nodes (4): Toggle real-time logs, Start real-time log streaming, Stop real-time log streaming, Update logs widget from queue (called from main thread)

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Send a system notification without blocking

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): Run whisper-cli and handle timeouts.

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): Return True when whisper.cpp failed because CUDA ran out of memory.

## Knowledge Gaps
- **36 isolated node(s):** `Keyboard event loop (runs in daemon thread)`, `Show or focus history window (called on main thread)`, `Parse a DISPLAY value like :1 or :1.0 into its numeric display id.`, `Gestionnaire de configuration`, `Charge la configuration depuis le fichier JSON` (+31 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 14`** (1 nodes): `Send a system notification without blocking`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `Run whisper-cli and handle timeouts.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `Return True when whisper.cpp failed because CUDA ran out of memory.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HistoryWindow` connect `Community 5` to `Community 0`, `Community 4`, `Community 6`, `Community 7`, `Community 9`, `Community 10`, `Community 11`, `Community 12`, `Community 13`?**
  _High betweenness centrality (0.598) - this node is a cross-community bridge._
- **Why does `DictatePTTApplication` connect `Community 0` to `Community 3`?**
  _High betweenness centrality (0.585) - this node is a cross-community bridge._
- **Why does `SettingsWindow` connect `Community 6` to `Community 4`, `Community 5`, `Community 7`, `Community 9`, `Community 10`, `Community 11`, `Community 12`, `Community 13`?**
  _High betweenness centrality (0.214) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `HistoryWindow` (e.g. with `SettingsWindow` and `Settings window with CustomTkinter - Modern Design`) actually correct?**
  _`HistoryWindow` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `SettingsWindow` (e.g. with `HistoryWindow` and `History window with CustomTkinter - Modern Design`) actually correct?**
  _`SettingsWindow` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 29 inferred relationships involving `AppConfig` (e.g. with `DictatePTTApplication` and `Main application orchestrator`) actually correct?**
  _`AppConfig` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `DictatePTTApplication` (e.g. with `AppConfig` and `Application entry point`) actually correct?**
  _`DictatePTTApplication` has 3 INFERRED edges - model-reasoned connections that need verification._