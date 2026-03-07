"""Notification service"""

import subprocess

import config as cfg_module


class NotificationService:
	"""Handle system notifications"""

	@staticmethod
	def send(title: str, body: str = "") -> None:
		"""Send a system notification without blocking"""
		cfg = cfg_module.get_config_instance()
		if not cfg.get("notifications_enabled", True):
			return
		subprocess.Popen(["notify-send", title, body], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
