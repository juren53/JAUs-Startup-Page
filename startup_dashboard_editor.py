#!/usr/bin/env python3
"""
Startup Page Editor - A PyQt6 application for editing JAU's Startup Page.
This is the main entry point for running the application.

For version history and detailed changelog, see:
https://github.com/juren53/JAUs-Startup-Page/blob/main/CHANGELOG.md
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import main

if __name__ == "__main__":
    # Set the application icon explicitly here to ensure it's set before any windows appear
    # First try to use the PNG icon (preferred for Linux desktop integration)
    icon_path = os.path.join(os.path.dirname(__file__), "startup-dashboard-editor.png")
    if not os.path.exists(icon_path):
        # Fall back to JPG if PNG doesn't exist
        icon_path = os.path.join(os.path.dirname(__file__), "ICON_dashboard-editor.jpg")
    if os.path.exists(icon_path):
        # Create QApplication instance with icon
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(icon_path))
        main(app)
    else:
        # If icon doesn't exist, just run without setting icon
        main()

