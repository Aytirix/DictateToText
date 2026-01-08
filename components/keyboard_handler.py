"""Keyboard event handler"""

from evdev import InputDevice, ecodes

from app_config import AppConfig


class KeyboardHandler:
	"""Handle keyboard events and combos"""

	def __init__(self, cfg: AppConfig):
		self.config = cfg
		self._pressed = set()
		self._device = None

	def initialize(self) -> None:
		"""Initialize keyboard device"""
		self._device = InputDevice(self.config.input_event)
		print(f"Clavier: {self._device.name} ({self.config.input_event})")

	def read_events(self):
		"""Generator yielding keyboard events"""
		for ev in self._device.read_loop():
			if ev.type != ecodes.EV_KEY:
				continue

			if ev.value == 1:  # Key down
				self._pressed.add(ev.code)
			elif ev.value == 0:  # Key up
				self._pressed.discard(ev.code)

			yield ev

	def is_copilot_combo_pressed(self) -> bool:
		"""Check if copilot combo is pressed"""
		return self.config.copilot_combo.issubset(self._pressed)

	def is_history_combo_pressed(self) -> bool:
		"""Check if history combo is pressed"""
		return self.config.history_combo.issubset(self._pressed)
