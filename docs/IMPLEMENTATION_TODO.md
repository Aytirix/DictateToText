# Suivi d'implémentation des paramètres

**Dernière mise à jour** : 8 janvier 2026  
**Statut global** : 18/39 paramètres non implémentés

## Légende
- 🔴 **Non commencé** - Paramètre défini mais pas du tout utilisé
- 🟡 **En cours** - Paramètre partiellement implémenté
- 🟢 **Terminé** - Paramètre complètement fonctionnel
- ⚠️ **Bloqué** - Nécessite décision ou dépendance externe

---

## 1. Interface & Thème (6/6 non implémentés)

### 🔴 `window_opacity` (0.8-1.0)
**Priorité** : Basse  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `ui/history_window_ctk.py` - Ajouter `self.window.attributes('-alpha', opacity)`
- `ui/settings_window_ctk.py` - Ajouter slider de configuration

**Notes** : CustomTkinter supporte l'opacité via `attributes('-alpha')`

---

### 🔴 `font_family` (Police personnalisée)
**Priorité** : Basse  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `ui/history_window_ctk.py` - Appliquer `ctk.CTkFont(family=font_family)`
- `ui/settings_window_ctk.py` - Appliquer `ctk.CTkFont(family=font_family)`
- Tous les widgets de texte

**Notes** : Actuellement utilise police par défaut système

---

### 🔴 `font_size` (Taille globale)
**Priorité** : Moyenne  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `ui/history_window_ctk.py` - Utiliser `cfg.get("font_size")` dans tous les CTkFont
- `ui/settings_window_ctk.py` - Idem

**Notes** : Actuellement les tailles sont hardcodées (12, 14, 16, etc.)

---

### 🔴 `animations_enabled` (Activer animations)
**Priorité** : Basse  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `ui/history_window_ctk.py` - Conditionner les `.after()` et transitions
- `ui/settings_window_ctk.py` - Idem

**Notes** : CustomTkinter a peu d'animations, principalement les hover effects

---

### 🔴 `corner_radius` (Rayon coins arrondis 0-20px)
**Priorité** : Basse  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `ui/history_window_ctk.py` - Remplacer `corner_radius=10` par `cfg.get("corner_radius")`
- `ui/settings_window_ctk.py` - Idem

**Notes** : Valeur actuellement hardcodée à 10px partout

---

### 🔴 `ui_scaling` (Zoom interface 0.8-1.5x)
**Priorité** : Moyenne  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `ui/history_window_ctk.py` - Ajouter `ctk.set_widget_scaling(ui_scaling)` au démarrage
- `ui/settings_window_ctk.py` - Idem

**Notes** : CustomTkinter supporte nativement le scaling

---

## 2. Audio & Enregistrement (5/5 non implémentés)

### 🔴 `audio_format` (Format: wav/mp3/flac)
**Priorité** : Basse  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `components/audio_recorder.py` - Changer `sf.write()` format selon config
- Vérifier compatibilité Whisper

**Notes** : Actuellement forcé à WAV PCM_16. Whisper supporte plusieurs formats.

---

### 🟡 `noise_reduction` (Réduction de bruit)
**Priorité** : Haute  
**Difficulté** : Difficile  
**Fichiers à modifier** :
- `components/audio_recorder.py` - Intégrer traitement audio (noisereduce, librosa)
- Ajouter dépendance `noisereduce` dans requirements

**Notes** : Paramètre dans settings mais pas appliqué. Nécessite bibliothèque externe.

---

### 🟡 `auto_gain` (Normalisation volume)
**Priorité** : Moyenne  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `components/audio_recorder.py` - Normaliser amplitude avant sauvegarde

**Notes** : Paramètre dans settings mais pas appliqué. Simple traitement NumPy.

```python
# Exemple implémentation
if cfg.get("auto_gain"):
    audio = audio / np.max(np.abs(audio)) * 0.9
```

---

### 🔴 `silence_threshold` (Seuil de silence 0.0-1.0)
**Priorité** : Moyenne  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `components/audio_recorder.py` - Détecter silence et couper début/fin automatiquement

**Notes** : Utile pour éviter enregistrement vide. Nécessite calcul RMS.

