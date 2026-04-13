PROJECT_DIR  := $(shell pwd)
VENV         := $(PROJECT_DIR)/venv
PYTHON       := $(VENV)/bin/python
PIP          := $(VENV)/bin/pip
ENTRY        := $(PROJECT_DIR)/dictate_ptt_copilot.py
SERVICE_NAME := dictate-ptt.service
SERVICE_DIR  := $(HOME)/.config/systemd/user
SERVICE_FILE := $(SERVICE_DIR)/$(SERVICE_NAME)

.PHONY: help install run compile service enable disable start stop restart status logs logs-follow clean

# ── Aide ───────────────────────────────────────────────────

help: ## Afficher cette aide
	@echo ""
	@echo "  \033[1mDéveloppement\033[0m"
	@grep -E '^(install|run|compile):.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  \033[1mService systemd\033[0m"
	@grep -E '^(service|enable|disable|start|stop|restart|status|logs|logs-follow):.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  \033[1mMaintenance\033[0m"
	@grep -E '^(clean):.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ── Développement ──────────────────────────────────────────

install: ## Créer le venv (si besoin) et installer les dépendances
	@test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install sounddevice soundfile numpy evdev customtkinter
	@echo "✅ Dépendances installées"

run: ## Lancer le programme en avant-plan (hors service)
	$(PYTHON) $(ENTRY)

compile: ## Vérifier la syntaxe de tous les .py
	@find $(PROJECT_DIR) -name '*.py' ! -path '*/venv/*' ! -path '*/__pycache__/*' \
		-exec $(PYTHON) -m py_compile {} + && echo "✅ Compilation OK"

# ── Service systemd ────────────────────────────────────────

define SERVICE_UNIT
[Unit]
Description=Copilot Push-to-Talk Dictation (whisper.cpp)
After=graphical-session.target pipewire.service wireplumber.service
Wants=pipewire.service wireplumber.service

[Service]
Type=simple
ExecStart=$(PYTHON) $(ENTRY)
WorkingDirectory=$(PROJECT_DIR)
Restart=on-failure
RestartSec=1
StandardOutput=journal
StandardError=journal
Environment=XDG_RUNTIME_DIR=%t
PassEnvironment=DISPLAY WAYLAND_DISPLAY XDG_RUNTIME_DIR XAUTHORITY DBUS_SESSION_BUS_ADDRESS

[Install]
WantedBy=graphical-session.target
endef

export SERVICE_UNIT
service: ## Créer / mettre à jour le fichier service systemd
	@mkdir -p $(SERVICE_DIR)
	@echo "$$SERVICE_UNIT" > $(SERVICE_FILE)
	systemctl --user daemon-reload
	@echo "✅ $(SERVICE_NAME) installé et daemon rechargé"

enable: service start## Activer le service au démarrage
	systemctl --user enable $(SERVICE_NAME)
	@echo "✅ $(SERVICE_NAME) activé au démarrage"

disable: ## Désactiver le service au démarrage
	systemctl --user disable $(SERVICE_NAME)
	@echo "✅ $(SERVICE_NAME) désactivé au démarrage"

start: ## Démarrer le service
	systemctl --user import-environment DISPLAY WAYLAND_DISPLAY XDG_RUNTIME_DIR XAUTHORITY DBUS_SESSION_BUS_ADDRESS || true
	systemctl --user start $(SERVICE_NAME)

stop: ## Arrêter le service
	systemctl --user stop $(SERVICE_NAME)

restart: ## Redémarrer le service
	systemctl --user import-environment DISPLAY WAYLAND_DISPLAY XDG_RUNTIME_DIR XAUTHORITY DBUS_SESSION_BUS_ADDRESS || true
	systemctl --user daemon-reload
	systemctl --user restart $(SERVICE_NAME)

status: ## Afficher le statut du service
	systemctl --user status $(SERVICE_NAME)

logs: ## Afficher les derniers logs (50 lignes)
	journalctl --user -u $(SERVICE_NAME) -n 50 --no-pager

logs-follow: ## Suivre les logs en temps réel
	journalctl --user -u $(SERVICE_NAME) -f

# ── Maintenance ────────────────────────────────────────────

clean: ## Supprimer les fichiers temporaires et __pycache__
	find $(PROJECT_DIR) -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	rm -f /tmp/dictate_ptt_*.wav
	@echo "✅ Nettoyage terminé"
