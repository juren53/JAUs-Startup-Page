#!/usr/bin/env python3
"""
Test script to verify all modules are properly imported and the application can start.
"""
import sys
import os
from pathlib import Path

print("Testing The Startup Dashboard Editor imports...")

# Add parent directory to path so we can import src
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

try:
    # Import main modules
    from src.main import main
    from src.models.card_model import Card, Link, StartupPageModel
    from src.utils.html_parser import HtmlParser
    from src.views.card_editor import CardEditorDialog, LinkEditorDialog
    from src.views.main_window import MainWindow, CardPreviewWidget
    
    print("✅ All modules imported successfully!")
    
    # Get the path to Startup.html (now in parent directory)
    startup_html_path = Path(__file__).parent.parent / 'Startup.html'
    
    if startup_html_path.exists():
        print(f"✅ Found Startup.html file at: {startup_html_path}")
        print("Testing HTML parsing...")
        try:
            model = HtmlParser.load_from_file(str(startup_html_path))
            print(f"✅ Successfully parsed HTML file. Found {len(model.cards)} cards.")
            for i, card in enumerate(model.cards):
                print(f"  Card {i+1}: {card.title} - {len(card.links)} links")
        except Exception as e:
            print(f"❌ Error parsing HTML file: {e}")
    else:
        print(f"❌ Startup.html file not found at: {startup_html_path}")
    
    print("\nTest script completed. Now you can run the main application:")
    print("./startup_dashboard_editor.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please check your project structure and imports.")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

