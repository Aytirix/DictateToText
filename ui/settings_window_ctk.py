"""Settings window with CustomTkinter - Modern Design"""

import os
import re
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING

import config

if TYPE_CHECKING:
	from .history_window_ctk import HistoryWindow


def _enable_mousewheel_scroll(widget):
	"""Enable mousewheel scrolling for a widget and all its children"""

	def _on_mousewheel(event):
		try:
			if hasattr(widget, '_parent_canvas'):
				widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
		except:
			pass

	def _on_mousewheel_linux(event):
		try:
			if hasattr(widget, '_parent_canvas'):
				if event.num == 4:
					widget._parent_canvas.yview_scroll(-1, "units")
				elif event.num == 5:
					widget._parent_canvas.yview_scroll(1, "units")
		except:
			pass

	widget.bind("<MouseWheel>", _on_mousewheel, add="+")
	widget.bind("<Button-4>", _on_mousewheel_linux, add="+")
	widget.bind("<Button-5>", _on_mousewheel_linux, add="+")


class SettingsWindow:
	"""Modern settings window with CustomTkinter"""

	DEFAULT_WHISPER_MODELS = [
	    "tiny",
	    "tiny.en",
	    "tiny-q5_1",
	    "tiny.en-q5_1",
	    "tiny-q8_0",
	    "base",
	    "base.en",
	    "base-q5_1",
	    "base.en-q5_1",
	    "base-q8_0",
	    "small",
	    "small.en",
	    "small.en-tdrz",
	    "small-q5_1",
	    "small.en-q5_1",
	    "small-q8_0",
	    "medium",
	    "medium.en",
	    "medium-q5_0",
	    "medium.en-q5_0",
	    "medium-q8_0",
	    "large-v1",
	    "large-v2",
	    "large-v2-q5_0",
	    "large-v2-q8_0",
	    "large-v3",
	    "large-v3-q5_0",
	    "large-v3-turbo",
	    "large-v3-turbo-q5_0",
	    "large-v3-turbo-q8_0",
	]

	MODEL_METADATA = {
	    "tiny": {"size": "75 MB", "speed": "⚡⚡⚡⚡⚡", "quality": "⭐⭐", "label": "Polyglotte"},
	    "base": {"size": "142 MB", "speed": "⚡⚡⚡⚡", "quality": "⭐⭐⭐", "label": "Polyglotte"},
	    "small": {"size": "466 MB", "speed": "⚡⚡⚡", "quality": "⭐⭐⭐⭐", "label": "Polyglotte"},
	    "medium": {"size": "1.5 GB", "speed": "⚡⚡", "quality": "⭐⭐⭐⭐⭐", "label": "Polyglotte"},
	    "large-v1": {"size": "2.9 GB", "speed": "⚡", "quality": "⭐⭐⭐⭐", "label": "Legacy"},
	    "large-v2": {"size": "2.9 GB", "speed": "⚡", "quality": "⭐⭐⭐⭐⭐", "label": "Legacy"},
	    "large-v3": {"size": "2.9 GB", "speed": "⚡", "quality": "⭐⭐⭐⭐⭐", "label": "Référence"},
	    "large-v3-turbo": {"size": "~1.6 GB", "speed": "⚡⚡⚡⚡", "quality": "⭐⭐⭐⭐", "label": "Optimisé transcription"},
	}

	def __init__(self, parent, history_window: 'HistoryWindow'):
		self.parent = parent
		self.history_window = history_window
		self.cfg = config.get_config_instance()

		self.window = ctk.CTkToplevel(parent)
		self.current_category = "Interface"
		self.category_buttons = {}

		self._setup_ui()

		# Rendre modale après création des widgets
		self.window.after(10, self._make_modal)

	def _make_modal(self):
		"""Make window modal after it's viewable"""
		try:
			self.window.grab_set()
		except:
			pass

	def _setup_ui(self) -> None:
		"""Setup modern settings UI"""
		self.window.title("⚙️ Paramètres")
		self.window.geometry("1000x700")

		# Rendre fenêtre fille
		self.window.transient(self.parent)

		# Header
		header = ctk.CTkFrame(self.window, corner_radius=0, height=70)
		header.pack(fill="x", padx=0, pady=0)
		header.pack_propagate(False)

		title = ctk.CTkLabel(header, text="⚙️ Paramètres", font=ctk.CTkFont(size=26, weight="bold"))
		title.pack(pady=18)

		# Main container with sidebar + content
		main_container = ctk.CTkFrame(self.window, fg_color="transparent")
		main_container.pack(fill="both", expand=True, padx=0, pady=0)

		# Sidebar menu
		sidebar = ctk.CTkFrame(main_container, width=200, corner_radius=0)
		sidebar.pack(side="left", fill="y", padx=0, pady=0)
		sidebar.pack_propagate(False)

		categories = [
		    ("🎨 Interface", "Interface"),
		    ("🎙️ Audio", "Audio"),
		    ("🤖 Whisper", "Whisper"),
		    ("📦 Modèles", "Modeles"),
		    ("📝 Historique", "Historique"),
		    ("🔔 Notifications", "Notifications"),
		    ("🔧 Comportement", "Comportement"),
		    ("🐛 Debug", "Debug"),
		]

		for icon_label, category in categories:
			btn = ctk.CTkButton(sidebar,
			                    text=icon_label,
			                    height=45,
			                    corner_radius=0,
			                    font=ctk.CTkFont(size=14, weight="bold"),
			                    anchor="w",
			                    fg_color="transparent",
			                    hover_color=("gray85", "gray25"),
			                    command=lambda c=category: self._switch_category(c))
			btn.pack(fill="x", padx=0, pady=1)
			self.category_buttons[category] = btn

		# Content area (scrollable)
		self.content_frame = ctk.CTkScrollableFrame(main_container, corner_radius=0, fg_color=("gray95", "gray10"))
		self.content_frame.pack(side="left", fill="both", expand=True, padx=0, pady=0)
		_enable_mousewheel_scroll(self.content_frame)

		# Initialize all variables
		self._init_variables()

		# Show first category
		self._switch_category("Interface")

		# Bottom buttons
		button_frame = ctk.CTkFrame(self.window, corner_radius=0, height=70)
		button_frame.pack(fill="x", padx=0, pady=0, side="bottom")
		button_frame.pack_propagate(False)

		buttons_inner = ctk.CTkFrame(button_frame, fg_color="transparent")
		buttons_inner.pack(expand=True)

		reset_btn = ctk.CTkButton(buttons_inner,
		                          text="🔄 Réinitialiser",
		                          height=38,
		                          width=140,
		                          corner_radius=10,
		                          command=self._reset_settings,
		                          fg_color="transparent",
		                          border_width=2,
		                          font=ctk.CTkFont(size=13, weight="bold"))
		reset_btn.pack(side="left", padx=8)

		cancel_btn = ctk.CTkButton(buttons_inner,
		                           text="Annuler",
		                           height=38,
		                           width=140,
		                           corner_radius=10,
		                           command=self.window.destroy,
		                           fg_color="gray40",
		                           hover_color="gray30",
		                           font=ctk.CTkFont(size=13, weight="bold"))
		cancel_btn.pack(side="left", padx=8)

		apply_btn = ctk.CTkButton(buttons_inner,
		                          text="✓ Appliquer",
		                          height=38,
		                          width=140,
		                          corner_radius=10,
		                          command=self._apply_settings,
		                          font=ctk.CTkFont(size=13, weight="bold"))
		apply_btn.pack(side="left", padx=8)

	def _init_variables(self):
		"""Initialize all configuration variables"""
		# Interface
		self.theme_var = ctk.StringVar(value=self.cfg.get("theme_mode", "dark"))
		self.accent_var = ctk.StringVar(value=self.cfg.get("accent_color", "blue"))
		self.opacity_var = ctk.DoubleVar(value=self.cfg.get("window_opacity", 1.0))
		self.font_size_var = ctk.IntVar(value=self.cfg.get("font_size", 12))
		self.animations_var = ctk.BooleanVar(value=self.cfg.get("animations_enabled", True))

		# Audio
		self.sample_rate_var = ctk.StringVar(value=str(self.cfg.get("sample_rate", 16000)))
		self.noise_reduction_var = ctk.BooleanVar(value=self.cfg.get("noise_reduction", False))
		self.auto_gain_var = ctk.BooleanVar(value=self.cfg.get("auto_gain", False))

		# Whisper
		self.model_var = ctk.StringVar(value=self.cfg.get("whisper_model", "large-v3"))
		self.language_var = ctk.StringVar(value=self.cfg.get("language", "fr"))
		self.task_var = ctk.StringVar(value=self.cfg.get("task", "transcribe"))
		self.beam_size_var = ctk.IntVar(value=self.cfg.get("beam_size", 5))

		# Historique
		self.history_size_var = ctk.IntVar(value=self.cfg.get("history_size", 10))
		self.history_search_var = ctk.BooleanVar(value=self.cfg.get("history_search", True))
		self.export_format_var = ctk.StringVar(value=self.cfg.get("history_export_format", "txt"))

		# Notifications
		self.notif_enabled_var = ctk.BooleanVar(value=self.cfg.get("notifications_enabled", True))
		self.notif_duration_var = ctk.IntVar(value=self.cfg.get("notification_duration", 3))

		# Comportement
		self.recording_mode_var = ctk.StringVar(value=self.cfg.get("recording_mode", "push_to_talk"))
		self.auto_start_var = ctk.BooleanVar(value=self.cfg.get("auto_start", False))
		self.minimize_tray_var = ctk.BooleanVar(value=self.cfg.get("minimize_to_tray", False))

		# Debug
		self.log_level_var = ctk.StringVar(value=self.cfg.get("log_level", "info"))
		self.log_to_file_var = ctk.BooleanVar(value=self.cfg.get("log_to_file", False))
		self.save_audio_var = ctk.BooleanVar(value=self.cfg.get("save_audio_files", False))

		# Chemins
		self.whisper_path_var = ctk.StringVar(value=self.cfg.get("whisper_path", "~/Documents/tools/whisper.cpp"))

	def _switch_category(self, category: str):
		"""Switch to a different settings category"""
		self.current_category = category

		# Update button colors
		for cat, btn in self.category_buttons.items():
			if cat == category:
				btn.configure(fg_color=("gray75", "gray28"))
			else:
				btn.configure(fg_color="transparent")

		# Clear content
		for widget in self.content_frame.winfo_children():
			widget.destroy()

		# Add padding frame
		padding = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=10)
		padding.pack(fill="x")

		# Show category content
		if category == "Interface":
			self._show_interface_settings()
		elif category == "Audio":
			self._show_audio_settings()
		elif category == "Whisper":
			self._show_whisper_settings()
		elif category == "Modeles":
			self._show_models_settings()
		elif category == "Historique":
			self._show_history_settings()
		elif category == "Notifications":
			self._show_notification_settings()
		elif category == "Comportement":
			self._show_behavior_settings()
		elif category == "Debug":
			self._show_debug_settings()

	def _show_interface_settings(self):
		"""Show interface settings"""
		self._create_category_title("🎨 Interface & Thème")

		self._create_option_menu(self.content_frame, "Mode d'apparence", self.theme_var, ["dark", "light", "system"])

		self._create_option_menu(self.content_frame, "Couleur d'accent", self.accent_var,
		                         ["blue", "green", "red", "dark-blue"])

		self._create_slider(self.content_frame, "Opacité des fenêtres", self.opacity_var, 0.7, 1.0)

		self._create_slider(self.content_frame, "Taille de police", self.font_size_var, 10, 20, is_int=True)

		self._create_switch(self.content_frame, "Animations activées", self.animations_var)

	def _show_audio_settings(self):
		"""Show audio settings"""
		self._create_category_title("🎙️ Audio & Enregistrement")

		self._create_option_menu_with_help(
		    self.content_frame, "Fréquence d'échantillonnage", self.sample_rate_var,
		    ["16000", "22050", "44100", "48000"], "Qualité audio en Hz. 16000 Hz est suffisant pour la voix. "
		    "44100 Hz est la qualité CD. Plus élevé = fichiers plus gros.")

		self._create_switch_with_help(
		    self.content_frame, "Réduction de bruit", self.noise_reduction_var,
		    "Filtre audio pour réduire le bruit de fond. "
		    "Utile dans environnements bruyants, mais peut affecter la qualité.")

		self._create_switch_with_help(
		    self.content_frame, "Normalisation automatique", self.auto_gain_var,
		    "Ajuste automatiquement le volume d'enregistrement. "
		    "Recommandé si votre micro est trop faible ou trop fort.")

	def _show_whisper_settings(self):
		"""Show Whisper settings"""
		self._create_category_title("🤖 Whisper & Transcription")

		# Whisper path
		frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
		frame.pack(fill="x", pady=8, padx=20)

		label = ctk.CTkLabel(frame, text="Répertoire Whisper.cpp", anchor="w", width=280)
		label.pack(side="left", padx=(0, 20))

		entry = ctk.CTkEntry(frame, textvariable=self.whisper_path_var, width=300, height=36)
		entry.pack(side="left", expand=True, fill="x")

		browse_btn = ctk.CTkButton(frame, text="📁", width=40, height=36, command=self._browse_whisper_path)
		browse_btn.pack(side="left", padx=(10, 0))

		self._create_option_menu_with_help(self.content_frame, "Langue", self.language_var,
		                                   ["fr", "en", "es", "de", "it", "auto"],
		                                   "Langue de transcription. 'auto' détecte automatiquement la langue.")

		self._create_option_menu_with_help(
		    self.content_frame, "Tâche", self.task_var, ["transcribe", "translate"],
		    "'transcribe' = texte dans la langue source. "
		    "'translate' = traduit vers l'anglais.")

		self._create_slider_with_help(
		    self.content_frame,
		    "Beam size",
		    self.beam_size_var,
		    1,
		    10,
		    is_int=True,
		    help_text="Algorithme de recherche. Plus élevé = meilleure qualité mais plus lent. "
		    "Recommandé: 5 pour usage normal, 1 pour vitesse max.")

	def _show_history_settings(self):
		"""Show history settings"""
		self._create_category_title("📝 Historique")

		self._create_slider(self.content_frame,
		                    "Taille maximale de l'historique",
		                    self.history_size_var,
		                    5,
		                    100,
		                    is_int=True)

		self._create_switch(self.content_frame, "Recherche dans l'historique", self.history_search_var)

		self._create_option_menu(self.content_frame, "Format d'export", self.export_format_var, ["txt", "json", "csv"])

	def _show_notification_settings(self):
		"""Show notification settings"""
		self._create_category_title("🔔 Notifications & Feedback")

		self._create_switch(self.content_frame, "Notifications activées", self.notif_enabled_var)

		self._create_slider(self.content_frame,
		                    "Durée des notifications (secondes)",
		                    self.notif_duration_var,
		                    1,
		                    10,
		                    is_int=True)

	def _show_behavior_settings(self):
		"""Show behavior settings"""
		self._create_category_title("🔧 Comportement")

		self._create_option_menu(self.content_frame, "Mode d'enregistrement", self.recording_mode_var,
		                         ["push_to_talk", "toggle"])

		self._create_switch(self.content_frame, "Lancer au démarrage", self.auto_start_var)
		self._create_switch(self.content_frame, "Minimiser vers barre système", self.minimize_tray_var)

	def _show_debug_settings(self):
		"""Show debug settings"""
		self._create_category_title("🐛 Debug & Logs")

		self._create_option_menu(self.content_frame, "Niveau de log", self.log_level_var,
		                         ["debug", "info", "warning", "error"])

		self._create_switch(self.content_frame, "Sauvegarder les logs", self.log_to_file_var)
		self._create_switch(self.content_frame, "Conserver fichiers audio temporaires", self.save_audio_var)

	def _show_models_settings(self):
		"""Show Whisper models management"""
		self._create_category_title("📦 Gestion des Modèles Whisper")

		# Info section
		info_frame = ctk.CTkFrame(self.content_frame, fg_color=("gray90", "gray20"), corner_radius=10)
		info_frame.pack(fill="x", padx=20, pady=(0, 20))

		info_label = ctk.CTkLabel(
		    info_frame,
		    text="💡 La liste s'adapte automatiquement à votre version locale de whisper.cpp. Cliquez sur un modèle pour le sélectionner ou téléchargez les modèles manquants.",
		    font=ctk.CTkFont(size=12),
		    wraplength=800)
		info_label.pack(pady=10, padx=10)

		# Get whisper path
		whisper_path = os.path.expanduser(self.cfg.get("whisper_path", "~/Documents/tools/whisper.cpp"))
		models_dir = os.path.join(whisper_path, "models")
		models = self._get_whisper_models(models_dir)
		current_model = self.cfg.get("whisper_model", "large-v3")
		models_sorted = self._sort_models(models, current_model, models_dir)

		for model_name in models_sorted:
			model_frame = ctk.CTkFrame(self.content_frame, corner_radius=10, height=80)
			model_frame.pack(fill="x", padx=20, pady=5)
			model_frame.pack_propagate(False)

			# Check if model exists
			model_path = os.path.join(models_dir, f"ggml-{model_name}.bin")
			exists = Path(model_path).exists()
			display = self._get_model_display(model_name)

			# Model info left side
			info_container = ctk.CTkFrame(model_frame, fg_color="transparent")
			info_container.pack(side="left", fill="both", expand=True, padx=15, pady=10)

			# Model name + current indicator
			name_text = f"🎯 {model_name}" if model_name == current_model else model_name
			name_label = ctk.CTkLabel(info_container,
			                          text=name_text,
			                          font=ctk.CTkFont(size=16, weight="bold"),
			                          anchor="w")
			name_label.pack(anchor="w")

			# Details
			details = f"{display['size']}  •  Vitesse: {display['speed']}  •  Qualité: {display['quality']}"
			if display["tags"]:
				details += f"  •  {display['tags']}"
			details_label = ctk.CTkLabel(info_container,
			                             text=details,
			                             font=ctk.CTkFont(size=11),
			                             text_color="gray",
			                             anchor="w")
			details_label.pack(anchor="w", pady=(2, 0))

			# Right side buttons
			buttons_container = ctk.CTkFrame(model_frame, fg_color="transparent")
			buttons_container.pack(side="right", padx=10)

			if exists:
				# Uninstall button (only if not current model)
				if model_name != current_model:
					uninstall_btn = ctk.CTkButton(buttons_container,
					                              text="🗑️",
					                              width=35,
					                              height=32,
					                              fg_color="#d32f2f",
					                              hover_color="#b71c1c",
					                              command=lambda m=model_name: self._uninstall_model(m))
					uninstall_btn.pack(side="right", padx=5)

				# Select button
				if model_name != current_model:
					select_btn = ctk.CTkButton(buttons_container,
					                           text="Sélectionner",
					                           width=100,
					                           height=32,
					                           command=lambda m=model_name: self._select_model(m))
					select_btn.pack(side="right", padx=5)
				else:
					# Currently selected
					current_label = ctk.CTkLabel(buttons_container,
					                             text="✓ Sélectionné",
					                             text_color="green",
					                             font=ctk.CTkFont(size=12, weight="bold"))
					current_label.pack(side="right", padx=10)
			else:
				# Download button
				download_btn = ctk.CTkButton(buttons_container,
				                             text="📥 Télécharger",
				                             width=120,
				                             height=32,
				                             fg_color="#1e88e5",
				                             hover_color="#1565c0",
				                             command=lambda m=model_name: self._download_model(m))
				download_btn.pack(side="right", padx=5)

	def _get_whisper_models(self, models_dir: str) -> list[str]:
		"""Return models supported by the local whisper.cpp install, plus installed files."""
		models: list[str] = []
		download_script = os.path.join(os.path.dirname(models_dir), "models", "download-ggml-model.sh")

		if os.path.exists(download_script):
			try:
				with open(download_script, "r", encoding="utf-8") as script_file:
					content = script_file.read()
				match = re.search(r'models="(.*?)"', content, re.S)
				if match:
					models.extend(line.strip() for line in match.group(1).splitlines() if line.strip())
			except Exception:
				pass

		if not models:
			models.extend(self.DEFAULT_WHISPER_MODELS)

		try:
			for filename in sorted(os.listdir(models_dir)):
				if filename.startswith("ggml-") and filename.endswith(".bin"):
					model_name = filename[len("ggml-"):-len(".bin")]
					if model_name not in models:
						models.append(model_name)
		except OSError:
			pass

		current_model = self.cfg.get("whisper_model", "large-v3")
		if current_model and current_model not in models:
			models.insert(0, current_model)

		return models

	def _sort_models(self, models: list[str], current_model: str, models_dir: str) -> list[str]:
		"""Sort current and installed models first, then keep whisper.cpp order."""
		model_order = {model_name: index for index, model_name in enumerate(dict.fromkeys(models))}

		def sort_key(model_name: str) -> tuple[int, int, str]:
			model_path = os.path.join(models_dir, f"ggml-{model_name}.bin")
			is_current = model_name == current_model
			is_installed = Path(model_path).exists()
			priority = 0 if is_current else 1 if is_installed else 2
			return (priority, model_order.get(model_name, len(model_order)), model_name)

		return sorted(dict.fromkeys(models), key=sort_key)

	def _get_model_display(self, model_name: str) -> dict[str, str]:
		"""Build a UI-friendly description for a model variant."""
		base_name = self._get_base_model_name(model_name)
		base_meta = self.MODEL_METADATA.get(base_name, {
		    "size": "Taille variable",
		    "speed": "Variable",
		    "quality": "Variable",
		    "label": "Personnalisé",
		})

		tags = []
		if model_name.endswith(".en") or ".en-" in model_name:
			tags.append("Anglais uniquement")
		if model_name.endswith("-tdrz"):
			tags.append("TinyDiarize")

		quantization = self._get_quantization_suffix(model_name)
		if quantization:
			tags.append(f"Quantifié {quantization.upper()}")

		if base_meta.get("label"):
			tags.insert(0, base_meta["label"])

		return {
		    "size": base_meta["size"],
		    "speed": base_meta["speed"],
		    "quality": base_meta["quality"],
		    "tags": " • ".join(tags),
		}

	@staticmethod
	def _get_quantization_suffix(model_name: str) -> str | None:
		"""Extract quantization suffix like q5_0 or q8_0 when present."""
		match = re.search(r'-(q\d(?:_\d)?)$', model_name)
		return match.group(1) if match else None

	@staticmethod
	def _get_base_model_name(model_name: str) -> str:
		"""Reduce a variant name to its base family."""
		base_name = model_name
		quantization = SettingsWindow._get_quantization_suffix(base_name)
		if quantization:
			base_name = base_name[:-(len(quantization) + 1)]
		if base_name.endswith("-tdrz"):
			base_name = base_name[:-5]
		if base_name.endswith(".en"):
			base_name = base_name[:-3]
		return base_name

	def _select_model(self, model_name: str):
		"""Select a different Whisper model"""
		self.model_var.set(model_name)
		self._show_models_settings()  # Refresh display

	def _download_model(self, model_name: str):
		"""Download a Whisper model"""
		import subprocess
		import threading
		from tkinter import messagebox

		def download():
			whisper_path = os.path.expanduser(self.whisper_path_var.get())
			download_script = os.path.join(whisper_path, "models/download-ggml-model.sh")

			try:
				if not os.path.exists(download_script):
					self.window.after(
					    0, lambda: messagebox.showerror(
					        "Erreur", f"Script de téléchargement introuvable:\n{download_script}", parent=self.window))
					return

				result = subprocess.run(["bash", download_script, model_name],
				                        cwd=os.path.join(whisper_path, "models"),
				                        capture_output=True,
				                        text=True,
				                        timeout=600)

				if result.returncode == 0:
					self.window.after(
					    0, lambda: [
					        messagebox.showinfo("Téléchargement réussi",
					                            f"✓ Modèle {model_name} téléchargé avec succès !",
					                            parent=self.window),
					        self._show_models_settings()
					    ])
				else:
					self.window.after(
					    0, lambda: messagebox.showerror(
					        "Erreur", f"Échec du téléchargement:\n{result.stderr}", parent=self.window))
			except subprocess.TimeoutExpired:
				self.window.after(
				    0, lambda: messagebox.showerror("Erreur", "Timeout du téléchargement", parent=self.window))
			except Exception as e:
				self.window.after(0, lambda: messagebox.showerror("Erreur", f"Erreur: {e}", parent=self.window))

		# Show progress message
		messagebox.showinfo(
		    "Téléchargement",
		    f"📥 Téléchargement du modèle {model_name} en cours...\\nCela peut prendre plusieurs minutes.",
		    parent=self.window)

		# Download in background
		threading.Thread(target=download, daemon=True).start()

	def _uninstall_model(self, model_name: str):
		"""Uninstall a Whisper model"""
		from tkinter import messagebox
		import os

		if messagebox.askyesno("Désinstaller le modèle",
		                       f"Voulez-vous vraiment supprimer le modèle {model_name} ?\\n\\n"
		                       f"Cette action est irréversible.",
		                       parent=self.window):
			whisper_path = os.path.expanduser(self.whisper_path_var.get())
			model_path = os.path.join(whisper_path, f"models/ggml-{model_name}.bin")

			try:
				if os.path.exists(model_path):
					os.remove(model_path)
					messagebox.showinfo("Désinstallation réussie",
					                    f"✓ Modèle {model_name} désinstallé !",
					                    parent=self.window)
					# Clear and refresh models display
					for widget in self.content_frame.winfo_children():
						widget.destroy()
					self._show_models_settings()
				else:
					messagebox.showerror("Erreur", f"Modèle introuvable: {model_path}", parent=self.window)
			except Exception as e:
				messagebox.showerror("Erreur", f"Impossible de supprimer: {e}", parent=self.window)

	def _browse_whisper_path(self):
		"""Browse for whisper path"""
		from tkinter import filedialog
		import os

		path = filedialog.askdirectory(title="Sélectionner le répertoire whisper.cpp",
		                               initialdir=os.path.expanduser(self.whisper_path_var.get()))

		if path:
			self.whisper_path_var.set(path)

	def _create_category_title(self, title: str):
		"""Create category title"""
		frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
		frame.pack(fill="x", pady=(5, 20), padx=20)

		label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=22, weight="bold"), anchor="w")
		label.pack(fill="x")

		separator = ctk.CTkFrame(frame, height=2, fg_color=("gray70", "gray30"))
		separator.pack(fill="x", pady=(8, 0))

	def _create_option_menu(self, parent, label: str, variable, values: list):
		"""Create an option menu with label"""
		frame = ctk.CTkFrame(parent, fg_color="transparent")
		frame.pack(fill="x", pady=8, padx=20)

		lbl = ctk.CTkLabel(frame, text=label, anchor="w", width=280)
		lbl.pack(side="left", padx=(0, 20))

		menu = ctk.CTkComboBox(frame,
		                       variable=variable,
		                       values=values,
		                       width=220,
		                       height=36,
		                       corner_radius=8,
		                       state="readonly")
		menu.pack(side="right")

	def _create_slider(self, parent, label: str, variable, from_: float, to: float, is_int: bool = False):
		"""Create a slider with label and value display"""
		frame = ctk.CTkFrame(parent, fg_color="transparent")
		frame.pack(fill="x", pady=8, padx=20)

		lbl = ctk.CTkLabel(frame, text=label, anchor="w", width=280)
		lbl.pack(side="left", padx=(0, 20))

		value_label = ctk.CTkLabel(frame, text=str(variable.get()), width=50, font=ctk.CTkFont(size=14, weight="bold"))
		value_label.pack(side="right", padx=(10, 0))

		def on_change(value):
			if is_int:
				value_label.configure(text=str(int(float(value))))
			else:
				value_label.configure(text=f"{float(value):.2f}")

		slider = ctk.CTkSlider(frame, from_=from_, to=to, variable=variable, width=150, height=20, command=on_change)
		slider.pack(side="right")

	def _create_switch(self, parent, label: str, variable):
		"""Create a switch with label"""
		frame = ctk.CTkFrame(parent, fg_color="transparent")
		frame.pack(fill="x", pady=8, padx=20)

		lbl = ctk.CTkLabel(frame, text=label, anchor="w", width=280)
		lbl.pack(side="left", padx=(0, 20))

		switch = ctk.CTkSwitch(frame, text="", variable=variable, width=50, height=26)
		switch.pack(side="right")

	def _create_option_menu_with_help(self, parent, label: str, variable, values: list, help_text: str):
		"""Create an option menu with help tooltip"""
		frame = ctk.CTkFrame(parent, fg_color="transparent")
		frame.pack(fill="x", pady=8, padx=20)

		label_container = ctk.CTkFrame(frame, fg_color="transparent")
		label_container.pack(side="left", padx=(0, 20))

		lbl = ctk.CTkLabel(label_container, text=label, anchor="w")
		lbl.pack(side="left")

		help_btn = ctk.CTkButton(label_container,
		                         text="?",
		                         width=20,
		                         height=20,
		                         corner_radius=10,
		                         fg_color="transparent",
		                         border_width=1,
		                         font=ctk.CTkFont(size=11, weight="bold"),
		                         command=lambda: self._show_help(label, help_text))
		help_btn.pack(side="left", padx=(5, 0))

		menu = ctk.CTkOptionMenu(frame,
		                         variable=variable,
		                         values=values,
		                         width=220,
		                         height=36,
		                         corner_radius=8,
		                         anchor="center")
		menu.pack(side="right")

	def _create_slider_with_help(self,
	                             parent,
	                             label: str,
	                             variable,
	                             from_: float,
	                             to: float,
	                             is_int: bool = False,
	                             help_text: str = ""):
		"""Create a slider with help tooltip"""
		frame = ctk.CTkFrame(parent, fg_color="transparent")
		frame.pack(fill="x", pady=8, padx=20)

		label_container = ctk.CTkFrame(frame, fg_color="transparent")
		label_container.pack(side="left", padx=(0, 20))

		lbl = ctk.CTkLabel(label_container, text=label, anchor="w")
		lbl.pack(side="left")

		help_btn = ctk.CTkButton(label_container,
		                         text="?",
		                         width=20,
		                         height=20,
		                         corner_radius=10,
		                         fg_color="transparent",
		                         border_width=1,
		                         font=ctk.CTkFont(size=11, weight="bold"),
		                         command=lambda: self._show_help(label, help_text))
		help_btn.pack(side="left", padx=(5, 0))

		value_label = ctk.CTkLabel(frame, text=str(variable.get()), width=50, font=ctk.CTkFont(size=14, weight="bold"))
		value_label.pack(side="right", padx=(10, 0))

		def on_change(value):
			if is_int:
				value_label.configure(text=str(int(float(value))))
			else:
				value_label.configure(text=f"{float(value):.2f}")

		slider = ctk.CTkSlider(frame, from_=from_, to=to, variable=variable, width=150, height=20, command=on_change)
		slider.pack(side="right")

	def _create_switch_with_help(self, parent, label: str, variable, help_text: str):
		"""Create a switch with help tooltip"""
		frame = ctk.CTkFrame(parent, fg_color="transparent")
		frame.pack(fill="x", pady=8, padx=20)

		label_container = ctk.CTkFrame(frame, fg_color="transparent")
		label_container.pack(side="left", padx=(0, 20))

		lbl = ctk.CTkLabel(label_container, text=label, anchor="w")
		lbl.pack(side="left")

		help_btn = ctk.CTkButton(label_container,
		                         text="?",
		                         width=20,
		                         height=20,
		                         corner_radius=10,
		                         fg_color="transparent",
		                         border_width=1,
		                         font=ctk.CTkFont(size=11, weight="bold"),
		                         command=lambda: self._show_help(label, help_text))
		help_btn.pack(side="left", padx=(5, 0))

		switch = ctk.CTkSwitch(frame, text="", variable=variable, width=50, height=26)
		switch.pack(side="right")

	def _show_help(self, title: str, message: str):
		"""Show help dialog"""
		from tkinter import messagebox
		messagebox.showinfo(f"ℹ️ {title}", message, parent=self.window)

	def _apply_settings(self):
		"""Apply all settings with hot-reload"""
		old_config = {
		    "theme_mode": self.cfg.get("theme_mode"),
		    "font_size": self.cfg.get("font_size"),
		    "window_opacity": self.cfg.get("window_opacity"),
		    "history_size": self.cfg.get("history_size"),
		    "save_audio_files": self.cfg.get("save_audio_files"),
		}

		updates = {
		    "theme_mode": self.theme_var.get(),
		    "accent_color": self.accent_var.get(),
		    "window_opacity": self.opacity_var.get(),
		    "font_size": self.font_size_var.get(),
		    "animations_enabled": self.animations_var.get(),
		    "sample_rate": int(self.sample_rate_var.get()),
		    "noise_reduction": self.noise_reduction_var.get(),
		    "auto_gain": self.auto_gain_var.get(),
		    "whisper_model": self.model_var.get(),
		    "whisper_path": self.whisper_path_var.get(),
		    "language": self.language_var.get(),
		    "task": self.task_var.get(),
		    "beam_size": self.beam_size_var.get(),
		    "history_size": self.history_size_var.get(),
		    "history_search": self.history_search_var.get(),
		    "history_export_format": self.export_format_var.get(),
		    "notifications_enabled": self.notif_enabled_var.get(),
		    "notification_duration": self.notif_duration_var.get(),
		    "recording_mode": self.recording_mode_var.get(),
		    "auto_start": self.auto_start_var.get(),
		    "minimize_to_tray": self.minimize_tray_var.get(),
		    "log_level": self.log_level_var.get(),
		    "log_to_file": self.log_to_file_var.get(),
		    "save_audio_files": self.save_audio_var.get(),
		}

		if self.cfg.update(updates):
			# Apply theme immediately
			if old_config["theme_mode"] != self.theme_var.get():
				ctk.set_appearance_mode(self.theme_var.get())

			# Apply window opacity
			if old_config["window_opacity"] != self.opacity_var.get():
				self.history_window.window.attributes("-alpha", self.opacity_var.get())

			# Apply font size
			if old_config["font_size"] != self.font_size_var.get():
				new_font = ctk.CTkFont(size=self.font_size_var.get())
				self.history_window.text_widget.configure(font=new_font)

			# Apply history size
			if old_config["history_size"] != self.history_size_var.get():
				self.history_window.history_manager.set_max_size(self.history_size_var.get())

			# Apply save_audio_files changes (add/remove tab)
			if old_config["save_audio_files"] != self.save_audio_var.get():
				if self.save_audio_var.get():
					self.history_window.add_audio_tab()
				else:
					self.history_window.remove_audio_tab()

			# Update history window
			self.history_window.update_title()
			self.history_window.update_content()

			messagebox.showinfo("Paramètres", "✓ Paramètres appliqués avec succès !", parent=self.window)
			self.window.destroy()
		else:
			messagebox.showerror("Erreur", "Impossible de sauvegarder la configuration", parent=self.window)

	def _reset_settings(self):
		"""Reset to default settings"""
		if messagebox.askyesno("Réinitialiser",
		                       "Voulez-vous vraiment réinitialiser tous les paramètres par défaut ?",
		                       parent=self.window):
			self.cfg.reset()

			# Appliquer immédiatement les valeurs par défaut
			ctk.set_appearance_mode("dark")
			self.history_window.window.attributes("-alpha", 1.0)
			self.history_window.text_widget.configure(font=ctk.CTkFont(size=12))
			self.history_window.history_manager.set_max_size(10)
			self.history_window.update_title()
			self.history_window.update_content()

			messagebox.showinfo("Réinitialisation",
			                    "✓ Paramètres réinitialisés aux valeurs par défaut !",
			                    parent=self.window)
			self.window.destroy()
