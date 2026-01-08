"""Settings window UI"""

import tkinter as tk
from tkinter import messagebox

import config


class SettingsWindow:
	"""Settings window for configuration"""

	def __init__(self, parent, history_window):
		self.parent = parent
		self.history_window = history_window
		self.current_value = config.get_history_size()

		self.window = tk.Toplevel(parent)
		self._setup_ui()

	def _setup_ui(self) -> None:
		"""Setup user interface"""
		self.window.title("⚙️ Paramètres")
		self.window.geometry("600x400")
		self.window.configure(bg="#1e1e1e")
		self.window.resizable(False, False)
		self.window.transient(self.parent)
		self.window.grab_set()

		# Title
		title_frame = tk.Frame(self.window, bg="#1e1e1e")
		title_frame.pack(pady=20, padx=20, fill="x")

		title_label = tk.Label(title_frame, text="⚙️ PARAMÈTRES", font=("Sans", 18, "bold"), bg="#1e1e1e", fg="#ffffff")
		title_label.pack()

		# History section
		section_frame = tk.Frame(self.window, bg="#2b2b2b", relief="ridge", borderwidth=2)
		section_frame.pack(pady=10, padx=40, fill="both", expand=True)

		section_title = tk.Label(section_frame,
		                         text="📜 HISTORIQUE",
		                         font=("Sans", 14, "bold"),
		                         bg="#2b2b2b",
		                         fg="#569cd6")
		section_title.pack(pady=15)

		# Setting: History size
		setting_frame = tk.Frame(section_frame, bg="#2b2b2b")
		setting_frame.pack(pady=10, padx=20, fill="x")

		label = tk.Label(setting_frame,
		                 text="Nombre maximum d'éléments :",
		                 font=("Sans", 11),
		                 bg="#2b2b2b",
		                 fg="#d4d4d4")
		label.pack(side="left")

		controls_frame = tk.Frame(setting_frame, bg="#2b2b2b")
		controls_frame.pack(side="right")

		minus_btn = tk.Button(controls_frame,
		                      text="−",
		                      command=self.decrease_value,
		                      bg="#3c3c3c",
		                      fg="white",
		                      font=("Sans", 14, "bold"),
		                      width=3,
		                      relief="flat",
		                      cursor="hand2")
		minus_btn.pack(side="left", padx=5)

		self.value_label = tk.Label(controls_frame,
		                            text=str(self.current_value),
		                            font=("Sans", 14, "bold"),
		                            bg="#1e1e1e",
		                            fg="#00ff00",
		                            width=5,
		                            relief="sunken",
		                            borderwidth=2)
		self.value_label.pack(side="left", padx=5)

		plus_btn = tk.Button(controls_frame,
		                     text="+",
		                     command=self.increase_value,
		                     bg="#3c3c3c",
		                     fg="white",
		                     font=("Sans", 14, "bold"),
		                     width=3,
		                     relief="flat",
		                     cursor="hand2")
		plus_btn.pack(side="left", padx=5)

		# Buttons
		button_frame = tk.Frame(self.window, bg="#1e1e1e")
		button_frame.pack(pady=20, padx=20, fill="x")

		cancel_btn = tk.Button(button_frame,
		                       text="ANNULER",
		                       command=self.window.destroy,
		                       bg="#5c5c5c",
		                       fg="white",
		                       font=("Sans", 11, "bold"),
		                       padx=30,
		                       pady=10,
		                       cursor="hand2",
		                       relief="flat")
		cancel_btn.pack(side="left", padx=10)

		apply_btn = tk.Button(button_frame,
		                      text="APPLIQUER",
		                      command=self.apply_settings,
		                      bg="#0e639c",
		                      fg="white",
		                      font=("Sans", 11, "bold"),
		                      padx=30,
		                      pady=10,
		                      cursor="hand2",
		                      relief="flat")
		apply_btn.pack(side="right", padx=10)

	def decrease_value(self) -> None:
		if self.current_value > 1:
			self.current_value -= 1
			self.value_label.config(text=str(self.current_value))

	def increase_value(self) -> None:
		if self.current_value < 100:
			self.current_value += 1
			self.value_label.config(text=str(self.current_value))

	def apply_settings(self) -> None:
		old_size = config.get_history_size()
		if self.current_value != old_size:
			if self.history_window.history_manager.set_max_size(self.current_value):
				self.history_window.update_title()
				self.history_window.update_content()

				messagebox.showinfo("Paramètres",
				                    f"✓ Configuration sauvegardée\nTaille de l'historique: {self.current_value}",
				                    parent=self.window)
				self.window.destroy()
			else:
				messagebox.showerror("Erreur", "Impossible de sauvegarder la configuration", parent=self.window)
		else:
			self.window.destroy()
