"""Application configuration"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Set

from evdev import InputDevice, ecodes, list_devices
import config as cfg_module


@dataclass
class AppConfig:
	"""Application configuration"""
	input_event: str = "/dev/input/event3"
	whisper_bin: str = None
	whisper_model: str = None
	whisper_path: str = None
	language: str = "fr"
	sample_rate: int = 16000
	channels: int = 1
	copilot_combo: Set[int] = None
	history_combo: Set[int] = None

	def __post_init__(self):
		self.reload()

	def reload(self) -> None:
		"""Reload runtime configuration from disk."""
		# Load from config
		cfg = cfg_module.get_config_instance()

		# Combos from config (convert string key names to evdev codes)
		record_keys = cfg.get("record_combo", ["KEY_LEFTMETA", "KEY_LEFTSHIFT", "KEY_F23"])
		history_keys = cfg.get("history_combo", ["KEY_LEFTCTRL", "KEY_LEFTSHIFT", "KEY_H"])
		self.copilot_combo = {getattr(ecodes, k, None) for k in record_keys} - {None}
		self.history_combo = {getattr(ecodes, k, None) for k in history_keys} - {None}

		# Fallback if config keys were invalid
		if not self.copilot_combo:
			self.copilot_combo = {ecodes.KEY_LEFTMETA, ecodes.KEY_LEFTSHIFT, ecodes.KEY_F23}
		if not self.history_combo:
			self.history_combo = {ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_H}

		self.input_event = cfg.get("input_event", "/dev/input/event3")
		self.whisper_path = os.path.expanduser(cfg.get("whisper_path", "~/Documents/tools/whisper.cpp"))
		model_name = cfg.get("whisper_model", "large-v3")
		self.language = cfg.get("language", "fr")
		self.sample_rate = cfg.get("sample_rate", 16000)
		self.channels = cfg.get("channels", 1)

		# Build paths
		self.whisper_bin = os.path.join(self.whisper_path, "build/bin/whisper-cli")
		self.whisper_model = os.path.join(self.whisper_path, f"models/ggml-{model_name}.bin")

	def validate(self) -> None:
		"""Validate configuration paths"""
		if not self._has_readable_keyboard_device():
			raise PermissionError(
				"Aucun périphérique clavier lisible. "
				"Ajoutez votre utilisateur au groupe input: sudo usermod -aG input $USER, "
				"puis déconnectez-vous et reconnectez-vous."
			)
		if not Path(self.whisper_bin).exists():
			raise FileNotFoundError(f"whisper-cli introuvable: {self.whisper_bin}")
		if not Path(self.whisper_model).exists():
			raise FileNotFoundError(f"Modèle introuvable: {self.whisper_model}")

	def _has_readable_keyboard_device(self) -> bool:
		"""Return True when at least one keyboard-like input device is readable."""
		for path in [self.input_event, *list_devices()]:
			try:
				device = InputDevice(path)
				keys = device.capabilities().get(ecodes.EV_KEY, [])
			except OSError:
				continue

			if isinstance(keys, list) and keys:
				return True
		return False
