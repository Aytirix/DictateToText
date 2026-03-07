"""History management component"""

import config


class HistoryManager:
	"""Manage transcription history"""

	def __init__(self):
		self.items = list(config.get_history())  # copy, don't hold reference
		self._max_size = config.get_history_size()
		self._observers = []

	def add(self, text: str) -> None:
		"""Add item to history"""
		text = text.strip()
		if not text:
			return

		self.items.append(text)
		if len(self.items) > self._max_size:
			self.items[:] = self.items[-self._max_size:]

		config.save_history(self.items)
		self._notify_observers()

	def set_max_size(self, size: int) -> bool:
		"""Update maximum history size"""
		if config.set_history_size(size):
			self._max_size = size
			if len(self.items) > size:
				self.items[:] = self.items[-size:]
				config.save_history(self.items)
			self._notify_observers()
			return True
		return False

	def attach_observer(self, observer) -> None:
		"""Attach an observer to be notified of changes"""
		self._observers.append(observer)

	def detach_observer(self, observer) -> None:
		"""Detach an observer"""
		self._observers = [o for o in self._observers if o is not observer]

	def _notify_observers(self) -> None:
		"""Notify all observers of changes"""
		dead = []
		for observer in self._observers:
			if hasattr(observer, 'update_content') and hasattr(observer, 'window'):
				try:
					if observer.window.winfo_exists():
						observer.window.after(0, observer.update_content)
					else:
						dead.append(observer)
				except Exception:
					dead.append(observer)
		for obs in dead:
			self._observers.remove(obs)