---

### 🔴 `audio_device_index` (Index microphone)
**Priorité** : Haute  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `components/audio_recorder.py` - Ajouter `device=audio_device_index` dans `sd.InputStream()`
- `ui/settings_window_ctk.py` - Ajouter liste déroulante des devices disponibles

**Notes** : Actuellement utilise device par défaut. Utile pour multi-micros.

```python
# Liste devices disponibles
devices = sd.query_devices()
```

---

## 3. Whisper & Transcription (8/8 non implémentés)

### 🔴 `task` ("transcribe" ou "translate")
**Priorité** : Moyenne  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `services/transcription.py` - Ajouter option `-tr` à la commande whisper

**Notes** : Permet traduction automatique vers anglais

```python
if cfg.get("task") == "translate":
    cmd += ["-tr"]
```

---

### 🔴 `temperature` (Créativité 0.0-1.0)
**Priorité** : Basse  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `services/transcription.py` - Ajouter `--temperature` à cmd whisper

**Notes** : Contrôle le sampling. 0.0 = déterministe, >0 = créatif.

---

### 🟡 `beam_size` (Qualité vs vitesse 1-10)
**Priorité** : Moyenne  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `services/transcription.py` - Ajouter `-bs <beam_size>` à cmd whisper

**Notes** : Paramètre dans settings mais pas passé à whisper-cli.

```python
beam_size = cfg.get("beam_size", 5)
cmd += ["-bs", str(beam_size)]
```

---

### 🔴 `best_of` (Nombre tentatives 1-5)
**Priorité** : Basse  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `services/transcription.py` - Ajouter `-bo <best_of>` à cmd whisper

**Notes** : Whisper.cpp peut essayer plusieurs décodages et prendre le meilleur.

---

### 🔴 `initial_prompt` (Contexte/vocabulaire)
**Priorité** : Haute  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `services/transcription.py` - Ajouter `--prompt "..."` à cmd whisper

**Notes** : Très utile pour vocabulaire technique/médical. Améliore précision.

```python
prompt = cfg.get("initial_prompt", "")
if prompt:
    cmd += ["--prompt", prompt]
```

---

### 🔴 `word_timestamps` (Timestamps par mot)
**Priorité** : Basse  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `services/transcription.py` - Ajouter `-ml 1` pour timestamps
- Modifier `_clean_output()` pour parser les timestamps

**Notes** : Retourne format `[00:00.000 --> 00:01.500] mot`. Utile pour sous-titres.

---

### 🔴 `vad_filter` (Voice Activity Detection)
**Priorité** : Moyenne  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `services/transcription.py` - Vérifier si whisper.cpp supporte VAD intégré
- Alternative : Utiliser WebRTC VAD en preprocessing

**Notes** : Supprime automatiquement les silences. Peut améliorer vitesse.

---

### 🔴 `compute_type` (int8/float16/float32)
**Priorité** : Moyenne  
**Difficulté** : Difficile  
**Fichiers à modifier** :
- `services/transcription.py` - Vérifier flags whisper.cpp pour quantization
- Peut nécessiter recompilation de whisper.cpp avec flags spécifiques

**Notes** : int8 = rapide mais moins précis, float32 = lent mais précis.

---

## 4. Presse-papiers & Sortie (3/3 non implémentés)

### 🔴 `add_prefix` (Texte avant)
**Priorité** : Moyenne  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `components/transcription_worker.py` - Modifier texte avant `ClipboardService.copy()`

**Notes** : Utile pour ajouter "Dictée : " ou autre préfixe automatique.

```python
prefix = cfg.get("add_prefix", "")
suffix = cfg.get("add_suffix", "")
final_text = f"{prefix}{text}{suffix}"
```

---

### 🔴 `add_suffix` (Texte après)
**Priorité** : Moyenne  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `components/transcription_worker.py` - Modifier texte avant `ClipboardService.copy()`

**Notes** : Utile pour ajouter ponctuation automatique.

---

### 🔴 `clipboard_timeout` (Durée dans clipboard, 0=illimité)
**Priorité** : Basse  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `services/clipboard.py` - Implémenter timer qui vide le clipboard après X secondes

