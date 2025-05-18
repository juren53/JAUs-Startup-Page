#!/usr/bin/env python3
"""
Startup Page Editor - A PyQt6 application for editing JAU's Startup Page.
This is the main entry point for running the application.
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import main

if __name__ == "__main__":
    main()

