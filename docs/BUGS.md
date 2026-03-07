# 🐛 Suivi des bugs — Dictate PTT Copilot

**Dernière mise à jour** : 7 mars 2026 — **15/15 bugs corrigés** ✅

## Légende statuts
- 🔴 **En attente** — Pas encore corrigé
- 🟡 **En cours** — Correction en cours
- 🟢 **Fait** — Corrigé et vérifié

---

## Bug #1 — Threading Tkinter : l'historique bloque la boucle clavier
**Statut** : � Fait  
**Sévérité** : Critique  

**Description** :  
`_show_history()` est appelé depuis le thread de la boucle evdev (écoute clavier). Il crée la fenêtre Tkinter dans ce thread secondaire, puis appelle `mainloop()` qui est bloquant. Résultat : tant que la fenêtre d'historique est ouverte, la boucle clavier est figée. Plus aucun enregistrement n'est possible. C'est la cause principale du "ça remplit pas l'historique".

**Fichiers concernés** : `application.py` (lignes 87-98)

**Commentaire post-correction** :  
Architecture réécrite : `run()` crée une root CTk cachée (`withdraw()`) dans le thread principal et lance `mainloop()`. La boucle evdev tourne dans un thread daemon. Les appels Tkinter depuis le thread evdev passent par `self._root.after(0, callback)`. L'enregistrement fonctionne pendant que l'historique est ouvert.

---

## Bug #2 — `_show_history()` bloque le event loop principal
**Statut** : � Fait  
**Sévérité** : Critique  

**Description** :  
`self._history_window.run()` appelle `window.mainloop()` qui est bloquant. Pendant ce temps, `_event_loop()` dans `run()` est interrompu. L'application ne fait rien d'autre tant que la fenêtre est ouverte. C'est lié au bug #1 mais distinct : même si le threading est corrigé, il faut que le mainloop Tkinter et la boucle evdev coexistent.

**Fichiers concernés** : `application.py` (ligne 98)

**Commentaire post-correction** :  
`HistoryWindow.run()` supprimé. La fenêtre est créée via `CTkToplevel` (pas de `mainloop()` propre). Le thread evdev schedule l'affichage via `self._root.after(0, self._show_history)`. Le signal SIGTERM est géré dans le thread principal.

---

## Bug #3 — Multiples instances de `ctk.CTk()`
**Statut** : � Fait  
**Sévérité** : Critique  

**Description** :  
À chaque ouverture de la fenêtre historique, une nouvelle `ctk.CTk()` est créée. CustomTkinter ne supporte qu'**une seule** instance root `CTk()`. Les réouvertures successives créent des conflits Tcl internes (crash, freeze, comportements aléatoires). Il faut utiliser `ctk.CTkToplevel()` pour les fenêtres secondaires, ou garder une seule instance root.

**Fichiers concernés** : `ui/history_window_ctk.py` (ligne 71)

**Commentaire post-correction** :  
Une seule `CTk()` root cachée dans `application.py`. `HistoryWindow` utilise `CTkToplevel(root)`. Plus de conflits Tcl sur les ouvertures/fermetures multiples.

---

## Bug #4 — Les raccourcis clavier du config.json sont ignorés
**Statut** : � Fait  
**Sévérité** : Moyenne  

**Description** :  
Dans `app_config.py`, les combos clavier sont hardcodés dans `__post_init__` et les valeurs `record_combo` et `history_combo` du `config.json` ne sont jamais lues. Modifier les raccourcis dans les paramètres n'a aucun effet.

**Fichiers concernés** : `app_config.py` (lignes 26-29)

**Commentaire post-correction** :  
`__post_init__` lit `record_combo` et `history_combo` du JSON, convertit chaque nom de touche (ex: `"KEY_LEFTMETA"`) en code evdev via `getattr(ecodes, k)`. Les valeurs `None` (touches invalides) sont filtrées. Fallback sur les combos par défaut si la conversion échoue.

---

## Bug #5 — `channels` jamais lu depuis la config
**Statut** : � Fait  
**Sévérité** : Mineure  

**Description** :  
Dans `app_config.py`, `self.channels` garde toujours sa valeur par défaut `1`. Il n'est jamais mis à jour depuis `cfg.get("channels")`, contrairement à `sample_rate` et `language` qui le sont.

**Fichiers concernés** : `app_config.py` (ligne 21 vs lignes 34-36)

**Commentaire post-correction** :  
`self.channels = cfg.get("channels", 1)` ajouté dans `__post_init__`. Valeur par défaut conservée à 1 (mono) pour compatibilité whisper.

---

