"""Main application orchestrator"""

import glob
import os
import re
import signal
import time
from threading import Thread

import customtkinter as ctk

import config as cfg_module
from app_config import AppConfig
from services import NotificationService, ClipboardService, TranscriptionService
from components import AudioRecorder, HistoryManager, KeyboardHandler, TranscriptionWorker
from ui import HistoryWindow


class DictatePTTApplication:
	"""Main application orchestrator"""

	_GUI_ENV_KEYS = ("DISPLAY", "WAYLAND_DISPLAY", "XDG_RUNTIME_DIR", "XAUTHORITY")

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
		self._history_open_requested = False

		# Keyboard state
		self._was_copilot_down = False
		self._was_history_down = False
		self._recording_started_at = None
		self._tap_toggle_recording = False

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

		gui_ready = self._ensure_gui_root()
		if not gui_ready:
			print("⚠️  Interface graphique indisponible au démarrage (contexte graphique introuvable ou inaccessible).", flush=True)
			print("ℹ️  La dictée continue en mode headless; l'historique ouvrira la GUI quand possible.", flush=True)

		# Start keyboard listener in daemon thread
		kbd_thread = Thread(target=self._event_loop, daemon=True)
		kbd_thread.start()

		if gui_ready:
			# Main thread runs Tkinter mainloop
			try:
				self._root.mainloop()
			except KeyboardInterrupt:
				self._shutdown()
			return

		# Headless fallback loop: keep service alive and try GUI on-demand
		try:
			while True:
				if self._history_open_requested:
					self._history_open_requested = False
					if self._ensure_gui_root():
						self._show_history()
						self._root.mainloop()
				time.sleep(0.2)
		except KeyboardInterrupt:
			self._shutdown()

	def _event_loop(self) -> None:
		"""Keyboard event loop (runs in daemon thread)"""
		try:
			for _ in self.keyboard_handler.read_events():
				# Check history combo
				history_down = self.keyboard_handler.is_history_combo_pressed()
				if history_down and not self._was_history_down:
					if self._root:
						# Schedule window creation on main (Tkinter) thread
						self._root.after(0, self._show_history)
					else:
						# Ask main thread to try creating GUI later (when display env is ready)
						self._history_open_requested = True
				self._was_history_down = history_down

				# Check copilot combo (recording)
				copilot_down = self.keyboard_handler.is_copilot_combo_pressed()

				recording_mode = cfg_module.get_config_instance().get("recording_mode", "push_to_talk")

				if recording_mode == "toggle":
					# Toggle mode: press once to start, press again to stop
					if copilot_down and not self._was_copilot_down:
						if self.recorder.is_recording:
							self._stop_recording_reminder()
							wav_file = self.recorder.stop_recording()
							self._recording_started_at = None
							if wav_file:
								self.worker.submit(wav_file)
						elif self.worker.is_transcribing():
							print("⚠️  Conversion en cours, patientez...", flush=True)
							NotificationService.transcribing()
						else:
							if self.recorder.start_recording():
								self._recording_started_at = time.monotonic()
								self._start_recording_reminder()
				else:
					# Push-to-talk mode: hold to record, or tap again for keys that release instantly.
					if copilot_down and not self._was_copilot_down:
						if self._tap_toggle_recording and self.recorder.is_recording:
							self._tap_toggle_recording = False
							self._stop_recording_reminder()
							wav_file = self.recorder.stop_recording()
							self._recording_started_at = None
							if wav_file:
								self.worker.submit(wav_file)
						elif self.worker.is_transcribing():
							print("⚠️  Conversion en cours, patientez...", flush=True)
							NotificationService.transcribing()
						else:
							if self.recorder.start_recording():
								self._recording_started_at = time.monotonic()

					if (not copilot_down and self._was_copilot_down and self.recorder.is_recording
					        and not self._tap_toggle_recording):
						elapsed = time.monotonic() - self._recording_started_at if self._recording_started_at else 0
						if elapsed < 0.35:
							self._tap_toggle_recording = True
							self._start_recording_reminder()
							print("🎙️  Touche instantanée détectée, écoute maintenue jusqu'au prochain appui.", flush=True)
							continue
						wav_file = self.recorder.stop_recording()
						self._recording_started_at = None
						if wav_file:
							self.worker.submit(wav_file)

				self._was_copilot_down = copilot_down
		except Exception as e:
			print(f"❌ Erreur boucle clavier: {e}", flush=True)

	def _start_recording_reminder(self) -> None:
		"""Show persistent recording notification."""
		NotificationService.listening()

	def _stop_recording_reminder(self) -> None:
		"""Stop the toggle recording reminder."""
		NotificationService.close_current()

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
			self._history_window.on_settings_applied = self.keyboard_handler.reload_config
			self._history_window_open = True

			original_close = self._history_window.on_close

			def on_close_wrapper():
				self._history_window_open = False
				self._history_window = None
				original_close()

			self._history_window.on_close = on_close_wrapper

	def _ensure_gui_root(self) -> bool:
		"""Create hidden CTk root when a graphical display is available."""
		if self._root:
			return True

		cfg_obj = cfg_module.get_config_instance()
		ctk.set_appearance_mode(cfg_obj.get("theme_mode", "dark"))
		ctk.set_default_color_theme(cfg_obj.get("accent_color", "blue"))

		original_env = {key: os.environ.get(key) for key in self._GUI_ENV_KEYS}
		last_error = None

		for candidate in self._iter_gui_env_candidates():
			previous_env = {key: os.environ.get(key) for key in self._GUI_ENV_KEYS}
			self._apply_gui_env(candidate)

			try:
				self._root = ctk.CTk()
				self._root.withdraw()  # Hide root window
				self._log_gui_environment(candidate, original_env)
				return True
			except Exception as e:
				last_error = e
				self._root = None
				self._apply_gui_env(previous_env)

		if last_error is not None:
			print(f"⚠️  GUI non disponible: {last_error}", flush=True)
		return False

	def _iter_gui_env_candidates(self) -> list[dict[str, str | None]]:
		"""Build likely graphical environments for Tk/XWayland."""
		current_env = {key: os.environ.get(key) for key in self._GUI_ENV_KEYS}
		runtime_dir = self._discover_runtime_dir(current_env.get("XDG_RUNTIME_DIR"))
		wayland_display = self._discover_wayland_display(runtime_dir, current_env.get("WAYLAND_DISPLAY"))
		display_candidates = self._discover_display_candidates(current_env.get("DISPLAY"))
		xauthority_candidates = self._discover_xauthority_candidates(runtime_dir, current_env.get("XAUTHORITY"))

		candidates: list[dict[str, str | None]] = []
		seen: set[tuple[tuple[str, str | None], ...]] = set()

		def add_candidate(display: str | None,
		                  wayland: str | None,
		                  runtime: str | None,
		                  xauthority: str | None) -> None:
			candidate = {
			    "DISPLAY": display,
			    "WAYLAND_DISPLAY": wayland,
			    "XDG_RUNTIME_DIR": runtime,
			    "XAUTHORITY": xauthority,
			}
			signature = tuple((key, candidate[key]) for key in self._GUI_ENV_KEYS)
			if signature not in seen:
				seen.add(signature)
				candidates.append(candidate)

		add_candidate(current_env.get("DISPLAY"),
		              current_env.get("WAYLAND_DISPLAY"),
		              current_env.get("XDG_RUNTIME_DIR"),
		              current_env.get("XAUTHORITY"))

		for display in display_candidates:
			add_candidate(display, wayland_display, runtime_dir, current_env.get("XAUTHORITY"))
			for xauthority in xauthority_candidates:
				add_candidate(display, wayland_display, runtime_dir, xauthority)

		if not display_candidates:
			for xauthority in xauthority_candidates:
				add_candidate(None, wayland_display, runtime_dir, xauthority)

		add_candidate(None, wayland_display, runtime_dir, current_env.get("XAUTHORITY"))
		add_candidate(None, wayland_display, runtime_dir, None)

		return candidates

	def _discover_runtime_dir(self, current_runtime_dir: str | None) -> str | None:
		"""Return a valid XDG runtime directory when available."""
		if current_runtime_dir and os.path.isdir(current_runtime_dir):
			return current_runtime_dir

		fallback = f"/run/user/{os.getuid()}"
		if os.path.isdir(fallback):
			return fallback

		return None

	def _discover_wayland_display(self,
	                              runtime_dir: str | None,
	                              current_wayland_display: str | None) -> str | None:
		"""Return an existing Wayland socket name when possible."""
		if runtime_dir and current_wayland_display:
			current_socket = os.path.join(runtime_dir, current_wayland_display)
			if os.path.exists(current_socket):
				return current_wayland_display

		if not runtime_dir:
			return current_wayland_display

		for path in sorted(glob.glob(os.path.join(runtime_dir, "wayland-*"))):
			name = os.path.basename(path)
			if re.fullmatch(r"wayland-\d+", name):
				return name

		return current_wayland_display

	def _discover_display_candidates(self, current_display: str | None) -> list[str]:
		"""Discover likely X11/XWayland DISPLAY values, prioritizing the current user."""
		candidates: list[tuple[int, int, str]] = []
		current_uid = os.getuid()

		if current_display:
			display_number = self._display_number(current_display)
			priority = -1 if display_number is not None else 0
			candidates.append((priority, display_number or 0, current_display))

		for path in glob.glob("/tmp/.X11-unix/X*"):
			name = os.path.basename(path)
			if not re.fullmatch(r"X\d+", name):
				continue

			display_number = int(name[1:])
			display = f":{display_number}"

			try:
				socket_uid = os.stat(path).st_uid
			except OSError:
				socket_uid = -1

			priority = 0 if socket_uid == current_uid else 1
			candidates.append((priority, display_number, display))

		seen: set[str] = set()
		ordered: list[str] = []
		for _, _, display in sorted(candidates):
			if display not in seen:
				seen.add(display)
				ordered.append(display)
		return ordered

	def _discover_xauthority_candidates(self,
	                                    runtime_dir: str | None,
	                                    current_xauthority: str | None) -> list[str]:
		"""Return existing Xauthority files that might grant access to XWayland."""
		paths: list[str] = []

		if current_xauthority:
			paths.append(current_xauthority)

		paths.append(os.path.expanduser("~/.Xauthority"))

		if runtime_dir:
			paths.extend(glob.glob(os.path.join(runtime_dir, ".mutter-Xwaylandauth.*")))
			paths.extend(glob.glob(os.path.join(runtime_dir, "*Xauthority*")))
			paths.extend(glob.glob(os.path.join(runtime_dir, "*xauth*")))

		seen: set[str] = set()
		existing: list[str] = []
		for path in paths:
			if path and os.path.isfile(path) and path not in seen:
				seen.add(path)
				existing.append(path)
		return existing

	def _apply_gui_env(self, candidate: dict[str, str | None]) -> None:
		"""Apply one GUI environment candidate to the current process."""
		for key in self._GUI_ENV_KEYS:
			value = candidate.get(key)
			if value:
				os.environ[key] = value
			else:
				os.environ.pop(key, None)

	def _log_gui_environment(self,
	                         selected_env: dict[str, str | None],
	                         original_env: dict[str, str | None]) -> None:
		"""Log when a missing or incomplete GUI environment was repaired automatically."""
		if selected_env == original_env:
			return

		details = [f"{key}={value}" for key, value in selected_env.items() if value]
		if details:
			print(f"🖥️  Environnement graphique détecté automatiquement ({', '.join(details)})", flush=True)

	@staticmethod
	def _display_number(display: str) -> int | None:
		"""Parse a DISPLAY value like :1 or :1.0 into its numeric display id."""
		match = re.fullmatch(r":(\d+)(?:\.\d+)?", display)
		if not match:
			return None
		return int(match.group(1))

	def _shutdown(self, *args) -> None:
		"""Shutdown application"""
		print("\n🛑 Arrêt de l'application...")
		self._stop_recording_reminder()

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
