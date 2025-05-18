#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("The Startup Dashboard Editor")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

