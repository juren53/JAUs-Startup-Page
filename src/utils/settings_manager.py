import json
import os
from pathlib import Path

class SettingsManager:
    """Manages application settings, including the last opened file."""
    
    def __init__(self):
        # Create settings directory if it doesn't exist
        self.settings_dir = Path.home() / ".startup-dashboard-editor"
        self.settings_file = self.settings_dir / "settings.json"
        
        self.settings = {
            "last_file": None,  # Path to the last opened file
            "window_size": [1000, 700],  # Default window size
            "dark_mode": False,  # Default theme
            "zoom_level": 1.0  # Default zoom level (100%)
        }
        
        # Create directory if it doesn't exist
        if not self.settings_dir.exists():
            self.settings_dir.mkdir(parents=True, exist_ok=True)
        
        # Load settings if the file exists
        self.load_settings()
    
    def load_settings(self):
        """Load settings from the settings file."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to the settings file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get_setting(self, key, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        """Set a setting value and save to file."""
        self.settings[key] = value
        self.save_settings()
    
    def get_last_file(self):
        """Get the path to the last opened file."""
        return self.settings.get("last_file")
    
    def set_last_file(self, file_path):
        """Set the path to the last opened file and save settings."""
        self.settings["last_file"] = file_path
        self.save_settings()

