"""Application configuration"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Set

from evdev import ecodes
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
		if self.copilot_combo is None:
			self.copilot_combo = {ecodes.KEY_LEFTMETA, ecodes.KEY_LEFTSHIFT, ecodes.KEY_F23}
		if self.history_combo is None:
			self.history_combo = {ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_H}

		# Load from config
		cfg = cfg_module.get_config_instance()
		self.whisper_path = os.path.expanduser(cfg.get("whisper_path", "~/Documents/tools/whisper.cpp"))
		model_name = cfg.get("whisper_model", "large-v3")
		self.language = cfg.get("language", "fr")
		self.sample_rate = cfg.get("sample_rate", 16000)

		# Build paths
		self.whisper_bin = os.path.join(self.whisper_path, "build/bin/whisper-cli")
		self.whisper_model = os.path.join(self.whisper_path, f"models/ggml-{model_name}.bin")

	def validate(self) -> None:
		"""Validate configuration paths"""
		if not Path(self.input_event).exists():
			raise FileNotFoundError(f"Device introuvable: {self.input_event}")
		if not Path(self.whisper_bin).exists():
			raise FileNotFoundError(f"whisper-cli introuvable: {self.whisper_bin}")
		if not Path(self.whisper_model).exists():
			raise FileNotFoundError(f"Modèle introuvable: {self.whisper_model}")