**Notes** : Nécessite thread séparé pour monitorer le temps. Utilité discutable.

---

## 5. Historique (1/1 non implémenté)

### 🔴 `history_auto_clear_days` (Vider après X jours, 0=jamais)
**Priorité** : Basse  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `components/history_manager.py` - Ajouter timestamp aux entrées
- Au chargement, filtrer entrées > X jours

**Notes** : Nécessite refonte format historique pour inclure timestamps.

```python
# Format actuel : ["texte1", "texte2"]
# Format nécessaire : [{"text": "texte1", "timestamp": 1234567890}, ...]
```

---

## 6. Notifications & Feedback (4/4 non implémentés)

### 🔴 `notification_position` (Position à l'écran)
**Priorité** : Basse  
**Difficulté** : Difficile  
**Fichiers à modifier** :
- `services/notification.py` - Remplacer `notify-send` par solution custom
- Option : Utiliser `plyer` ou créer overlay Tkinter

**Notes** : `notify-send` ne supporte pas position personnalisée sous Linux.

---

### 🟡 `notification_duration` (Durée affichage secondes)
**Priorité** : Basse  
**Difficulté** : Difficile  
**Fichiers à modifier** :
- `services/notification.py` - Ajouter `-t <ms>` à notify-send

**Notes** : Paramètre dans settings. `notify-send` supporte `-t` mais pas toujours respecté par le DE.

```python
duration_ms = cfg.get("notification_duration", 3) * 1000
subprocess.Popen(["notify-send", "-t", str(duration_ms), title, body])
```

---

### 🔴 `visual_feedback` (Indicateur visuel)
**Priorité** : Moyenne  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `application.py` - Créer overlay transparent Tkinter pendant enregistrement
- Afficher indicateur rouge "REC" en coin d'écran

**Notes** : Améliore UX. Alternative : changer couleur tray icon.

---

### 🔴 `tray_icon` (Icône barre système)
**Priorité** : Haute  
**Difficulté** : Difficile  
**Fichiers à modifier** :
- `application.py` - Intégrer `pystray` pour system tray
- Ajouter menu contextuel (Afficher, Paramètres, Quitter)

**Notes** : Nécessite dépendance `pystray`. Important pour `minimize_to_tray`.

---

## 7. Comportement (4/4 non implémentés)

### 🟡 `recording_mode` ("push_to_talk" ou "toggle")
**Priorité** : Moyenne  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `components/keyboard_handler.py` - Modifier logique press/release
- Mode toggle : 1er appui = start, 2ème appui = stop

**Notes** : Paramètre dans settings mais toggle non implémenté.

```python
if mode == "toggle":
    if not recording:
        start_recording()
    else:
        stop_recording()
```

---

### 🟡 `auto_start` (Lancer au démarrage)
**Priorité** : Haute  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `ui/settings_window_ctk.py` - Créer/supprimer fichier autostart
- Linux : `~/.config/autostart/dictate-ptt.desktop`
- Attention : conflit possible avec systemd service

**Notes** : Paramètre dans settings. Doit modifier fichiers système.

```python
autostart_path = Path.home() / ".config/autostart/dictate-ptt.desktop"
if enable:
    autostart_path.write_text(desktop_entry_content)
else:
    autostart_path.unlink(missing_ok=True)
```

---

### 🔴 `minimize_to_tray` (Minimiser vers barre système)
**Priorité** : Moyenne  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `ui/history_window_ctk.py` - Intercepter événement minimize
- Cacher fenêtre au lieu de minimiser si option activée

**Notes** : Nécessite `tray_icon` implémenté d'abord. Dépendance bloquante.

---

### 🔴 `close_to_tray` (Fermer vers barre système)
**Priorité** : Basse  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `ui/history_window_ctk.py` - Intercepter `protocol("WM_DELETE_WINDOW")`
- Cacher au lieu de fermer si option activée

**Notes** : Nécessite `tray_icon` implémenté d'abord. Dépendance bloquante.

---

## 8. Debug & Logs (5/5 non implémentés)

### 🟡 `log_level` (debug/info/warning/error)
**Priorité** : Haute  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `dictate_ptt_copilot.py` - Configurer module `logging` avec niveau
- Remplacer tous les `print()` par `logger.info()`, `logger.debug()`, etc.