## Bug #6 — `input_event` hardcodé à `/dev/input/event3`
**Statut** : � Fait  
**Sévérité** : Moyenne  

**Description** :  
Le device clavier est hardcodé à `/dev/input/event3` dans la dataclass. La valeur `input_event` du `config.json` n'est jamais lue dans `__post_init__`. Si le numéro du device change (branchement USB, reboot), le programme plante.

**Fichiers concernés** : `app_config.py` (ligne 13)

**Commentaire post-correction** :  
`self.input_event = cfg.get("input_event", "/dev/input/event3")` ajouté dans `__post_init__`. Le device est maintenant configurable via JSON. La validation d'existence est assurée par `validate()`.

---

## Bug #7 — Paramètres Whisper avancés non passés à whisper-cli
**Statut** : � Fait  
**Sévérité** : Importante  

**Description** :  
La commande whisper-cli ne reçoit que le modèle, le fichier et la langue. Les paramètres `beam_size`, `initial_prompt`, `task` (translate), `best_of`, etc. sont configurés dans le JSON mais **jamais transmis** à la ligne de commande. Le modèle tourne avec ses valeurs par défaut, ce qui peut expliquer les mauvaises transcriptions.

**Fichiers concernés** : `services/transcription.py` (lignes 15-19)

**Commentaire post-correction** :  
La commande whisper-cli reçoit maintenant `-bs` (beam_size), `--prompt` (initial_prompt), et `-tr` (si task=translate). Les paramètres sont lus depuis `AppConfig` et ajoutés conditionnellement à la commande.

---

## Bug #8 — `_clean_output` peut supprimer du vrai texte dicté
**Statut** : � Fait  
**Sévérité** : Moyenne  

**Description** :  
Le filtre `bad_prefixes` contient des mots courants comme `"processing"`, `"Processing"`, `"found "`, `"Device "`. Si la dictée contient une phrase commençant par ces mots, elle sera supprimée. Le filtre `bad_contains` peut aussi couper des lignes valides si elles contiennent `"SSE"` ou `"AVX"` par hasard.

**Fichiers concernés** : `services/transcription.py` (lignes 27-88)

**Commentaire post-correction** :  
Réécrit pour n'utiliser que `stdout` (plus de mélange avec stderr). Le filtre agressif `bad_prefixes`/`bad_contains` a été supprimé. `_clean_output` ne fait plus que retirer les timestamps `[HH:MM:SS.mmm --> ...]` et joindre les lignes non-vides.

---

## Bug #9 — Pas de vérification du return code de whisper-cli
**Statut** : � Fait  
**Sévérité** : Moyenne  

**Description** :  
Après `subprocess.run()`, `result.returncode` n'est jamais vérifié. Si whisper-cli échoue (modèle introuvable, fichier corrompu, OOM), le code passe silencieusement la sortie stderr à `_clean_output` qui retourne probablement une string vide ou du garbage.

**Fichiers concernés** : `services/transcription.py` (ligne 20)

