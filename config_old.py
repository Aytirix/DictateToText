#!/usr/bin/env python3
"""Configuration pour Dictate PTT Copilot"""

import json
from pathlib import Path

CONFIG_FILE = Path("~/Documents/tools/py/config/dictate_ptt_copilot/config.json").expanduser()

# Valeurs par défaut
DEFAULT_CONFIG = {"history_size": 10, "history": []}


def load_config():
	"""Charge la configuration depuis le fichier JSON"""
	if CONFIG_FILE.exists():
		try:
			with open(CONFIG_FILE, "r") as f:
				config = json.load(f)
				# Fusionner avec les valeurs par défaut pour les clés manquantes
				return {**DEFAULT_CONFIG, **config}
		except Exception as e:
			print(f"Erreur lecture config: {e}")
			return DEFAULT_CONFIG.copy()
	return DEFAULT_CONFIG.copy()


def save_config(config):
	"""Sauvegarde la configuration dans le fichier JSON"""
	try:
		CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
		with open(CONFIG_FILE, "w") as f:
			json.dump(config, f, indent=2, ensure_ascii=False)
		return True
	except Exception as e:
		print(f"Erreur sauvegarde config: {e}")
		return False


# Configuration globale
config = load_config()


def get_history_size():
	"""Retourne la taille maximale de l'historique"""
	return config.get("history_size", DEFAULT_CONFIG["history_size"])


def set_history_size(size):
	"""Définit la taille maximale de l'historique"""
	config["history_size"] = size
	return save_config(config)


def get_history():
	"""Retourne l'historique sauvegardé"""
	return config.get("history", [])


def save_history(history_list):
	"""Sauvegarde l'historique"""
	config["history"] = history_list
	return save_config(config)
	return save_config(config)