**Notes** : Paramètre dans settings. Nécessite refonte logging complet.

```python
import logging
level = getattr(logging, cfg.get("log_level", "INFO").upper())
logging.basicConfig(level=level)
```

---

### 🟡 `log_to_file` (Sauvegarder logs)
**Priorité** : Haute  
**Difficulté** : Facile  
**Fichiers à modifier** :
- `dictate_ptt_copilot.py` - Ajouter `FileHandler` au logger

**Notes** : Paramètre dans settings. Dépend de `log_level` implémenté.

```python
if cfg.get("log_to_file"):
    log_path = Path(cfg.get("log_file_path")).expanduser()
    handler = logging.FileHandler(log_path)
    logging.getLogger().addHandler(handler)
```

---

### 🔴 `log_file_path` (Chemin fichier log)
**Priorité** : Moyenne  
**Difficulté** : Facile  
**Fichiers à modifier** :
- Aucun (utilisé par `log_to_file`)

**Notes** : Dépend de `log_to_file` implémenté.

---

### 🔴 `show_console` (Console de debug)
**Priorité** : Basse  
**Difficulté** : Moyenne  
**Fichiers à modifier** :
- `dictate_ptt_copilot.py` - Créer fenêtre Tkinter séparée avec Text widget
- Rediriger stdout/stderr vers cette fenêtre

**Notes** : Utile pour debug sans terminal. Alternative : utiliser logs.

---

### 🔴 `performance_monitoring` (Monitoring CPU/GPU/RAM)
**Priorité** : Basse  
**Difficulté** : Difficile  
**Fichiers à modifier** :
- `ui/history_window_ctk.py` - Onglet Stats déjà présent, ajouter plus de métriques
- Utiliser `psutil` pour CPU/RAM, `nvidia-smi` pour GPU

**Notes** : Déjà partiellement implémenté dans onglet Stats. À compléter.

---

## Plan d'implémentation recommandé

### Phase 1 : Corrections Audio (Priorité Haute)
1. ✅ `audio_device_index` - Sélection microphone
2. ✅ `auto_gain` - Normalisation volume
3. ✅ `noise_reduction` - Réduction bruit

### Phase 2 : Amélioration Whisper (Priorité Haute)
4. ✅ `initial_prompt` - Contexte vocabulaire
5. ✅ `beam_size` - Connecter au transcriptor
6. ✅ `task` - Transcribe/Translate

### Phase 3 : Interface (Priorité Moyenne)
7. ✅ `tray_icon` - Icône système (BLOQUANT pour autres)
8. ✅ `auto_start` - Démarrage auto
9. ✅ `recording_mode` - Toggle mode
10. ✅ `font_size` - Taille police globale
11. ✅ `ui_scaling` - Zoom interface

### Phase 4 : Logs & Debug (Priorité Haute)
12. ✅ `log_level` - Niveaux logging
13. ✅ `log_to_file` - Fichier logs

### Phase 5 : Presse-papiers (Priorité Moyenne)
14. ✅ `add_prefix` / `add_suffix` - Texte avant/après
15. ✅ `notification_duration` - Durée notifs

### Phase 6 : Polish (Priorité Basse)
16. ✅ `minimize_to_tray` / `close_to_tray`
17. ✅ `visual_feedback` - Indicateur REC
18. ✅ Paramètres restants selon besoins

---

## Dépendances Python à ajouter

```txt
# requirements.txt additions
noisereduce>=2.0.0      # noise_reduction
pystray>=0.19.0         # tray_icon
pillow>=10.0.0          # tray_icon (images)
psutil>=5.9.0           # performance_monitoring
```

---

## Notes générales

- **Tests nécessaires** : Chaque paramètre doit être testé individuellement
- **Documentation** : Mettre à jour CONFIG_README.md avec exemples d'usage
- **Compatibilité** : Vérifier compatibilité Linux (Wayland vs X11)
- **Performance** : Mesurer impact des traitements audio sur latence
- **UX** : Certains paramètres peuvent nécessiter restart du service

---

**Prochaine révision** : À compléter après chaque implémentation
