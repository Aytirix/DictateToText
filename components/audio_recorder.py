"""Audio recording component"""

import os
import time
import threading
from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf

import config as cfg_module
from app_config import AppConfig


class AudioRecorder:
	"""Handle audio recording"""

	def __init__(self, cfg: AppConfig):
		self.config = cfg
		self._recording = False
		self._frames = []
		self._lock = threading.Lock()
		self._stream = None

	def start_stream(self) -> None:
		"""Start audio input stream"""
		self._stream = sd.InputStream(samplerate=self.config.sample_rate,
		                              channels=self.config.channels,
		                              dtype="int16",
		                              callback=self._audio_callback)
		self._stream.start()

	def stop_stream(self) -> None:
		"""Stop audio input stream"""
		if self._stream:
			self._stream.close()
			self._stream = None

	def _audio_callback(self, indata, frames_count, time_info, status):
		"""Audio callback for recording"""
		if self._recording:
			with self._lock:
				self._frames.append(indata.copy())

	def start_recording(self) -> bool:
		"""Start recording audio"""
		if self._recording:
			# Already recording — ignore, don't cancel
			return False

		with self._lock:
			self._frames = []
		self._recording = True
		print("🎙️  REC (Copilot maintenu)...", flush=True)
		return True

	def stop_recording(self) -> Optional[str]:
		"""Stop recording and save to file"""
		self._recording = False

		with self._lock:
			if not self._frames:
				print("⏹️  Stop (rien).", flush=True)
				return None
			audio = np.concatenate(self._frames, axis=0)
			self._frames = []

		cfg = cfg_module.get_config_instance()
		timestamp = int(time.time() * 1000)

		# Determine save location
		if cfg.get("save_audio_files", False):
			audio_dir = Path(cfg.get("audio_temp_dir", "~/Documents/tools/py/audio_temp")).expanduser()
			audio_dir.mkdir(parents=True, exist_ok=True)
			wav_file = str(audio_dir / f"dictate_ptt_{timestamp}.wav")
		else:
			wav_file = f"/tmp/dictate_ptt_{timestamp}.wav"

		sf.write(wav_file, audio, self.config.sample_rate, subtype="PCM_16")
		print("⏹️  Stop → ajout à la queue…", flush=True)

		return wav_file

	@property
	def is_recording(self) -> bool:
		return self._recording
