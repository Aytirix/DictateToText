"""Transcription service using Whisper"""

import subprocess

import config as cfg_module
from app_config import AppConfig


class TranscriptionService:
	"""Handle Whisper transcription"""

	def __init__(self, cfg: AppConfig):
		self.config = cfg

	def transcribe(self, wav_path: str) -> str:
		"""Transcribe audio file using Whisper"""
		cfg = cfg_module.get_config_instance()

		cmd = [self.config.whisper_bin, "-m", self.config.whisper_model, "-f", wav_path, "-nt"]
		if self.config.language != "auto":
			cmd += ["-l", self.config.language]

		# Beam size
		beam_size = cfg.get("beam_size", 5)
		cmd += ["-bs", str(beam_size)]

		# Initial prompt (very useful for French vocabulary)
		initial_prompt = cfg.get("initial_prompt", "")
		if initial_prompt:
			cmd += ["--prompt", initial_prompt]

		# Translate mode
		if cfg.get("task", "transcribe") == "translate":
			cmd += ["-tr"]

		try:
			result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
		except subprocess.TimeoutExpired:
			print("❌ Timeout whisper-cli (120s)", flush=True)
			return ""

		if result.returncode != 0:
			print(f"❌ whisper-cli erreur (code {result.returncode}): {result.stderr[:200]}", flush=True)

		# Use only stdout for text — stderr contains logs
		return self._clean_output(result.stdout or "")

	@staticmethod
	def _clean_output(output: str) -> str:
		"""Clean Whisper output"""
		lines = []
		for line in output.splitlines():
			s = line.strip()
			if not s:
				continue

			# Remove timestamp [..]
			if s.startswith("[") and "]" in s:
				s = s.split("]", 1)[-1].strip()

			# Keep only lines with text
			if s and any(ch.isalpha() for ch in s):
				lines.append(s)

		return "\n".join(lines).strip()
