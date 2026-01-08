#!/usr/bin/env python3
"""
Dictate PTT Copilot - Push-to-talk voice dictation with Whisper
Main entry point
"""

from app_config import AppConfig
from application import DictatePTTApplication


def main():
	"""Application entry point"""
	cfg = AppConfig()
	app = DictatePTTApplication(cfg)
	app.run()


if __name__ == "__main__":
	main()
