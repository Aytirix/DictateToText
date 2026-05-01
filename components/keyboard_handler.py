"""Keyboard event handler"""

import select

from evdev import InputDevice, ecodes, list_devices

from app_config import AppConfig


class KeyboardHandler:
	"""Handle keyboard events and combos"""

	def __init__(self, cfg: AppConfig):
		self.config = cfg
		self._pressed = set()
		self._devices = []

	def initialize(self) -> None:
		"""Initialize keyboard devices."""
		self._devices = self._discover_keyboard_devices()
		if not self._devices:
			self._devices = [InputDevice(self.config.input_event)]

		for device in self._devices:
			print(f"Clavier: {device.name} ({device.path})")

	def reload_config(self) -> None:
		"""Reload key combos from configuration."""
		self.config.reload()
		self._pressed.clear()

	def read_events(self):
		"""Generator yielding keyboard events from all keyboard-like devices."""
		while True:
			readable, _, _ = select.select(self._devices, [], [])
			for device in readable:
				try:
					events = device.read()
				except OSError:
					self._devices = [dev for dev in self._devices if dev.fd != device.fd]
					if not self._devices:
						self.initialize()
					continue

				for ev in events:
					if ev.type != ecodes.EV_KEY:
						continue

					if ev.value == 1:  # Key down
						self._pressed.add(ev.code)
					elif ev.value == 0:  # Key up
						self._pressed.discard(ev.code)

					yield ev

	def _discover_keyboard_devices(self) -> list[InputDevice]:
		"""Open devices that can emit keyboard events."""
		devices = []
		seen_paths = set()

		for path in [self.config.input_event, *list_devices()]:
			if path in seen_paths:
				continue
			seen_paths.add(path)

			try:
				device = InputDevice(path)
				keys = device.capabilities().get(ecodes.EV_KEY, [])
			except OSError:
				continue

			if self._is_keyboard_like(device, keys):
				devices.append(device)

		return devices

	@staticmethod
	def _is_keyboard_like(device: InputDevice, keys) -> bool:
		"""Return True for devices worth listening to for hotkeys."""
		if not isinstance(keys, list) or not keys:
			return False

		key_set = set(keys)
		name = device.name.lower()
		return (
		    "keyboard" in name
		    or "hotkey" in name
		    or "consumer control" in name
		    or ecodes.KEY_A in key_set
		    or ecodes.KEY_SPACE in key_set
		    or ecodes.KEY_LEFTMETA in key_set
		    or ecodes.KEY_F23 in key_set
		)

	def is_copilot_combo_pressed(self) -> bool:
		"""Check if copilot combo is pressed"""
		return self.config.copilot_combo.issubset(self._pressed)

	def is_history_combo_pressed(self) -> bool:
		"""Check if history combo is pressed"""
		return self.config.history_combo.issubset(self._pressed)
