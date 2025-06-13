#!/usr/bin/env python3
"""
JAU's Startup Page Editor - Main application module

For version history and detailed changelog, see:
https://github.com/juren53/JAUs-Startup-Page/blob/main/CHANGELOG.md
"""
import sys
import os
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from src.views.main_window import MainWindow

def get_last_commit_date():
    """Get the date of the last commit from Git."""
    try:
        # Get the timestamp of the last commit
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%at'],
            capture_output=True, text=True, check=True
        )
        timestamp = int(result.stdout.strip())
        # Convert to datetime and format it
        commit_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        return commit_date
    except (subprocess.SubprocessError, ValueError):
        # If there's any error (e.g., not a git repo), return current date
        return datetime.now().strftime('%Y-%m-%d')

def main(existing_app=None):
    # Use existing app if provided, otherwise create a new one
    if existing_app:
        app = existing_app
    else:
        app = QApplication(sys.argv)
        app.setApplicationName("The Startup Dashboard Editor")
        
        # Set application style
        app.setStyle("Fusion")
        
        # Set application icon
        # First try to use PNG icon (preferred for Linux desktop integration)
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               "startup-dashboard-editor.png")
        if not os.path.exists(icon_path):
            # Fall back to JPG if PNG doesn't exist
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                   "ICON_dashboard-editor.jpg")
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            app.setWindowIcon(app_icon)
    
    # Get the last commit date
    last_commit_date = get_last_commit_date()
    
    # Create and show the main window
    window = MainWindow(last_commit_date=last_commit_date)
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

