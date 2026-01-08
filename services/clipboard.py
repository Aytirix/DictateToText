"""Clipboard service"""

import subprocess

from .notification import NotificationService


class ClipboardService:
	"""Handle clipboard operations"""

	@staticmethod
	def copy(text: str) -> bool:
		"""Copy text to clipboard using wl-copy"""
		text = text.strip()
		if not text:
			return False

		try:
			proc = subprocess.Popen(["wl-copy"],
			                        stdin=subprocess.PIPE,
			                        stdout=subprocess.DEVNULL,
			                        stderr=subprocess.DEVNULL,
			                        text=True)
			proc.stdin.write(text)
			proc.stdin.close()

			print("📋 Texte copié dans le presse-papiers!", flush=True)
			NotificationService.send("Dictate PTT Copilot", "✅ Texte copié dans le presse-papiers")
			return True

		except Exception as e:
			print(f"wl-copy erreur: {e}", flush=True)
			NotificationService.send("Dictate PTT Copilot", f"Erreur copie:\n{e}")
			return False
