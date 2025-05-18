# Project Renamed to "The Startup Dashboard Editor"

I've made the following changes to rename the project and improve the UI layout:

## Changes Made

### 1. Project Renaming

- **Changed application name** from "JAU's Startup Page Editor" to "The Startup Dashboard Editor"
- **Updated window titles** in all relevant UI components
- **Changed settings directory** from ".jau-startup-editor" to ".startup-dashboard-editor"
- **Updated documentation** including README.md and dialog titles

### 2. UI Improvements

- **Fixed Main Links list positioning** in the card editor dialog:
  - The list now starts from the top of the dialog instead of the middle
  - Added more prominent styling to the "Main Links" label
  - Increased the minimum height of the list for better visibility

## How to Test the Changes

1. **Run the application**:
   ```bash
   ./startup_dashboard_editor.py
   ```

2. **Verify the application name**:
   - The window title should now show "The Startup Dashboard Editor"
   - The About dialog (Help → About) should show the new name

3. **Test the Main Links list positioning**:
   - Create a new card or edit an existing one
   - In the edit dialog, the "Main Links" list should start from the top
   - The list should have a larger height, making it more prominent

4. **Verify settings persistence**:
   - Make some changes (add a card, toggle dark mode, etc.)
   - Close and reopen the application
   - Your changes should persist
   - Settings are now stored in `~/.startup-dashboard-editor/settings.json`

## Summary of Files Changed

1. **src/views/main_window.py**:
   - Updated window title
   - Updated the About dialog content

2. **src/views/card_editor.py**:
   - Improved styling of the "Main Links" label
   - Repositioned the link list to start from the top
   - Increased minimum height of the list

3. **src/main.py**:
   - Updated application name

4. **src/utils/settings_manager.py**:
   - Changed settings directory path

5. **README.md**:
   - Updated all instances of the project name

These changes maintain all the functionality of the application while providing a more generic name and improved UI layout.

