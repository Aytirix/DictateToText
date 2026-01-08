"""Notification service"""

import subprocess


class NotificationService:
	"""Handle system notifications"""

	@staticmethod
	def send(title: str, body: str = "") -> None:
		"""Send a system notification without blocking"""
		subprocess.Popen(["notify-send", title, body], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
