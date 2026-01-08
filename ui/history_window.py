"""History window UI"""

import tkinter as tk

import config
from components import HistoryManager, TranscriptionWorker


class HistoryWindow:
	"""History window with real-time updates"""

	def __init__(self, history_manager: HistoryManager, worker: TranscriptionWorker):
		self.history_manager = history_manager
		self.worker = worker

		self.window = tk.Tk()
		self._setup_ui()

		# Attach as observer
		self.history_manager.attach_observer(self)

		# Schedule status updates
		self.schedule_update()

	def _setup_ui(self) -> None:
		"""Setup the user interface"""
		self.update_title()
		self.window.geometry("700x500")
		self.window.configure(bg="#2b2b2b")
		self.window.protocol("WM_DELETE_WINDOW", self.on_close)

		# Top frame with status and config button
		top_frame = tk.Frame(self.window, bg="#2b2b2b")
		top_frame.pack(pady=10, padx=10, fill="x")

		status_frame = tk.Frame(top_frame, bg="#2b2b2b")
		status_frame.pack(side="left", fill="x", expand=True)

		self.status_label = tk.Label(status_frame, text="", font=("Monospace", 11, "bold"), bg="#2b2b2b")
		self.status_label.pack()

		config_btn = tk.Button(top_frame,
		                       text="⚙️",
		                       command=self.open_config,
		                       bg="#3c3c3c",
		                       fg="white",
		                       font=("Sans", 12, "bold"),
		                       padx=10,
		                       pady=5,
		                       cursor="hand2",
		                       relief="flat")
		config_btn.pack(side="right")

		# History frame
		history_frame = tk.Frame(self.window, bg="#2b2b2b")
		history_frame.pack(pady=10, padx=10, fill="both", expand=True)

		scrollbar = tk.Scrollbar(history_frame)
		scrollbar.pack(side="right", fill="y")

		self.text_widget = tk.Text(history_frame,
		                           font=("Monospace", 10),
		                           bg="#1e1e1e",
		                           fg="#d4d4d4",
		                           wrap="word",
		                           yscrollcommand=scrollbar.set,
		                           padx=10,
		                           pady=10)
		self.text_widget.pack(side="left", fill="both", expand=True)
		scrollbar.config(command=self.text_widget.yview)

		# Text tags
		self.text_widget.tag_config("number", foreground="#569cd6", font=("Monospace", 10, "bold"))
		self.text_widget.tag_config("content", foreground="#d4d4d4")
		self.text_widget.tag_config("empty", foreground="#808080", font=("Monospace", 10, "italic"))

		# Close button
		close_btn = tk.Button(self.window,
		                      text="Fermer",
		                      command=self.on_close,
		                      bg="#0e639c",
		                      fg="white",
		                      font=("Sans", 10, "bold"),
		                      padx=20,
		                      pady=5,
		                      cursor="hand2")
		close_btn.pack(pady=10)

		# Initial content
		self.update_content()
		self.update_status()

	def schedule_update(self) -> None:
		"""Schedule periodic status updates"""
		if self.window.winfo_exists():
			self.update_status()
			self.window.after(200, self.schedule_update)

	def update_status(self) -> None:
		"""Update transcription status indicator"""
		if self.worker.is_transcribing():
			self.status_label.config(text="⏳ Conversion en cours...", fg="#ffa500")
		else:
			self.status_label.config(text="✓ Aucune conversion en cours", fg="#00ff00")

	def update_content(self) -> None:
		"""Update history content"""
		self.text_widget.config(state="normal")
		self.text_widget.delete("1.0", "end")

		if not self.history_manager.items:
			self.text_widget.insert("1.0", "(Historique vide)\n\n", "empty")
		else:
			for i, text in enumerate(reversed(self.history_manager.items), 1):
				self.text_widget.insert("end", f"{i:2}. ", "number")
				self.text_widget.insert("end", f"{text}\n\n", "content")

		self.text_widget.config(state="disabled")
		self.text_widget.see("end")
		self.update_status()

	def focus(self) -> None:
		"""Bring window to front"""
		self.window.lift()
		self.window.focus_force()

	def update_title(self) -> None:
		"""Update window title with history size"""
		size = config.get_history_size()
		self.window.title(f"📜 Historique Dictate PTT Copilot ({size} max)")

	def open_config(self) -> None:
		"""Open settings window"""
		from .settings_window import SettingsWindow
		SettingsWindow(self.window, self)

	def on_close(self) -> None:
		"""Handle window close"""
		self.window.destroy()

	def run(self) -> None:
		"""Start main loop"""
		self.window.mainloop()
