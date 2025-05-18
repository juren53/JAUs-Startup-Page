# The Startup Dashboard Editor

A PyQt6-based GUI editor for managing the Startup dashboard page.

## Features

- Create, edit, and delete cards (sections) in the dashboard
- Manage links within each card
- Support for both main links and additional link sections
- Drag-and-drop reordering of cards and links
- Light and dark theme support with persistent settings
- Automatic loading of the last edited file on startup
- Masonry-style layout for efficient card arrangement without gaps
- Preview cards before saving
- Full HTML file editing with preservation of CSS and structure

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r qt_editor_requirements.txt
   ```

## Usage

Run the application:
```bash
./startup_dashboard_editor.py
```

### Basic Operations

- **Open an existing HTML file**: File → Open
- **Save changes**: File → Save or Save As
- **Add a new card**: Click "Add Card" or Edit → Add Card
- **Edit a card**: Select card, then click "Edit Card"
- **Remove a card**: Select card, then click "Remove Card"
- **Toggle dark mode**: View → Toggle Dark Mode or use Ctrl+D
- **Reorder cards**: Drag and drop cards in the list to change their order
- **Reorder links**: When editing a card, drag and drop links to change their order

## Enhanced Features

### Masonry Layout

The editor now generates HTML with a masonry-style layout that:
- Eliminates gaps between cards of different heights
- Provides a cleaner, more organized dashboard appearance
- Adapts responsively to different screen sizes

### Persistent Settings

The application remembers:
- The last file you were editing
- Your theme preference (light/dark mode)

Settings are stored in `~/.startup-dashboard-editor/settings.json`

## Project Structure

```
src/
├── models/           # Data models
├── views/            # UI components
├── utils/            # Utility functions and classes
└── main.py           # Application entry point
```

## Dependencies

- PyQt6: Modern Qt6 bindings for Python
- BeautifulSoup4: HTML parsing library
- PyYAML: YAML file handling
- lxml: XML/HTML parser for BeautifulSoup

## Documentation

- **README.md**: General application documentation
- **ENHANCEMENTS.md**: Overview of drag-and-drop and other enhancements
- **MASONRY_LAYOUT_FIX.md**: Details on the improved card layout
- **REMEMBER_LAST_FILE.md**: Information about persistent settings

## Testing

To verify that the application can start correctly and that all modules are properly imported, run:

```bash
./test_dashboard_editor.py
```

## License

Copyright © 2025

