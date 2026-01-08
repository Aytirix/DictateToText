"""History window with CustomTkinter - Modern Design"""

import customtkinter as ctk
from typing import TYPE_CHECKING
import threading
import queue

import config

if TYPE_CHECKING:
	from components import HistoryManager, TranscriptionWorker


def _enable_mousewheel_scroll(widget):
	"""Enable mousewheel scrolling for a widget and all its children"""

	def _on_mousewheel(event):
		# Try to scroll the widget
		try:
			if hasattr(widget, '_parent_canvas'):
				# For CTkScrollableFrame
				widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
			elif hasattr(widget, '_textbox'):
				# For CTkTextbox
				widget._textbox.yview_scroll(int(-1 * (event.delta / 120)), "units")
		except:
			pass

	def _on_mousewheel_linux(event):
		# Linux uses Button-4 and Button-5 for scroll
		try:
			if hasattr(widget, '_parent_canvas'):
				if event.num == 4:
					widget._parent_canvas.yview_scroll(-1, "units")
				elif event.num == 5:
					widget._parent_canvas.yview_scroll(1, "units")
			elif hasattr(widget, '_textbox'):
				if event.num == 4:
					widget._textbox.yview_scroll(-1, "units")
				elif event.num == 5:
					widget._textbox.yview_scroll(1, "units")
		except:
			pass

	# Bind for Windows/Mac
	widget.bind("<MouseWheel>", _on_mousewheel, add="+")
	# Bind for Linux
	widget.bind("<Button-4>", _on_mousewheel_linux, add="+")
	widget.bind("<Button-5>", _on_mousewheel_linux, add="+")


