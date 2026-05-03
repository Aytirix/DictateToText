"""Notification service"""

import subprocess
from threading import Lock

import config as cfg_module


class NotificationService:
	"""Handle system notifications"""

	_current_id = None
	_lock = Lock()
	APP_NAME = "Dictate PTT Copilot"

	@staticmethod
	def send(title: str, body: str = "") -> None:
		"""Send a system notification without blocking"""
		NotificationService._send(title, body, timeout_ms=None, replace=False)

	@classmethod
	def listening(cls) -> None:
		"""Show persistent listening notification."""
		cls._send(cls.APP_NAME, "🎙️ Écoute en cours", timeout_ms=0, replace=True)

	@classmethod
	def transcribing(cls) -> None:
		"""Show persistent transcribing notification."""
		cls._send(cls.APP_NAME, "🔄 Transcription en texte...", timeout_ms=0, replace=True)

	@classmethod
	def copied(cls) -> None:
		"""Show short success notification."""
		cls._send(cls.APP_NAME, "✅ Copié dans le presse-papiers", timeout_ms=3000, replace=True)

	@classmethod
	def failed(cls, body: str) -> None:
		"""Show short error notification."""
		cls._send(cls.APP_NAME, body, timeout_ms=5000, replace=True)

	@classmethod
	def close_current(cls) -> None:
		"""Close the currently tracked notification when the server supports it."""
		cfg = cfg_module.get_config_instance()
		if not cfg.get("notifications_enabled", True):
			return

		with cls._lock:
			notification_id = cls._current_id
			cls._current_id = None

		if not notification_id:
			return

		cmd = [
		    "gdbus",
		    "call",
		    "--session",
		    "--dest",
		    "org.freedesktop.Notifications",
		    "--object-path",
		    "/org/freedesktop/Notifications",
		    "--method",
		    "org.freedesktop.Notifications.CloseNotification",
		    f"uint32 {notification_id}",
		]
		try:
			subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		except Exception:
			pass

	@classmethod
	def _send(cls, title: str, body: str = "", timeout_ms: int | None = None, replace: bool = False) -> None:
		"""Send a notification, optionally replacing the previous app notification."""
		cfg = cfg_module.get_config_instance()
		if not cfg.get("notifications_enabled", True):
			return

		if replace:
			with cls._lock:
				new_id = cls._send_replace(title, body, timeout_ms, cls._current_id)
				if new_id is None and cls._current_id:
					cls._current_id = None
					new_id = cls._send_replace(title, body, timeout_ms, None)
				if new_id is not None:
					cls._current_id = new_id
			return

		cmd = cls._build_command(title, body, timeout_ms, replace=False)
		try:
			subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		except Exception:
			pass

	@classmethod
	def _send_replace(cls, title: str, body: str, timeout_ms: int | None, replace_id: str | None) -> str | None:
		"""Send a replacing notification and return its fresh ID."""
		cmd = cls._build_command(title, body, timeout_ms, replace=True, replace_id=replace_id)
		try:
			result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
		except Exception:
			return None

		new_id = result.stdout.strip()
		if result.returncode == 0 and new_id.isdigit():
			return new_id
		return None

	@classmethod
	def _build_command(cls,
	                   title: str,
	                   body: str = "",
	                   timeout_ms: int | None = None,
	                   replace: bool = False,
	                   replace_id: str | None = None) -> list[str]:
		"""Build the notify-send command."""
		cmd = [
		    "notify-send",
		    "-a",
		    cls.APP_NAME,
		    "-h",
		    "string:x-canonical-private-synchronous:dictate-ptt-copilot",
		]
		if timeout_ms is not None:
			cmd += ["-t", str(timeout_ms)]
		if replace and replace_id:
			cmd += ["-r", str(replace_id)]
		if replace:
			cmd += ["-p"]
		cmd += [title, body]
		return cmd
