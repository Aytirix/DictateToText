"""Notification service"""

import subprocess

import config as cfg_module


class NotificationService:
	"""Handle system notifications"""

	_current_id = None
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
	def _send(cls, title: str, body: str = "", timeout_ms: int | None = None, replace: bool = False) -> None:
		"""Send a notification, optionally replacing the previous app notification."""
		cfg = cfg_module.get_config_instance()
		if not cfg.get("notifications_enabled", True):
			return

		cmd = [
		    "notify-send",
		    "-a",
		    cls.APP_NAME,
		    "-h",
		    "string:x-canonical-private-synchronous:dictate-ptt-copilot",
		]
		if timeout_ms is not None:
			cmd += ["-t", str(timeout_ms)]
		if replace and cls._current_id:
			cmd += ["-r", str(cls._current_id)]
		if replace:
			cmd += ["-p"]
		cmd += [title, body]

		if replace:
			try:
				result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
				new_id = result.stdout.strip()
				if result.returncode == 0 and new_id.isdigit():
					cls._current_id = new_id
			except Exception:
				pass
		else:
			subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
