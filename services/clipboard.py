"""Clipboard service"""

import os
import subprocess

from .notification import NotificationService


class ClipboardService:
	"""Handle clipboard operations"""

	_last_process = None

	@classmethod
	def copy(cls, text: str) -> bool:
		"""Copy text to clipboard using wl-copy"""
		text = text.strip()
		if not text:
			return False

		try:
			env = os.environ.copy()
			# Ensure Wayland env vars are set for systemd context
			if "WAYLAND_DISPLAY" not in env:
				env["WAYLAND_DISPLAY"] = "wayland-1"
			if "XDG_RUNTIME_DIR" not in env:
				env["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"

			# Kill previous wl-copy process to avoid zombie accumulation
			if cls._last_process is not None:
				try:
					cls._last_process.kill()
					cls._last_process.wait(timeout=1)
				except Exception:
					pass

			# wl-copy must stay alive in the background to serve the Wayland
			# clipboard — do NOT wait for it to finish.
			cls._last_process = subprocess.Popen(["wl-copy", text],
			                                     env=env,
			                                     stdout=subprocess.DEVNULL,
			                                     stderr=subprocess.DEVNULL)

			print("📋 Texte copié dans le presse-papiers!", flush=True)
			NotificationService.send("Dictate PTT Copilot", "✅ Texte copié dans le presse-papiers")
			return True

		except Exception as e:
			print(f"wl-copy erreur: {e}", flush=True)
			NotificationService.send("Dictate PTT Copilot", f"Erreur copie:\n{e}")
			return False
