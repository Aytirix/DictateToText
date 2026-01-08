"""Transcription service using Whisper"""

import subprocess

from app_config import AppConfig


class TranscriptionService:
	"""Handle Whisper transcription"""

	def __init__(self, cfg: AppConfig):
		self.config = cfg

	def transcribe(self, wav_path: str) -> str:
		"""Transcribe audio file using Whisper"""
		cmd = [self.config.whisper_bin, "-m", self.config.whisper_model, "-f", wav_path, "-nt"]
		if self.config.language != "auto":
			cmd += ["-l", self.config.language]

		result = subprocess.run(cmd, capture_output=True, text=True)
		output = (result.stdout or "") + "\n" + (result.stderr or "")

		return self._clean_output(output)

	@staticmethod
	def _clean_output(output: str) -> str:
		"""Clean Whisper output from logs and metadata"""
		bad_prefixes = (
		    "whisper_",
		    "ggml_",
		    "main:",
		    "system_info:",
		    "processing",
		    "Processing",
		    "whisper_print_timings",
		    "load time",
		    "total time",
		    "fallbacks",
		    "Device ",
		    "device ",
		    "compute capability",
		    "found ",
		    "backends",
		    "CUDA",
		    "whisper_init",
		    "whisper_model_load",
		    "whisper_backend",
		    "kv ",
		    "mel time",
		    "sample time",
		    "encode time",
		    "decode time",
		    "batchd time",
		    "prompt time",
		)

		bad_contains = (
		    "compute capability",
		    "VMM:",
		    "CUDA devices",
		    "GGML_CUDA",
		    "OPENVINO",
		    "COREML",
		    "SSE",
		    "AVX",
		    "OPENMP",
		    "BLACKWELL",
		    "PEER_MAX_BATCH_SIZE",
		)

		lines = []
		for line in output.splitlines():
			s = line.strip()
			if not s:
				continue
			if s.startswith(bad_prefixes):
				continue
			if any(x in s for x in bad_contains):
				continue

			# Remove timestamp [..]
			if s.startswith("[") and "]" in s:
				s = s.split("]", 1)[-1].strip()

			# Keep only lines with text
			if any(ch.isalpha() for ch in s):
				lines.append(s)

		return "\n".join(lines).strip()
