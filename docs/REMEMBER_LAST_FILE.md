# JAU's Startup Page Editor - Remember Last File

I've added a new feature to the editor that remembers the last edited file and automatically opens it on startup.

## Features Added

1. **Remember Last File**: The application now remembers the last file you were working on and automatically loads it when you start the editor.

2. **Persistent Dark Mode Setting**: Your theme preference (light/dark mode) is now remembered between sessions.

3. **Settings Storage**: All settings are stored in a JSON file in your home directory at `~/.jau-startup-editor/settings.json`.

## How It Works

### Technical Implementation

1. **Settings Manager**: A new `SettingsManager` class has been added in `src/utils/settings_manager.py` to handle persistent settings:
   ```python
   class SettingsManager:
       def __init__(self):
           # Create settings directory if it doesn't exist
           self.settings_dir = Path.home() / ".jau-startup-editor"
           self.settings_file = self.settings_dir / "settings.json"
           
           self.settings = {
               "last_file": None,  # Path to the last opened file
               "window_size": [1000, 700],  # Default window size
               "dark_mode": False  # Default theme
           }
   ```

2. **Auto-Loading Last File**: When the editor starts, it automatically checks for and loads the last opened file:
   ```python
   # In MainWindow.__init__:
   # Load last file if available
   last_file = self.settings_manager.get_last_file()
   if last_file and os.path.exists(last_file):
       self.open_file(last_file)
   ```

3. **Saving File Path on Open/Save**: Whenever you open or save a file, the path is stored in settings:
   ```python
   # When opening a file:
   self.settings_manager.set_last_file(file_path)
   
   # When saving a file:
   self.settings_manager.set_last_file(self.current_file)
   ```

4. **Persistent Theme Settings**: Your choice of dark or light theme is now saved:
   ```python
   # When toggling theme:
   self.settings_manager.set_setting("dark_mode", self.dark_mode)
   ```

## Testing the New Feature

1. **Run the application**:
   ```bash
   ./startup_dashboard_editor.py
   ```

2. **Open a file**: Use File → Open to open your Startup.html file

3. **Make some changes**: Add, edit, or reorder cards and links

4. **Save the file**: Use File → Save or File → Save As

5. **Close the application**: Use File → Exit or close the window

6. **Restart the application**:
   ```bash
   ./startup_dashboard_editor.py
   ```

7. **Verify auto-loading**: The file you were working on should automatically open

8. **Verify theme persistence**: If you switched to dark mode, it should still be in dark mode

## Benefits

- **Improved Workflow**: No need to navigate to your file each time you start the editor
- **Time Saving**: Immediately continue where you left off
- **Preference Retention**: Your UI preferences persist between sessions

## Technical Details

The settings are stored in a JSON file at `~/.jau-startup-editor/settings.json`. If you want to reset all settings, you can simply delete this file:

```bash
rm -rf ~/.jau-startup-editor
```

This feature is completely transparent and requires no user interaction - it just works automatically in the background to improve your editing experience.

