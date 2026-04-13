# Dictate PTT Copilot - Configuration

## 📋 Configuration Complète

Le fichier de configuration se trouve dans : `~/Documents/tools/py/config/dictate_ptt_copilot/config.json`

### 🎨 Interface & Thème

```json
{
  "theme_mode": "dark",           // "dark", "light", "system"
  "accent_color": "blue",          // "blue", "green", "red", "violet", "orange"
  "window_opacity": 1.0,           // 0.8 à 1.0
  "font_family": "Segoe UI",       // Police personnalisée
  "font_size": 12,                 // Taille globale
  "animations_enabled": true,      // Activer animations
  "corner_radius": 10,             // Rayon coins arrondis (0-20px)
  "ui_scaling": 1.0               // Zoom interface (0.8-1.5x)
}
```

### 🎙️ Audio & Enregistrement

```json
{
  "sample_rate": 16000,            // 16000, 22050, 44100, 48000 Hz
  "channels": 1,                   // 1=Mono, 2=Stéréo
  "audio_format": "wav",           // "wav", "flac", "mp3"
  "noise_reduction": false,        // Réduction de bruit
  "auto_gain": false,              // Normalisation auto volume
  "silence_threshold": 0.01,       // Seuil de silence (0.0-1.0)
  "audio_device_index": null       // null=défaut, ou index du micro
}
```

### 🤖 Whisper & Transcription

```json
{
  "whisper_model": "large-v3",     // Exemples: "tiny", "small.en", "large-v3", "large-v3-turbo"
  "language": "fr",                // "fr", "en", "auto", etc.
  "task": "transcribe",            // "transcribe" ou "translate"
  "temperature": 0.0,              // Créativité (0.0-1.0)
  "beam_size": 5,                  // Qualité vs vitesse (1-10)
  "best_of": 5,                    // Nombre tentatives (1-5)
  "initial_prompt": "",            // Contexte/vocabulaire
  "word_timestamps": false,        // Timestamps par mot
  "vad_filter": false,             // Voice Activity Detection
  "compute_type": "float16"        // "int8", "float16", "float32"
}
```

**Téléchargement automatique des modèles** : Si un modèle n'est pas détecté, l'interface proposera de le télécharger automatiquement.

### ⌨️ Raccourcis Clavier

```json
{
  "record_combo": ["KEY_LEFTMETA", "KEY_LEFTSHIFT", "KEY_F23"],
  "history_combo": ["KEY_LEFTCTRL", "KEY_LEFTSHIFT", "KEY_H"]
}
```

Personnalisable depuis l'interface.

### 📋 Presse-papiers & Sortie

```json
{
  "add_prefix": "",                // Texte ajouté avant (optionnel)
  "add_suffix": "",                // Texte ajouté après (optionnel)
  "clipboard_timeout": 60          // Durée dans clipboard (0=illimité)
}
```

### 📝 Historique

```json
{
  "history_size": 10,              // Nombre max d'éléments
  "history_persistence": true,     // Garder entre sessions
  "history_search": true,          // Recherche dans historique
  "history_export_format": "txt",  // "txt", "json", "csv"
  "history_auto_clear_days": 0     // Vider après X jours (0=jamais)
}
```

### 🔔 Notifications & Feedback

```json
{
  "notifications_enabled": true,
  "notification_position": "top-right",  // Position à l'écran
  "notification_duration": 3,            // Durée affichage (secondes)
  "visual_feedback": true,               // Indicateur visuel
  "tray_icon": true                      // Icône barre système
}
```

### 🔧 Comportement

```json
{
  "recording_mode": "push_to_talk",  // "push_to_talk" seulement (toggle non implémenté)
  "auto_start": false,                // Lancer au démarrage système
  "minimize_to_tray": false,          // Minimiser vers barre système (non implémenté)
  "close_to_tray": false              // Fermer vers barre système (non implémenté)
}
```

**Note**: Actuellement, seul le mode `push_to_talk` est fonctionnel. Le mode `toggle` et les fonctionnalités de barre système ne sont pas encore implémentés.

### 🐛 Debug & Logs

```json
{
  "log_level": "info",                    // "debug", "info", "warning", "error"
  "log_to_file": false,                   // Sauvegarder logs
  "log_file_path": "~/...logs/dictate_ptt.log",
  "show_console": false,                  // Console de debug
  "performance_monitoring": false,        // Monitoring CPU/GPU/RAM
  "save_audio_files": false              // Garder fichiers WAV temp
}
```

## 🚀 Utilisation

### Via Code Python

```python
from config import get_config_instance

config = get_config_instance()

# Lire
theme = config.get("theme_mode")
model = config.get("whisper_model")

# Écrire
config.set("theme_mode", "light")
config.set("accent_color", "green")

# Mise à jour multiple
config.update({
    "font_size": 14,
    "animations_enabled": True
})

# Réinitialiser
config.reset()
```

### Via Interface

Toutes les options sont accessibles via le bouton ⚙️ dans la fenêtre d'historique.

## 📦 Modèles Whisper Disponibles

| Modèle | Taille | RAM | Vitesse | Qualité |
|--------|--------|-----|---------|---------|
| tiny   | 75 MB  | ~1 GB | ⚡⚡⚡⚡⚡ | ⭐⭐ |
| base   | 142 MB | ~1 GB | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| small  | 466 MB | ~2 GB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| medium | 1.5 GB | ~5 GB | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| large-v1/v2/v3 | 2.9 GB | ~10 GB | ⚡ | ⭐⭐⭐⭐⭐ |

## 🎯 Exemples de Configuration

### Configuration Légère (PC faible)
```json
{
  "whisper_model": "tiny",
  "compute_type": "int8",
  "animations_enabled": false,
  "performance_monitoring": false
}
```

### Configuration Qualité Maximale
```json
{
  "whisper_model": "large-v3",
  "compute_type": "float32",
  "beam_size": 10,
  "best_of": 5,
  "vad_filter": true
}
```

### Configuration Rapide
```json
{
  "whisper_model": "small",
  "compute_type": "int8",
  "beam_size": 1,
  "best_of": 1
}
```
