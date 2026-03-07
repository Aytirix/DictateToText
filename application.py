"""Main application orchestrator"""

import signal
from threading import Thread

import customtkinter as ctk

import config as cfg_module
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
		self.transcription_service = TranscriptionService()
		self.history_manager = HistoryManager()

		# Initialize components
		self.recorder = AudioRecorder(cfg)
		self.worker = TranscriptionWorker(self.transcription_service, self.history_manager, self.clipboard_service)
		self.keyboard_handler = KeyboardHandler(cfg)

		# Tkinter root (hidden) — must be unique, created in main thread
		self._root = None
		self._history_window = None
		self._history_window_open = False

		# Keyboard state
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

		# Create hidden Tkinter root in main thread
		import config as cfg_module
		cfg_obj = cfg_module.get_config_instance()
		ctk.set_appearance_mode(cfg_obj.get("theme_mode", "dark"))
		ctk.set_default_color_theme(cfg_obj.get("accent_color", "blue"))
		self._root = ctk.CTk()
		self._root.withdraw()  # Hide root window

		# Start keyboard listener in daemon thread
		kbd_thread = Thread(target=self._event_loop, daemon=True)
		kbd_thread.start()

		# Main thread runs Tkinter mainloop
		try:
			self._root.mainloop()
		except KeyboardInterrupt:
			self._shutdown()

	def _event_loop(self) -> None:
		"""Keyboard event loop (runs in daemon thread)"""
		try:
			for _ in self.keyboard_handler.read_events():
				# Check history combo
				history_down = self.keyboard_handler.is_history_combo_pressed()
				if history_down and not self._was_history_down:
					# Schedule window creation on main (Tkinter) thread
					self._root.after(0, self._show_history)
				self._was_history_down = history_down

				# Check copilot combo (recording)
				copilot_down = self.keyboard_handler.is_copilot_combo_pressed()

				recording_mode = cfg_module.get_config_instance().get("recording_mode", "push_to_talk")

				if recording_mode == "toggle":
					# Toggle mode: press once to start, press again to stop
					if copilot_down and not self._was_copilot_down:
						if self.recorder.is_recording:
							wav_file = self.recorder.stop_recording()
							if wav_file:
								self.worker.submit(wav_file)
						elif self.worker.is_transcribing():
							print("⚠️  Conversion en cours, patientez...", flush=True)
							self.notification_service.send("Dictate PTT Copilot", "Conversion en cours, patientez...")
						else:
							self.recorder.start_recording()
				else:
					# Push-to-talk mode (default): hold to record, release to stop
					if copilot_down and not self._was_copilot_down:
						if self.worker.is_transcribing():
							print("⚠️  Conversion en cours, patientez...", flush=True)
							self.notification_service.send("Dictate PTT Copilot", "Conversion en cours, patientez...")
						else:
							self.recorder.start_recording()

					if not copilot_down and self._was_copilot_down and self.recorder.is_recording:
						wav_file = self.recorder.stop_recording()
						if wav_file:
							self.worker.submit(wav_file)

				self._was_copilot_down = copilot_down
		except Exception as e:
			print(f"❌ Erreur boucle clavier: {e}", flush=True)

	def _show_history(self) -> None:
		"""Show or focus history window (called on main thread)"""
		if self._history_window_open and self._history_window:
			try:
				self._history_window.focus()
				return
			except Exception:
				self._history_window_open = False
				self._history_window = None

		if not self._history_window_open:
			self._history_window = HistoryWindow(self._root, self.history_manager, self.worker)
			self._history_window_open = True

			original_close = self._history_window.on_close

			def on_close_wrapper():
				self._history_window_open = False
				self._history_window = None
				original_close()

			self._history_window.on_close = on_close_wrapper

	def _shutdown(self, *args) -> None:
		"""Shutdown application"""
		print("\n🛑 Arrêt de l'application...")

		# Close history window if open
		if self._history_window_open and self._history_window:
			try:
				self._history_window.window.destroy()
			except Exception:
				pass

		# Stop Tkinter mainloop
		if self._root:
			try:
				self._root.quit()
				self._root.destroy()
			except Exception:
				pass

		try:
			self.recorder.stop_stream()
		except Exception:
			pass

		raise SystemExit(0)