**Commentaire post-correction** :  
`result.returncode` vérifié après exécution. Si non-zéro, stderr est loggué et une string vide est retournée. `TimeoutExpired` est aussi catchée (voir bug #14).

---

## Bug #10 — `wl-copy` peut ne pas fonctionner dans le contexte systemd
**Statut** : � Fait  
**Sévérité** : Moyenne  

**Description** :  
`ClipboardService.copy()` lance `wl-copy` qui nécessite `WAYLAND_DISPLAY` et `XDG_RUNTIME_DIR`. Le service systemd utilise `PassEnvironment` pour les hériter, mais si la session graphique n'est pas encore prête ou si les variables ne sont pas exportées, `wl-copy` échoue silencieusement (le `Popen` ne vérifie pas le résultat).

**Fichiers concernés** : `services/clipboard.py`, `dictate-ptt.service`

**Commentaire post-correction** :  
Réécrit avec `subprocess.run()` + `check=False` + vérification `returncode`. Ajout de fallbacks `WAYLAND_DISPLAY` et `XDG_RUNTIME_DIR` dans l'environnement si absents. Timeout de 5s ajouté.

---

## Bug #11 — Référence `HistoryManager.items` cassée après troncature
**Statut** : � Fait  
**Sévérité** : Moyenne  

**Description** :  
`self.items = config.get_history()` récupère une référence vers la liste interne du dict config. Quand `add()` fait `self.items = self.items[-self._max_size:]` (slice), ça crée une **nouvelle liste** et casse la référence avec le dict config. Les deux divergent. `config.save_history(self.items)` resynchronise, mais entre les deux appels il y a un état incohérent.

**Fichiers concernés** : `components/history_manager.py` (lignes 10, 22)

**Commentaire post-correction** :  
Initialisation avec `list(config.get_history())` pour copie propre. Troncature avec `self.items[:] = self.items[-self._max_size:]` (modification en place, pas de réassignation). La référence reste intacte.

---

## Bug #12 — Observer pattern silencieux sur erreur
**Statut** : � Fait  
**Sévérité** : Mineure  

**Description** :  
Dans `_notify_observers()`, les exceptions sont catchées avec `except: pass`. Si la fenêtre Tkinter est dans un état invalide ou si `window.after()` échoue, on ne le saura jamais. Ça peut masquer des bugs graves.

**Fichiers concernés** : `components/history_manager.py` (lignes 42-52)

**Commentaire post-correction** :  
`_notify_observers()` vérifie `winfo_exists()` avant d'appeler `window.after()`. Les observers morts sont auto-retirés de la liste. Ajout d'une méthode `detach_observer()` pour nettoyage explicite.

---

## Bug #13 — Double-click rapide annule l'enregistrement sans feedback clair
**Statut** : � Fait  
**Sévérité** : Mineure  

**Description** :  
Dans `start_recording()`, si `self._recording` est déjà `True`, l'enregistrement est annulé et les frames sont vidées. Le message affiché dit "Enregistrement en cours annulé!" mais il n'y a pas de notification système. L'utilisateur peut perdre un enregistrement sans comprendre pourquoi.

**Fichiers concernés** : `components/audio_recorder.py` (lignes 42-47)

**Commentaire post-correction** :  
Le double-appui est maintenant **ignoré** au lieu d'annuler : `start_recording()` retourne `False` si déjà en cours d'enregistrement, sans vider les frames. L'enregistrement en cours continue normalement.

---

## Bug #14 — Pas de timeout sur `subprocess.run` pour whisper-cli
**Statut** : � Fait  
**Sévérité** : Moyenne  

**Description** :  
Si whisper-cli se bloque (modèle corrompu, fichier audio trop long, manque de RAM), `subprocess.run()` attend indéfiniment. Le worker thread est bloqué et plus aucune transcription ne peut passer. La queue se remplit sans jamais se vider.

**Fichiers concernés** : `services/transcription.py` (ligne 20)

**Commentaire post-correction** :  
`timeout=120` ajouté à `subprocess.run()`. `subprocess.TimeoutExpired` est catchée, le processus est tué et un message d'erreur est loggué. Retourne une string vide en cas de timeout.

---

## Bug #15 — `_frames` (audio) pas thread-safe
**Statut** : � Fait  
**Sévérité** : Mineure  

**Description** :  
`self._frames.append(indata.copy())` est appelé depuis le thread callback de sounddevice, tandis que `self._frames = []` est fait depuis le thread principal. Il n'y a pas de Lock. En théorie, une race condition peut faire perdre des frames audio ou causer une exception.

**Fichiers concernés** : `components/audio_recorder.py` (lignes 37-39 et 49)

**Commentaire post-correction** :  
`threading.Lock` ajouté. `_audio_callback` acquiert le lock avant `append`. `start_recording` et `stop_recording` acquièrent le lock pour vider/lire `_frames`. Pas de race condition possible.

---

## Résumé

| # | Description courte | Sévérité | Statut |
|---|--------------------|----------|--------|
| 1 | Threading Tkinter bloque la boucle clavier | Critique | � |
| 2 | `mainloop()` bloque le event loop | Critique | 🟢 |
| 3 | Multiples instances `CTk()` | Critique | 🟢 |
| 4 | Raccourcis clavier config ignorés | Moyenne | 🟢 |
| 5 | `channels` pas lu depuis config | Mineure | 🟢 |
| 6 | `input_event` hardcodé | Moyenne | 🟢 |
| 7 | Paramètres Whisper non transmis | Importante | 🟢 |
| 8 | `_clean_output` coupe du vrai texte | Moyenne | 🟢 |
| 9 | Pas de check returncode whisper | Moyenne | 🟢 |
| 10 | `wl-copy` variables d'env manquantes | Moyenne | 🟢 |
| 11 | Référence `items` cassée après troncature | Moyenne | 🟢 |
| 12 | Observer silencieux sur erreur | Mineure | 🟢 |
| 13 | Double-click ignoré au lieu d'annuler | Mineure | 🟢 |
| 14 | Pas de timeout whisper-cli | Moyenne | 🟢 |
| 15 | `_frames` pas thread-safe | Mineure | 🟢 |
