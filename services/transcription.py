"""Transcription service using Whisper"""

import os
import subprocess

import config as cfg_module


class TranscriptionService:
	"""Handle Whisper transcription"""

	def transcribe(self, wav_path: str) -> str | None:
		"""Transcribe audio file using Whisper"""
		cfg = cfg_module.get_config_instance()

		whisper_bin = os.path.expanduser(cfg.get("whisper_bin", "whisper-cli"))
		whisper_path = os.path.expanduser(cfg.get("whisper_path", "~/Documents/tools/whisper.cpp"))
		model_name = cfg.get("whisper_model", "large-v3")
		whisper_model = os.path.join(whisper_path, f"models/ggml-{model_name}.bin")
		language = cfg.get("language", "fr")

		cmd = [whisper_bin, "-m", whisper_model, "-f", wav_path, "-nt"]
		if language != "auto":
			cmd += ["-l", language]

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

		no_gpu = cfg.get("whisper_no_gpu", False)
		if no_gpu:
			cmd += ["-ng"]

		timeout = cfg.get("whisper_timeout", 120)
		result = self._run_whisper(cmd, timeout)
		if result is None:
			return None

		if result.returncode != 0:
			stderr = result.stderr or ""
			print(f"❌ whisper-cli erreur (code {result.returncode}):\n{stderr.strip()}", flush=True)

			if not no_gpu and self._is_gpu_oom(stderr):
				print("⚠️  Mémoire GPU insuffisante. Gardez le GPU avec un modèle plus léger/quantifié.", flush=True)

			return None

		# Use only stdout for text — stderr contains logs
		return self._clean_output(result.stdout or "")

	@staticmethod
	def _run_whisper(cmd: list[str], timeout: int) -> subprocess.CompletedProcess | None:
		"""Run whisper-cli and handle timeouts."""
		try:
			return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
		except subprocess.TimeoutExpired:
			print(f"❌ Timeout whisper-cli ({timeout}s)", flush=True)
			return None

	@staticmethod
	def _is_gpu_oom(stderr: str) -> bool:
		"""Return True when whisper.cpp failed because CUDA ran out of memory."""
		s = stderr.lower()
		return "cuda" in s and "out of memory" in s

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
