# 🎙️ Dictate PTT Copilot

**Dictée vocale push-to-talk pour Linux**, propulsée par [whisper.cpp](https://github.com/ggerganov/whisper.cpp). Transcription 100 % locale, aucune donnée envoyée sur Internet.

Maintenez une combinaison de touches, parlez, relâchez : le texte transcrit est automatiquement copié dans votre presse-papiers.

![Linux](https://img.shields.io/badge/Linux-Wayland-blue)
![Python](https://img.shields.io/badge/Python-3.12+-green)
![whisper.cpp](https://img.shields.io/badge/whisper.cpp-local-orange)

---

## Fonctionnalités

- **Push-to-talk global** — fonctionne dans n'importe quelle application (via evdev)
- **Transcription locale** — whisper.cpp, pas d'API cloud, pas de données envoyées
- **Copie automatique** — le texte transcrit est copié dans le presse-papiers Wayland
- **Notifications système** — feedback visuel via `notify-send`
- **Interface graphique** — historique, statistiques système, logs, gestion audio (CustomTkinter)
- **Fenêtre de paramètres** — configuration complète via l'interface
- **Service systemd** — tourne en arrière-plan, démarre avec la session graphique
- **Raccourcis configurables** — modifiez les combinaisons de touches via le fichier de config

---

## Prérequis

| Composant | Version | Rôle |
|-----------|---------|------|
| **Linux** | Wayland (GNOME, KDE, Sway…) | Environnement graphique |
| **Python** | 3.12+ | Runtime |
| **whisper.cpp** | Dernière version | Moteur de transcription |
| **wl-clipboard** | — | Copie dans le presse-papiers (`wl-copy`) |
| **libnotify** | — | Notifications système (`notify-send`) |
| **PipeWire** | — | Serveur audio (installé par défaut sur les distros modernes) |

### Installer les dépendances système

```bash
# Debian / Ubuntu
sudo apt install python3 python3-venv wl-clipboard libnotify-bin libportaudio2

# Fedora
sudo dnf install python3 wl-clipboard libnotify portaudio-devel

# Arch
sudo pacman -S python wl-clipboard libnotify portaudio
```

### Compiler whisper.cpp

```bash
git clone https://github.com/ggerganov/whisper.cpp ~/Documents/tools/whisper.cpp
cd ~/Documents/tools/whisper.cpp
cmake -B build
cmake --build build --config Release

# Télécharger un modèle (ex: large-v3 pour le français)
./models/download-ggml-model.sh large-v3
```

> 💡 Pour l'accélération GPU (CUDA, Vulkan…), consultez la [doc whisper.cpp](https://github.com/ggerganov/whisper.cpp#building).

### Permissions clavier (evdev)

L'application lit directement les événements clavier via `/dev/input/eventX`. Votre utilisateur doit avoir accès en lecture :

```bash
sudo usermod -aG input $USER
```

Puis **déconnectez-vous et reconnectez-vous** pour que le changement prenne effet.

---

## Installation

```bash
git clone https://github.com/Aytirix/DictateToText.git
cd DictateToText

# Crée le venv et installe les dépendances Python
make install
```

---

## Utilisation

### Lancement rapide (avant-plan)

```bash
make run
```

### En tant que service systemd (recommandé)
#### Créer le fichier service, l'activer au démarrage, et le lancer

```bash
make service && make enable
```

Commandes utiles :

```bash
make status       # Statut du service
make logs         # 50 dernières lignes de logs
make logs-follow  # Logs en temps réel
make restart      # Redémarrer après un changement de config
make stop         # Arrêter
make disable      # Désactiver du démarrage automatique
```

### Raccourcis clavier par défaut

| Raccourci | Action |
|-----------|--------|
| `Super + Shift + F23` (touche Copilot) | **Maintenir** pour enregistrer, **relâcher** pour transcrire |
| `Ctrl + Shift + H` | Ouvrir la fenêtre d'historique |

> 💡 La touche `F23` correspond à la touche **Copilot** des claviers Microsoft Surface / Modern. Vous pouvez changer les raccourcis dans la configuration.

---

## Configuration

La configuration est stockée dans :

```
config/dictate_ptt_copilot/config.json
```

Elle est créée automatiquement au premier lancement avec les valeurs par défaut. Vous pouvez aussi la modifier via la fenêtre de paramètres (`Ctrl+Shift+H` → onglet Paramètres).

### Paramètres principaux

| Paramètre | Défaut | Description |
|-----------|--------|-------------|
| `whisper_model` | `"large-v3"` | Modèle Whisper (`tiny`, `base`, `small`, `medium`, `large-v1/v2/v3`, `large-v3-turbo`, variantes `.en` et quantifiées selon votre version de `whisper.cpp`) |
| `language` | `"fr"` | Langue de transcription |
| `beam_size` | `5` | Taille du faisceau (plus grand = plus précis, plus lent) |
| `initial_prompt` | `""` | Contexte pour améliorer la transcription |
| `record_combo` | `["KEY_LEFTMETA", "KEY_LEFTSHIFT", "KEY_F23"]` | Combo d'enregistrement (noms evdev) |
| `history_combo` | `["KEY_LEFTCTRL", "KEY_LEFTSHIFT", "KEY_H"]` | Combo pour l'historique |
| `input_event` | `"/dev/input/event3"` | Périphérique clavier — à adapter à votre machine |
| `sample_rate` | `16000` | Fréquence d'échantillonnage audio |
| `history_size` | `10` | Nombre max d'éléments dans l'historique |
| `save_audio_files` | `false` | Sauvegarder les fichiers WAV |
| `task` | `"transcribe"` | `"transcribe"` ou `"translate"` (vers l'anglais) |

> ℹ️ La liste complète des paramètres est documentée dans [docs/CONFIG_README.md](docs/CONFIG_README.md).

### Identifier votre périphérique clavier

```bash
# Lister les périphériques d'entrée
cat /proc/bus/input/devices

# Ou tester interactivement
sudo evtest
```

Cherchez votre clavier et notez le numéro `eventX`, puis mettez à jour `input_event` dans la config.

---

## Architecture

```
dictate_ptt_copilot.py          ← Point d'entrée
├── app_config.py               ← Configuration (dataclass + validation)
├── application.py              ← Orchestrateur principal
├── config.py                   ← Gestionnaire JSON (defaults, load, save)
│
├── services/
│   ├── transcription.py        ← Appel whisper-cli (subprocess)
│   ├── clipboard.py            ← wl-copy (Wayland)
│   └── notification.py         ← notify-send
│
├── components/
│   ├── keyboard_handler.py     ← Lecture evdev, détection des combos
│   ├── audio_recorder.py       ← Capture audio (sounddevice)
│   ├── transcription_worker.py ← Worker thread + queue
│   └── history_manager.py      ← Historique avec observer pattern
│
└── ui/
    ├── history_window_ctk.py   ← Fenêtre historique (4 onglets)
    └── settings_window_ctk.py  ← Fenêtre paramètres
```

**Flux de données** :

1. Le **thread principal** lance le mainloop Tkinter (root cachée)
2. Un **thread daemon** écoute le clavier via evdev
3. Appui sur le combo → `AudioRecorder.start_recording()`
4. Relâchement → `AudioRecorder.stop_recording()` → fichier WAV
5. Le WAV est soumis au `TranscriptionWorker` (thread + queue)
6. `TranscriptionService` appelle `whisper-cli` en subprocess
7. Le texte transcrit est copié dans le presse-papiers + ajouté à l'historique + notification

---

## Commandes Make

```
  Développement
    install         Créer le venv (si besoin) et installer les dépendances
    run             Lancer le programme en avant-plan (hors service)
    compile         Vérifier la syntaxe de tous les .py

  Service systemd
    service         Créer / mettre à jour le fichier service systemd
    enable          Activer le service au démarrage
    disable         Désactiver le service au démarrage
    start           Démarrer le service
    stop            Arrêter le service
    restart         Redémarrer le service
    status          Afficher le statut du service
    logs            Afficher les derniers logs (50 lignes)
    logs-follow     Suivre les logs en temps réel

  Maintenance
    clean           Supprimer les fichiers temporaires et __pycache__
```

---

## Dépannage

### Le service ne démarre pas

```bash
make status
make logs
```

Vérifiez que les variables Wayland sont disponibles :
```bash
systemctl --user show-environment | grep WAYLAND
```

### Pas de son / périphérique audio non trouvé

```bash
# Vérifier que PipeWire tourne
systemctl --user status pipewire

# Lister les périphériques audio
python3 -c "import sounddevice; print(sounddevice.query_devices())"
```

### Erreur de permission evdev

```bash
# Vérifier l'accès au device
ls -la /dev/input/event3

# S'assurer que l'utilisateur est dans le groupe input
groups $USER
```

### Transcription vide ou mauvaise

- Essayez un plus grand modèle (`"large-v3"` au lieu de `"base"`)
- Ajoutez un `initial_prompt` adapté à votre vocabulaire
- Augmentez `beam_size` (au prix de la vitesse)

---

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
