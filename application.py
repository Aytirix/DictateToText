"""Main application orchestrator"""

import signal
from threading import Thread

from app_config import AppConfig
from services import NotificationService, ClipboardService, TranscriptionService
from components import AudioRecorder, HistoryManager, KeyboardHandler, TranscriptionWorker
from ui import HistoryWindow


class DictatePTTApplication:
	"""Main application orchestrator"""

	def __init__(self, cfg: AppConfig):
		self.config = cfg

		# Initialize services
		self.notification_service = NotificationService()
		self.clipboard_service = ClipboardService()
		self.transcription_service = TranscriptionService(cfg)
		self.history_manager = HistoryManager()

		# Initialize components
		self.recorder = AudioRecorder(cfg)
		self.worker = TranscriptionWorker(self.transcription_service, self.history_manager, self.clipboard_service)
		self.keyboard_handler = KeyboardHandler(cfg)

		# State
		self._history_window = None
		self._history_window_open = False
		self._was_copilot_down = False
		self._was_history_down = False

	def run(self) -> None:
		"""Run the application"""
		print(f"📜 Historique chargé: {len(self.history_manager.items)} éléments")

		# Validate configuration
		self.config.validate()

		# Start components
		self.worker.start()
		self.keyboard_handler.initialize()
		self.recorder.start_stream()

		# Setup signal handlers
		signal.signal(signal.SIGTERM, self._shutdown)

		print("Push-to-talk: MAINTIENS Copilot → relâche → transcrit + copie.")
		print("Historique: Ctrl+Shift+H")
		print()

		# Main event loop
		try:
			self._event_loop()
		except KeyboardInterrupt:
			self._shutdown()

	def _event_loop(self) -> None:
		"""Main keyboard event loop"""
		for _ in self.keyboard_handler.read_events():
			# Check history combo
			history_down = self.keyboard_handler.is_history_combo_pressed()
			if history_down and not self._was_history_down:
				self._show_history()
			self._was_history_down = history_down

			# Check copilot combo (recording)
			copilot_down = self.keyboard_handler.is_copilot_combo_pressed()

			# Start recording
			if copilot_down and not self._was_copilot_down:
				if self.worker.is_transcribing():
					print("⚠️  Conversion en cours, patientez...", flush=True)
					self.notification_service.send("Dictate PTT Copilot", "Conversion en cours, patientez...")
				else:
					self.recorder.start_recording()

			# Stop recording
			if not copilot_down and self._was_copilot_down and self.recorder.is_recording:
				wav_file = self.recorder.stop_recording()
				if wav_file:
					self.worker.submit(wav_file)

			self._was_copilot_down = copilot_down

	def _show_history(self) -> None:
		"""Show or focus history window"""
		if self._history_window_open and self._history_window:
			try:
				self._history_window.focus()
			except:
				# Window was closed externally
				self._history_window_open = False
				self._history_window = None

		if not self._history_window_open:

			def create_window():
				self._history_window = HistoryWindow(self.history_manager, self.worker)
				self._history_window_open = True

				# Callback when window closes
				original_close = self._history_window.on_close

				def on_close_wrapper():
					self._history_window_open = False
					self._history_window = None
					original_close()

				self._history_window.on_close = on_close_wrapper
				self._history_window.run()

			Thread(target=create_window, daemon=True).start()

	def _shutdown(self, *args) -> None:
		"""Shutdown application"""
		print("\n🛑 Arrêt de l'application...")

		# Close history window if open
		if self._history_window_open and self._history_window:
			try:
				self._history_window.window.quit()
				self._history_window.window.destroy()
			except:
				pass

		try:
			self.recorder.stop_stream()
		except Exception:
			pass

		raise SystemExit(0)
