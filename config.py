#!/usr/bin/env python3
"""Configuration complète pour Dictate PTT Copilot"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

CONFIG_FILE = Path("~/Documents/tools/py/config/dictate_ptt_copilot/config.json").expanduser()

# Valeurs par défaut complètes
DEFAULT_CONFIG = {
    # Interface & Thème
    "theme_mode": "dark",  # "dark", "light", "system"
    "accent_color": "blue",  # "blue", "green", "red", "violet", "orange"
    "window_opacity": 1.0,
    "font_family": "Segoe UI",
    "font_size": 12,
    "animations_enabled": True,
    "corner_radius": 10,
    "ui_scaling": 1.0,

    # Audio & Enregistrement
    "sample_rate": 16000,
    "channels": 1,
    "audio_format": "wav",
    "noise_reduction": False,
    "auto_gain": False,
    "silence_threshold": 0.01,
    "audio_device_index": None,  # None = défaut du système

    # Whisper & Transcription
    "whisper_model": "large-v3",  # "tiny", "base", "small", "medium", "large-v1/v2/v3"
    "language": "fr",
    "task": "transcribe",  # "transcribe" ou "translate"
    "temperature": 0.0,
    "beam_size": 5,
    "best_of": 5,
    "initial_prompt": "",
    "word_timestamps": False,
    "vad_filter": False,
    "compute_type": "float16",  # "int8", "float16", "float32"

    # Raccourcis Clavier
    "record_combo": ["KEY_LEFTMETA", "KEY_LEFTSHIFT", "KEY_F23"],
    "history_combo": ["KEY_LEFTCTRL", "KEY_LEFTSHIFT", "KEY_H"],

    # Presse-papiers & Sortie
    "add_prefix": "",
    "add_suffix": "",
    "clipboard_timeout": 0,  # secondes, 0 = illimité

    # Historique
    "history_size": 10,
    "history_persistence": True,
    "history_search": True,
    "history_export_format": "txt",  # "txt", "json", "csv"
    "history_auto_clear_days": 0,  # 0 = jamais
    "history": [],

    # Notifications & Feedback
    "notifications_enabled": True,
    "notification_position": "top-right",  # "top-right", "top-left", "bottom-right", "bottom-left"
    "notification_duration": 3,  # secondes
    "visual_feedback": True,
    "tray_icon": True,

    # Comportement
    "recording_mode": "push_to_talk",  # "push_to_talk" ou "toggle"
    "auto_start": False,
    "minimize_to_tray": False,
    "close_to_tray": False,

    # Debug & Logs
    "log_level": "info",  # "debug", "info", "warning", "error"
    "log_to_file": False,
    "log_file_path": "~/Documents/tools/py/logs/dictate_ptt.log",
    "show_console": False,
    "performance_monitoring": False,
    "save_audio_files": False,
    "audio_temp_dir": "~/Documents/tools/py/audio_temp",

    # Chemins
    "whisper_path": "~/Documents/tools/whisper.cpp",
    "whisper_bin": "~/Documents/tools/whisper.cpp/build/bin/whisper-cli",
    "whisper_models_dir": "~/Documents/tools/whisper.cpp/models",
    "input_event": "/dev/input/event3",
}


class Config:
	"""Gestionnaire de configuration"""

	def __init__(self):
		self._config = self._load()

	def _load(self) -> Dict[str, Any]:
		"""Charge la configuration depuis le fichier JSON"""
		if CONFIG_FILE.exists():
			try:
				with open(CONFIG_FILE, "r") as f:
					config = json.load(f)
					# Fusionner avec les valeurs par défaut
					return {**DEFAULT_CONFIG, **config}
			except Exception as e:
				print(f"⚠️  Erreur lecture config: {e}")
				return DEFAULT_CONFIG.copy()
		return DEFAULT_CONFIG.copy()

	def save(self) -> bool:
		"""Sauvegarde la configuration dans le fichier JSON"""
		try:
			CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
			with open(CONFIG_FILE, "w") as f:
				json.dump(self._config, f, indent=2, ensure_ascii=False)
			return True
		except Exception as e:
			print(f"❌ Erreur sauvegarde config: {e}")
			return False

	def get(self, key: str, default: Any = None) -> Any:
		"""Récupère une valeur de configuration"""
		return self._config.get(key, default)

	def set(self, key: str, value: Any) -> bool:
		"""Définit une valeur de configuration et sauvegarde"""
		self._config[key] = value
		return self.save()

	def update(self, updates: Dict[str, Any]) -> bool:
		"""Met à jour plusieurs valeurs"""
		self._config.update(updates)
		return self.save()

	def reset(self) -> bool:
		"""Réinitialise à la configuration par défaut"""
		self._config = DEFAULT_CONFIG.copy()
		return self.save()

	def get_all(self) -> Dict[str, Any]:
		"""Retourne toute la configuration"""
		return self._config.copy()

	# Accesseurs spécifiques pour compatibilité avec l'ancien code
	def get_history(self):
		"""Retourne l'historique"""
		return self._config.get("history", [])

	def save_history(self, history):
		"""Sauvegarde l'historique"""
		return self.set("history", history)

	def get_history_size(self):
		"""Retourne la taille maximale de l'historique"""
		return self._config.get("history_size", 10)

	def set_history_size(self, size):
		"""Définit la taille maximale de l'historique"""
		return self.set("history_size", size)


# Instance globale
_config_instance = Config()


# Fonctions pour compatibilité avec l'ancien code
def load_config():
	return _config_instance.get_all()


def save_config(config):
	return _config_instance.update(config)


def get_history():
	return _config_instance.get_history()


def save_history(history):
	return _config_instance.save_history(history)


def get_history_size():
	return _config_instance.get_history_size()


def set_history_size(size):
	return _config_instance.set_history_size(size)


# Export pour usage avancé
def get_config_instance() -> Config:
	"""Retourne l'instance de configuration"""
	return _config_instance