class HistoryWindow:
	"""Modern history window with CustomTkinter"""

	def __init__(self, history_manager: 'HistoryManager', worker: 'TranscriptionWorker'):
		self.history_manager = history_manager
		self.worker = worker

		# Logs en temps réel
		self.logs_queue = queue.Queue()
		self.logs_thread = None
		self.logs_running = False

		# Charger config
		cfg = config.get_config_instance()

		# Configurer thème CustomTkinter
		ctk.set_appearance_mode(cfg.get("theme_mode", "dark"))
		ctk.set_default_color_theme(cfg.get("accent_color", "blue"))

		self.window = ctk.CTk()
		self._setup_ui(cfg)

		# Attach as observer
		self.history_manager.attach_observer(self)

		# Schedule status updates
		self.schedule_update()

	def _setup_ui(self, cfg) -> None:
		"""Setup the modern user interface"""
		self.update_title()
		self.window.geometry("800x600")

		# Opacity
		opacity = cfg.get("window_opacity", 1.0)
		self.window.attributes("-alpha", opacity)

		self.window.protocol("WM_DELETE_WINDOW", self.on_close)

		# Header frame avec gradient effect
		header_frame = ctk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
		header_frame.pack(fill="x", padx=20, pady=(20, 10))

		# Titre avec icône
		title_label = ctk.CTkLabel(header_frame,
		                           text="📜 Historique des Transcriptions",
		                           font=ctk.CTkFont(size=24, weight="bold"),
		                           anchor="w")
		title_label.pack(side="left", fill="x", expand=True)

		# Status indicator (moderne)
		self.status_frame = ctk.CTkFrame(header_frame, corner_radius=15)
		self.status_frame.pack(side="right", padx=10)

		self.status_indicator = ctk.CTkLabel(self.status_frame,
		                                     text="●",
		                                     font=ctk.CTkFont(size=20),
		                                     text_color="#00ff00",
		                                     width=10)
		self.status_indicator.pack(side="left", padx=(10, 5), pady=5)

		self.status_label = ctk.CTkLabel(self.status_frame, text="Prêt", font=ctk.CTkFont(size=12, weight="bold"))
		self.status_label.pack(side="left", padx=(0, 10), pady=5)

		# Settings button (moderne avec icône)
		settings_btn = ctk.CTkButton(header_frame,
		                             text="⚙️",
		                             width=40,
		                             height=40,
		                             corner_radius=20,
		                             command=self.open_config,
		                             font=ctk.CTkFont(size=20),
		                             fg_color="transparent",
		                             hover_color=("gray70", "gray30"))
		settings_btn.pack(side="right")

		# Tabbed interface
		self.tabview = ctk.CTkTabview(self.window, corner_radius=10)
		self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))

		# Create tabs
		self.tab_history = self.tabview.add("📜 Historique")
		self.tab_stats = self.tabview.add("📊 Statistiques")
		self.tab_logs = self.tabview.add("📋 Logs")

		# Conditionally add Audio Files tab
		if cfg.get("save_audio_files", False):
			self.tab_audio = self.tabview.add("🎵 Fichiers Audio")
		else:
			self.tab_audio = None

		# === TAB 1: HISTORIQUE ===
		# Search frame (si activé)
		if cfg.get("history_search", True):
			search_frame = ctk.CTkFrame(self.tab_history, fg_color="transparent")
			search_frame.pack(fill="x", padx=10, pady=(10, 10))

			self.search_entry = ctk.CTkEntry(search_frame,
			                                 placeholder_text="🔍 Rechercher dans l'historique...",
			                                 height=40,
			                                 corner_radius=10,
			                                 font=ctk.CTkFont(size=14))
			self.search_entry.pack(fill="x", side="left", expand=True)
			self.search_entry.bind("<KeyRelease>", self._on_search)

			clear_search_btn = ctk.CTkButton(search_frame,
			                                 text="✕",
			                                 width=40,
			                                 height=40,
			                                 corner_radius=10,
			                                 command=self._clear_search,
			                                 fg_color="transparent",
			                                 hover_color=("gray70", "gray30"))
			clear_search_btn.pack(side="right", padx=(10, 0))

		# Text widget for history
		self.text_widget = ctk.CTkTextbox(self.tab_history,
		                                  wrap="word",
		                                  corner_radius=10,
		                                  font=ctk.CTkFont(size=cfg.get("font_size", 12)))
		self.text_widget.pack(fill="both", expand=True, padx=10, pady=(0, 10))
		_enable_mousewheel_scroll(self.text_widget)

		# Bottom button frame for history tab
		button_frame = ctk.CTkFrame(self.tab_history, fg_color="transparent")
		button_frame.pack(fill="x", padx=10, pady=(0, 10))

		clear_btn = ctk.CTkButton(button_frame,
		                          text="🗑️ Vider",
		                          command=self._clear_history,
		                          width=100,
		                          height=35,
		                          corner_radius=8,
		                          fg_color="#d32f2f",
		                          hover_color="#b71c1c",
		                          font=ctk.CTkFont(size=13, weight="bold"))
		clear_btn.pack(side="left", padx=5)

		export_btn = ctk.CTkButton(button_frame,
		                           text="📤 Exporter",
		                           command=self._export_history,
		                           width=120,
		                           height=35,
		                           corner_radius=8,
		                           font=ctk.CTkFont(size=13, weight="bold"))
		export_btn.pack(side="right", padx=5)

		# === TAB 2: STATISTIQUES ===
		stats_main = ctk.CTkFrame(self.tab_stats, fg_color="transparent")
		stats_main.pack(fill="both", expand=True, padx=10, pady=10)

		# Title
		stats_title = ctk.CTkLabel(stats_main, text="📊 Statistiques Système", font=ctk.CTkFont(size=20, weight="bold"))
		stats_title.pack(pady=(10, 20))

		# Horizontal container for stats
		stats_row = ctk.CTkFrame(stats_main, fg_color="transparent")
		stats_row.pack(fill="both", expand=True, padx=10)

		# CPU Frame
		cpu_frame = ctk.CTkFrame(stats_row, corner_radius=10)
		cpu_frame.pack(side="left", fill="both", expand=True, padx=5)

		cpu_label = ctk.CTkLabel(cpu_frame, text="🖥️ CPU", font=ctk.CTkFont(size=16, weight="bold"))
		cpu_label.pack(pady=(15, 10))

		self.cpu_text = ctk.CTkLabel(cpu_frame, text="0.0%", font=ctk.CTkFont(size=18, weight="bold"))
		self.cpu_text.pack(pady=(0, 10))

		self.cpu_bar = ctk.CTkProgressBar(cpu_frame, width=30, height=200, orientation="vertical")
		self.cpu_bar.pack(pady=15, padx=20)
		self.cpu_bar.set(0)

		# RAM Frame
		ram_frame = ctk.CTkFrame(stats_row, corner_radius=10)
		ram_frame.pack(side="left", fill="both", expand=True, padx=5)

		ram_label = ctk.CTkLabel(ram_frame, text="💾 RAM", font=ctk.CTkFont(size=16, weight="bold"))
		ram_label.pack(pady=(15, 10))

		self.ram_text = ctk.CTkLabel(ram_frame, text="0 MB", font=ctk.CTkFont(size=14, weight="bold"))
		self.ram_text.pack(pady=(0, 10))

		self.ram_bar = ctk.CTkProgressBar(ram_frame, width=30, height=200, orientation="vertical")
		self.ram_bar.pack(pady=15, padx=20)
		self.ram_bar.set(0)

		# GPU Frame
		gpu_frame = ctk.CTkFrame(stats_row, corner_radius=10)
		gpu_frame.pack(side="left", fill="both", expand=True, padx=5)

		gpu_label = ctk.CTkLabel(gpu_frame, text="🎮 GPU", font=ctk.CTkFont(size=16, weight="bold"))
		gpu_label.pack(pady=(15, 10))

		self.gpu_text = ctk.CTkLabel(gpu_frame,
		                             text="Chargement...",
		                             font=ctk.CTkFont(size=11),
		                             wraplength=180,
		                             justify="center")
		self.gpu_text.pack(pady=(0, 10), padx=10)

		# GPU bars container
		gpu_bars_frame = ctk.CTkFrame(gpu_frame, fg_color="transparent")
		gpu_bars_frame.pack(pady=(0, 15))

		# GPU Utilization bar
		gpu_util_container = ctk.CTkFrame(gpu_bars_frame, fg_color="transparent")
		gpu_util_container.pack(side="left", padx=10)

		gpu_util_label = ctk.CTkLabel(gpu_util_container, text="Utilisation", font=ctk.CTkFont(size=10))
		gpu_util_label.pack(pady=(0, 5))

		self.gpu_util_bar = ctk.CTkProgressBar(gpu_util_container, width=30, height=150, orientation="vertical")
		self.gpu_util_bar.pack(pady=(0, 5))
		self.gpu_util_bar.set(0)

		self.gpu_util_text = ctk.CTkLabel(gpu_util_container, text="0%", font=ctk.CTkFont(size=10, weight="bold"))
		self.gpu_util_text.pack()

		# GPU Memory bar
		gpu_mem_container = ctk.CTkFrame(gpu_bars_frame, fg_color="transparent")
		gpu_mem_container.pack(side="left", padx=10)

		gpu_mem_label = ctk.CTkLabel(gpu_mem_container, text="VRAM", font=ctk.CTkFont(size=10))
		gpu_mem_label.pack(pady=(0, 5))

		self.gpu_mem_bar = ctk.CTkProgressBar(gpu_mem_container, width=30, height=150, orientation="vertical")
		self.gpu_mem_bar.pack(pady=(0, 5))
		self.gpu_mem_bar.set(0)

		self.gpu_mem_text = ctk.CTkLabel(gpu_mem_container, text="0 MB", font=ctk.CTkFont(size=10, weight="bold"))
		self.gpu_mem_text.pack()

		# === TAB 3: LOGS ===
		logs_container = ctk.CTkFrame(self.tab_logs, fg_color="transparent")
		logs_container.pack(fill="both", expand=True, padx=10, pady=10)

		# Logs textbox
		self.logs_widget = ctk.CTkTextbox(logs_container,
		                                  wrap="word",
		                                  corner_radius=10,
		                                  font=ctk.CTkFont(family="Courier", size=11))
		self.logs_widget.pack(fill="both", expand=True)
		self.logs_widget.insert("1.0", "📋 Logs du système\n" + "=" * 50 + "\n\n")
		self.logs_widget.insert("end", "Cliquez sur 'Actualiser' pour charger les logs...\n")
		self.logs_widget.configure(state="disabled")
		_enable_mousewheel_scroll(self.logs_widget)

		# Logs control buttons
		logs_btn_frame = ctk.CTkFrame(logs_container, fg_color="transparent")
		logs_btn_frame.pack(fill="x", pady=(10, 0))

		clear_logs_btn = ctk.CTkButton(logs_btn_frame,
		                               text="🗑️ Effacer",
		                               command=self.clear_logs,
		                               width=100,
		                               height=32,
		                               corner_radius=8)
		clear_logs_btn.pack(side="left", padx=5)

		self.realtime_logs_btn = ctk.CTkButton(logs_btn_frame,
		                                       text="▶️ Temps réel",
		                                       command=self.toggle_realtime_logs,
		                                       width=120,
		                                       height=32,
		                                       corner_radius=8)
		self.realtime_logs_btn.pack(side="left", padx=5)

		# === TAB 4: FICHIERS AUDIO (conditionnel) ===
		if self.tab_audio:
			audio_container = ctk.CTkFrame(self.tab_audio, fg_color="transparent")
			audio_container.pack(fill="both", expand=True, padx=10, pady=10)

			# Title and controls
			audio_header = ctk.CTkFrame(audio_container, fg_color="transparent")
			audio_header.pack(fill="x", pady=(0, 10))

			audio_title = ctk.CTkLabel(audio_header,
			                           text="🎵 Fichiers Audio Enregistrés",
			                           font=ctk.CTkFont(size=16, weight="bold"))
			audio_title.pack(side="left")

			delete_all_btn = ctk.CTkButton(audio_header,
			                               text="🗑️ Tout supprimer",
			                               command=self._delete_all_audio,
			                               width=130,
			                               height=32,
			                               fg_color="#d32f2f",
			                               hover_color="#b71c1c",
			                               corner_radius=8)
			delete_all_btn.pack(side="right", padx=5)

			refresh_audio_btn = ctk.CTkButton(audio_header,
			                                  text="🔄 Actualiser",
			                                  command=self._refresh_audio_list,
			                                  width=110,
			                                  height=32,
			                                  corner_radius=8)
			refresh_audio_btn.pack(side="right", padx=5)

			# Scrollable frame for audio files
			self.audio_list_frame = ctk.CTkScrollableFrame(audio_container, corner_radius=10)
			self.audio_list_frame.pack(fill="both", expand=True)
			_enable_mousewheel_scroll(self.audio_list_frame)

			# Initial load
		self._refresh_audio_list()

	def _on_search(self, event=None):
		"""Handle search"""
		query = self.search_entry.get().lower()
		self.update_content(search_query=query)

	def _clear_search(self):
		"""Clear search"""
		self.search_entry.delete(0, 'end')
		self.update_content()

	def _export_history(self):
		"""Export history"""
		cfg = config.get_config_instance()
		format_type = cfg.get("history_export_format", "txt")

		from tkinter import filedialog
		import json
		import csv
		from datetime import datetime

		filename = filedialog.asksaveasfilename(defaultextension=f".{format_type}",
		                                        filetypes=[(f"{format_type.upper()} files", f"*.{format_type}"),
		                                                   ("All files", "*.*")])

		if filename:
			try:
				if format_type == "txt":
					with open(filename, "w", encoding="utf-8") as f:
						f.write(f"Historique Dictate PTT - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
						f.write("=" * 60 + "\n\n")
						for i, text in enumerate(self.history_manager.items, 1):
							f.write(f"{i}. {text}\n\n")
				elif format_type == "json":
					with open(filename, "w", encoding="utf-8") as f:
						json.dump({
						    "export_date": datetime.now().isoformat(),
						    "items": self.history_manager.items
						},
						          f,
						          indent=2,
						          ensure_ascii=False)
				elif format_type == "csv":
					with open(filename, "w", newline="", encoding="utf-8") as f:
						writer = csv.writer(f)
						writer.writerow(["Index", "Texte"])
						for i, text in enumerate(self.history_manager.items, 1):
							writer.writerow([i, text])

				# Success notification
				from services import NotificationService
				NotificationService.send("Export réussi", f"Historique exporté vers {filename}")
			except Exception as e:
				print(f"Erreur export: {e}")

	def _clear_history(self):
		"""Clear all history with confirmation"""
		from tkinter import messagebox

		if messagebox.askyesno("Confirmation", "Voulez-vous vraiment vider tout l'historique ?"):
			self.history_manager.items.clear()
			config.save_history([])
			self.update_content()

	def schedule_update(self) -> None:
		"""Schedule periodic status updates"""
		if self.window.winfo_exists():
			self.update_status()
			self.window.after(200, self.schedule_update)

	def update_status(self) -> None:
		"""Update transcription status indicator"""
		if self.worker.is_transcribing():
			self.status_indicator.configure(text_color="#ffa500")
			self.status_label.configure(text="Transcription en cours...")
		else:
			self.status_indicator.configure(text_color="#00ff00")
			self.status_label.configure(text="Prêt")

	def update_content(self, search_query: str = "") -> None:
		"""Update history content with optional search"""
		self.text_widget.configure(state="normal")
		self.text_widget.delete("1.0", "end")

		items = self.history_manager.items

		# Filter if searching
		if search_query:
			items = [item for item in items if search_query in item.lower()]

		if not items:
			empty_text = "Aucun résultat" if search_query else "Historique vide"
			self.text_widget.insert("1.0", f"\n\n          {empty_text}\n\n")
		else:
			for i, text in enumerate(reversed(items), 1):
				# Numéro avec style
				self.text_widget.insert("end", f"{i:2}. ", "number")
				self.text_widget.insert("end", f"{text}\n\n", "content")

		self.text_widget.configure(state="disabled")
		self.update_status()

	def update_stats(self) -> None:
		"""Update system statistics"""
		try:
			import psutil

			# CPU
			cpu_percent = psutil.cpu_percent(interval=0.1)
			self.cpu_bar.set(cpu_percent / 100.0)
			self.cpu_text.configure(text=f"{cpu_percent:.1f}%")

			# RAM
			mem = psutil.virtual_memory()
			ram_percent = mem.percent
			ram_used = mem.used / (1024**3)  # GB
			ram_total = mem.total / (1024**3)  # GB
			self.ram_bar.set(ram_percent / 100.0)
			self.ram_text.configure(text=f"{ram_used:.1f} / {ram_total:.1f} GB\n({ram_percent:.1f}%)")

			# GPU - détection automatique
			self._update_gpu_info()

		except ImportError:
			self.cpu_text.configure(text="psutil non installé")
			self.ram_text.configure(text="psutil non installé")
		except Exception as e:
			self.cpu_text.configure(text=f"Erreur: {e}")

		# Schedule next update
		self.window.after(2000, self.update_stats)

	def _update_gpu_info(self) -> None:
		"""Update GPU information - supports NVIDIA, AMD, Intel"""
		import subprocess

		gpu_info = None

		# Try NVIDIA GPU first
		try:
			result = subprocess.run([
			    "nvidia-smi", "--query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total",
			    "--format=csv,noheader,nounits"
			],
			                        capture_output=True,
			                        text=True,
			                        timeout=2)
			if result.returncode == 0 and result.stdout.strip():
				parts = result.stdout.strip().split(', ')
				if len(parts) >= 5:
					name = parts[0]
					temp = parts[1]
					util = parts[2]
					mem_used = parts[3]
					mem_total = parts[4]
					gpu_info = f"{name}\n{temp}°C"

					# Update progress bars
					try:
						util_percent = float(util)
						mem_used_mb = float(mem_used)
						mem_total_mb = float(mem_total)
						mem_percent = (mem_used_mb / mem_total_mb * 100) if mem_total_mb > 0 else 0

						self.gpu_util_bar.set(util_percent / 100.0)
						self.gpu_util_text.configure(text=f"{util_percent:.0f}%")

						self.gpu_mem_bar.set(mem_percent / 100.0)
						self.gpu_mem_text.configure(text=f"{mem_used_mb:.0f}/{mem_total_mb:.0f} MB")
					except ValueError:
						pass
		except (FileNotFoundError, subprocess.TimeoutExpired):
			pass

		# Try AMD GPU
		if not gpu_info:
			try:
				result = subprocess.run(["rocm-smi", "--showuse", "--showtemp", "--showmeminfo", "vram"],
				                        capture_output=True,
				                        text=True,
				                        timeout=2)
				if result.returncode == 0 and result.stdout.strip():
					gpu_info = "GPU AMD détecté\n" + result.stdout.strip()[:100]
			except (FileNotFoundError, subprocess.TimeoutExpired):
				pass

		# Try Intel GPU via sysfs
		if not gpu_info:
			try:
				# Check for Intel GPU
				result = subprocess.run(["lspci"], capture_output=True, text=True, timeout=2)
				if result.returncode == 0:
					for line in result.stdout.split('\n'):
						if 'VGA' in line or 'Display' in line or '3D' in line:
							if 'Intel' in line or 'AMD' in line or 'NVIDIA' in line:
								# Extract GPU name
								gpu_name = line.split(': ', 1)[-1] if ': ' in line else line
								gpu_info = f"{gpu_name}\nIntégré"
								break
			except (FileNotFoundError, subprocess.TimeoutExpired):
				pass

		# Fallback: try to get any GPU info from lspci
		if not gpu_info:
			try:
				result = subprocess.run(["lspci", "-v"], capture_output=True, text=True, timeout=2)
				if result.returncode == 0:
					lines = result.stdout.split('\n')
					for i, line in enumerate(lines):
						if ('VGA compatible controller' in line or '3D controller' in line
						    or 'Display controller' in line):
							gpu_info = line.split(': ', 1)[-1] if ': ' in line else "GPU détecté"
							# Try to get more details
							if i + 1 < len(lines):
								next_line = lines[i + 1].strip()
								if next_line.startswith('Subsystem:'):
									gpu_info += "\n" + next_line.replace('Subsystem: ', '')
							break
			except (FileNotFoundError, subprocess.TimeoutExpired):
				pass

		# Update UI
		if gpu_info:
			self.gpu_text.configure(text=gpu_info, text_color=("black", "white"))
		else:
			self.gpu_text.configure(text="Aucun GPU détecté", text_color="gray")
			self.gpu_util_bar.set(0)
			self.gpu_util_text.configure(text="0%")
			self.gpu_mem_bar.set(0)
			self.gpu_mem_text.configure(text="0 MB")

	def toggle_realtime_logs(self) -> None:
		"""Toggle real-time logs"""
		if self.logs_running:
			self.stop_realtime_logs()
		else:
			self.start_realtime_logs()

	def start_realtime_logs(self) -> None:
		"""Start real-time log streaming"""
		if self.logs_running:
			return

		self.logs_running = True
		self.realtime_logs_btn.configure(text="⏸️ Pause", fg_color="#c44536")

		# Clear and show initial message
		self.logs_widget.configure(state="normal")
		self.logs_widget.delete("1.0", "end")
		self.logs_widget.insert("1.0", "📋 Logs en temps réel\n" + "=" * 80 + "\n\n")
		self.logs_widget.configure(state="disabled")

		# Start thread
		self.logs_thread = threading.Thread(target=self._logs_reader_thread, daemon=True)
		self.logs_thread.start()

		# Start UI updater
		self._update_logs_from_queue()

	def stop_realtime_logs(self) -> None:
		"""Stop real-time log streaming"""
		self.logs_running = False
		self.realtime_logs_btn.configure(text="▶️ Temps réel", fg_color=["#3B8ED0", "#1F6AA5"])

	def _logs_reader_thread(self) -> None:
		"""Thread that reads logs from journalctl -f"""
		import subprocess

		try:
			process = subprocess.Popen(["journalctl", "--user", "-u", "dictate-ptt.service", "-f", "--no-pager"],
			                           stdout=subprocess.PIPE,
			                           stderr=subprocess.PIPE,
			                           text=True,
			                           bufsize=1)

			while self.logs_running:
				line = process.stdout.readline()
				if line:
					self.logs_queue.put(line)
				else:
					break

			process.terminate()
			process.wait(timeout=2)

		except Exception as e:
			self.logs_queue.put(f"Erreur thread logs: {e}\n")

	def _update_logs_from_queue(self) -> None:
		"""Update logs widget from queue (called from main thread)"""
		if not self.logs_running:
			return

		try:
			while True:
				line = self.logs_queue.get_nowait()
				self.logs_widget.configure(state="normal")
				self.logs_widget.insert("end", line)
				self.logs_widget.see("end")
				self.logs_widget.configure(state="disabled")
		except queue.Empty:
			pass

		# Schedule next update
		if self.logs_running:
			self.window.after(100, self._update_logs_from_queue)

	def clear_logs(self) -> None:
		"""Clear logs display"""
		self.logs_widget.configure(state="normal")
		self.logs_widget.delete("1.0", "end")
		self.logs_widget.insert("1.0", "📋 Logs du système\n" + "=" * 50 + "\n\n")
		self.logs_widget.insert("end", f"Logs effacés\n")
		self.logs_widget.configure(state="disabled")

	def refresh_logs(self) -> None:
		"""Refresh logs from journalctl"""
		import subprocess
		from datetime import datetime

		self.logs_widget.configure(state="normal")

		try:
			result = subprocess.run(["journalctl", "--user", "-u", "dictate-ptt.service", "-n", "100", "--no-pager"],
			                        capture_output=True,
			                        text=True,
			                        timeout=5)

			self.logs_widget.delete("1.0", "end")
			self.logs_widget.insert("1.0", f"📋 Logs du système (actualisé {datetime.now().strftime('%H:%M:%S')})\n")
			self.logs_widget.insert("end", "=" * 80 + "\n\n")

			if result.returncode == 0:
				self.logs_widget.insert("end", result.stdout)
			else:
				self.logs_widget.insert("end", f"Erreur lors de la récupération des logs\n{result.stderr}")

		except subprocess.TimeoutExpired:
			self.logs_widget.insert("end", "Timeout lors de la récupération des logs\n")
		except FileNotFoundError:
			self.logs_widget.insert("end", "journalctl non trouvé\n")
		except Exception as e:
			self.logs_widget.insert("end", f"Erreur: {e}\n")

		self.logs_widget.configure(state="disabled")
		self.logs_widget.see("end")

	def _refresh_audio_list(self) -> None:
		"""Refresh the list of audio files"""
		if not self.tab_audio:
			return

		import os
		from pathlib import Path
		from datetime import datetime

		# Clear current list
		for widget in self.audio_list_frame.winfo_children():
			widget.destroy()

		cfg = config.get_config_instance()
		audio_dir = Path(cfg.get("audio_temp_dir", "~/Documents/tools/py/audio_temp")).expanduser()

		if not audio_dir.exists():
			no_files_label = ctk.CTkLabel(self.audio_list_frame,
			                              text="Aucun fichier audio trouvé",
			                              font=ctk.CTkFont(size=14),
			                              text_color="gray")
			no_files_label.pack(pady=20)
			return

		# Get all wav files
		audio_files = sorted(audio_dir.glob("dictate_ptt_*.wav"), key=lambda x: x.stat().st_mtime, reverse=True)

		if not audio_files:
			no_files_label = ctk.CTkLabel(self.audio_list_frame,
			                              text="Aucun fichier audio trouvé",
			                              font=ctk.CTkFont(size=14),
			                              text_color="gray")
			no_files_label.pack(pady=20)
			return

		# Display each audio file
		for audio_file in audio_files:
			file_frame = ctk.CTkFrame(self.audio_list_frame, corner_radius=8)
			file_frame.pack(fill="x", pady=5, padx=5)

			# File info
			info_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
			info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)

			file_name = audio_file.name
			file_size = audio_file.stat().st_size / 1024  # KB
			file_time = datetime.fromtimestamp(audio_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')

			name_label = ctk.CTkLabel(info_frame, text=file_name, font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
			name_label.pack(anchor="w")

			details_label = ctk.CTkLabel(info_frame,
			                             text=f"{file_size:.1f} KB  •  {file_time}",
			                             font=ctk.CTkFont(size=11),
			                             text_color="gray",
			                             anchor="w")
			details_label.pack(anchor="w")

			# Buttons
			buttons_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
			buttons_frame.pack(side="right", padx=10)

			play_btn = ctk.CTkButton(buttons_frame,
			                         text="▶️",
			                         width=35,
			                         height=32,
			                         fg_color="#2e7d32",
			                         hover_color="#1b5e20",
			                         command=lambda f=str(audio_file): self._play_audio(f))
			play_btn.pack(side="left", padx=3)

			delete_btn = ctk.CTkButton(buttons_frame,
			                           text="🗑️",
			                           width=35,
			                           height=32,
			                           fg_color="#d32f2f",
			                           hover_color="#b71c1c",
			                           command=lambda f=str(audio_file): self._delete_audio(f))
			delete_btn.pack(side="left", padx=3)

	def _play_audio(self, file_path: str) -> None:
		"""Play an audio file"""
		import subprocess
		import threading

		def play():
			try:
				# Try different audio players
				for player in ["paplay", "aplay", "ffplay", "mpv"]:
					try:
						if player == "ffplay":
							subprocess.run([player, "-nodisp", "-autoexit", file_path], check=True, capture_output=True)
						else:
							subprocess.run([player, file_path], check=True, capture_output=True)
						break
					except FileNotFoundError:
						continue
			except Exception as e:
				print(f"Erreur lecture audio: {e}")

		threading.Thread(target=play, daemon=True).start()

	def _delete_audio(self, file_path: str) -> None:
		"""Delete a single audio file"""
		import os
		from tkinter import messagebox

		if messagebox.askyesno("Supprimer le fichier",
		                       f"Voulez-vous vraiment supprimer ce fichier ?\n\n{os.path.basename(file_path)}",
		                       parent=self.window):
			try:
				os.remove(file_path)
				self._refresh_audio_list()
			except Exception as e:
				messagebox.showerror("Erreur", f"Impossible de supprimer le fichier: {e}", parent=self.window)

	def _delete_all_audio(self) -> None:
		"""Delete all audio files"""
		import os
		from pathlib import Path
		from tkinter import messagebox

		if messagebox.askyesno(
		    "Supprimer tous les fichiers",
		    "Voulez-vous vraiment supprimer TOUS les fichiers audio ?\n\nCette action est irréversible.",
		    parent=self.window):
			try:
				cfg = config.get_config_instance()
				audio_dir = Path(cfg.get("audio_temp_dir", "~/Documents/tools/py/audio_temp")).expanduser()

				if audio_dir.exists():
					for audio_file in audio_dir.glob("dictate_ptt_*.wav"):
						os.remove(audio_file)

				self._refresh_audio_list()
				messagebox.showinfo("✓ Succès", "Tous les fichiers audio ont été supprimés.", parent=self.window)
			except Exception as e:
				messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}", parent=self.window)

	def focus(self) -> None:
		"""Bring window to front"""
		self.window.lift()
		self.window.focus_force()

	def update_title(self) -> None:
		"""Update window title with history size"""
		size = config.get_history_size()
		self.window.title(f"📜 Historique Dictate PTT ({size} max)")

	def add_audio_tab(self) -> None:
		"""Add the audio files tab dynamically"""
		if self.tab_audio is not None:
			return  # Tab already exists

		# Add the tab
		self.tab_audio = self.tabview.add("🎵 Fichiers Audio")

		# Create the audio tab UI
		audio_container = ctk.CTkFrame(self.tab_audio, fg_color="transparent")
		audio_container.pack(fill="both", expand=True, padx=10, pady=10)

		# Title and controls
		audio_header = ctk.CTkFrame(audio_container, fg_color="transparent")
		audio_header.pack(fill="x", pady=(0, 10))

		audio_title = ctk.CTkLabel(audio_header,
		                           text="🎵 Fichiers Audio Enregistrés",
		                           font=ctk.CTkFont(size=16, weight="bold"))
		audio_title.pack(side="left")

		delete_all_btn = ctk.CTkButton(audio_header,
		                               text="🗑️ Tout supprimer",
		                               command=self._delete_all_audio,
		                               width=130,
		                               height=32,
		                               fg_color="#d32f2f",
		                               hover_color="#b71c1c",
		                               corner_radius=8)
		delete_all_btn.pack(side="right", padx=5)

		refresh_audio_btn = ctk.CTkButton(audio_header,
		                                  text="🔄 Actualiser",
		                                  command=self._refresh_audio_list,
		                                  width=110,
		                                  height=32,
		                                  corner_radius=8)
		refresh_audio_btn.pack(side="right", padx=5)

		# Scrollable frame for audio files
		self.audio_list_frame = ctk.CTkScrollableFrame(audio_container, corner_radius=10)
		self.audio_list_frame.pack(fill="both", expand=True)
		_enable_mousewheel_scroll(self.audio_list_frame)

		# Initial load
		self._refresh_audio_list()

	def remove_audio_tab(self) -> None:
		"""Remove the audio files tab dynamically"""
		if self.tab_audio is None:
			return  # Tab doesn't exist

		try:
			# Delete the tab
			self.tabview.delete("🎵 Fichiers Audio")
			self.tab_audio = None
			self.audio_list_frame = None
		except Exception as e:
			print(f"Erreur suppression onglet audio: {e}")

	def open_config(self) -> None:
		"""Open settings window"""
		from .settings_window_ctk import SettingsWindow
		SettingsWindow(self.window, self)

	def on_close(self) -> None:
		"""Handle window close"""
		self.stop_realtime_logs()
		self.window.destroy()

	def run(self) -> None:
		"""Start main loop"""
		self.window.mainloop()
