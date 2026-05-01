"""Transcription worker thread"""

import os
from queue import Queue
from threading import Lock, Thread

from services import NotificationService, ClipboardService, TranscriptionService
from components.history_manager import HistoryManager


class TranscriptionWorker:
	"""Worker thread that processes transcriptions sequentially"""

	def __init__(self, transcription_service: TranscriptionService, history_manager: HistoryManager,
	             clipboard_service: ClipboardService):
		self.transcription_service = transcription_service
		self.history_manager = history_manager
		self.clipboard_service = clipboard_service

		self._queue = Queue()
		self._transcribing = False
		self._transcribing_lock = Lock()
		self._thread = None

	def start(self) -> None:
		"""Start the worker thread"""
		self._thread = Thread(target=self._run, daemon=True)
		self._thread.start()
		print("🔧 Worker de transcription démarré")

	def submit(self, wav_file: str) -> None:
		"""Submit a file for transcription"""
		self._queue.put(wav_file)

	def is_transcribing(self) -> bool:
		"""Check if currently transcribing"""
		with self._transcribing_lock:
			return self._transcribing

	def _run(self) -> None:
		"""Worker main loop"""
		while True:
			wav_file = self._queue.get()

			try:
				# Set transcribing flag
				with self._transcribing_lock:
					self._transcribing = True

				print(f"🔄 Transcription en cours: {wav_file}", flush=True)
				NotificationService.transcribing()
				text = self.transcription_service.transcribe(wav_file)

				# Release flag immediately after transcription
				with self._transcribing_lock:
					self._transcribing = False

				if text is None:
					print("❌ Transcription échouée.", flush=True)
					NotificationService.failed("Transcription échouée")
				elif text:
					print("✅ Transcription terminée.", flush=True)
					self.history_manager.add(text)
					print(text, flush=True)

					try:
						self.clipboard_service.copy(text)
					except Exception as e:
						print(f"⚠️  Erreur copie: {e}", flush=True)
						NotificationService.failed(f"Transcription OK mais erreur copie: {e}")
				else:
					print("✅ Transcription terminée.", flush=True)
					print("⚠️  Transcription vide.", flush=True)

			except Exception as e:
				print(f"❌ Erreur transcription: {e}", flush=True)
				NotificationService.failed(f"Erreur: {e}")
				with self._transcribing_lock:
					self._transcribing = False

			finally:
				# Cleanup (only if not saving audio files)
				import config
				cfg = config.get_config_instance()
				if not cfg.get("save_audio_files", False):
					try:
						os.remove(wav_file)
					except OSError:
						pass
				self._queue.task_done()
