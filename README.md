# JAUs-Startup-Page and Dashboard Editor

This repository contains two main components:

1. **JAU's Startup Page**: An HTML page that collects and organizes bookmarks into an HTML table.
2. **The Startup Dashboard Editor**: A PyQt6-based GUI editor for managing the Startup dashboard page.

## JAU's Startup Page

The original component - an HTML page that provides an organized collection of bookmarks in a table format.

## The Startup Dashboard Editor

A newer component that provides a GUI for editing the Startup Page without directly editing HTML code.

### Features

- Create, edit, and delete cards (sections) in the dashboard
- Manage links within each card
- Support for both main links and additional link sections
- Drag-and-drop reordering of cards and links
- Light and dark theme support with persistent settings
- Automatic loading of the last edited file on startup
- Masonry-style layout for efficient card arrangement without gaps
- Preview cards before saving
- Full HTML file editing with preservation of CSS and structure

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install CLI command (optional but recommended):
   ```bash
   chmod +x bin/startup_dashboard_editor
   ln -sf "$(pwd)/bin/startup_dashboard_editor" ~/.local/bin/startup_dashboard_editor
   ```
   
   Ensure `~/.local/bin` is in your PATH:
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

### Usage

#### CLI Command (Recommended)
Once installed, you can run the application from anywhere:

```bash
# Launch with default/last file
startup_dashboard_editor

# Open a specific file
startup_dashboard_editor Startup.html
startup_dashboard_editor --file ~/path/to/my-dashboard.html

# Show help and options
startup_dashboard_editor --help
startup_dashboard_editor --version

# Check for updates
startup_dashboard_editor --check-version
```

#### Direct Execution
Alternatively, run directly from the project directory:
```bash
./startup_dashboard_editor.py
```

#### Basic Operations

- **Open an existing HTML file**: File → Open
- **Save changes**: File → Save or Save As
- **Add a new card**: Click "Add Card" or Edit → Add Card
- **Edit a card**: Select card, then click "Edit Card"
- **Remove a card**: Select card, then click "Remove Card"
- **Toggle dark mode**: View → Toggle Dark Mode or use Ctrl+D
- **Reorder cards**: Drag and drop cards in the list to change their order
- **Reorder links**: When editing a card, drag and drop links to change their order

### Enhanced Features

#### Masonry Layout

The editor now generates HTML with a masonry-style layout that:
- Eliminates gaps between cards of different heights
- Provides a cleaner, more organized dashboard appearance
- Adapts responsively to different screen sizes

#### Persistent Settings

The application remembers:
- The last file you were editing
- Your theme preference (light/dark mode)

Settings are stored in `~/.startup-dashboard-editor/settings.json`

### Project Structure

```
src/
├── models/           # Data models
├── views/            # UI components
├── utils/            # Utility functions and classes
└── main.py           # Application entry point
```

### Dependencies

- PyQt6: Modern Qt6 bindings for Python
- BeautifulSoup4: HTML parsing library
- PyYAML: YAML file handling
- lxml: XML/HTML parser for BeautifulSoup

### Documentation

- **README.md**: General application documentation
- **ENHANCEMENTS.md**: Overview of drag-and-drop and other enhancements
- **MASONRY_LAYOUT_FIX.md**: Details on the improved card layout
- **REMEMBER_LAST_FILE.md**: Information about persistent settings

### Testing

To verify that the application can start correctly and that all modules are properly imported:

```bash
# Test module imports and functionality
./tools/test_dashboard_editor.py

# Test CLI command installation
startup_dashboard_editor --version

# Check for updates
startup_dashboard_editor --check-version
```

## Git Repository

This project is managed using Git version control. To work with the repository:

- Check out the [GIT_GUIDE.md](GIT_GUIDE.md) for basic Git usage instructions
- The repository includes:
  - Source code in the `src` directory
  - Documentation in Markdown files
  - Configuration files like `.gitignore` and licensing information

### Contributing

To contribute to the project:

1. Create a new branch for your feature or bug fix
2. Make your changes and commit them with clear, descriptive messages
3. Push your branch to the remote repository
4. Create a pull request for review

See the [GIT_GUIDE.md](GIT_GUIDE.md) file for detailed Git commands and best practices.

## License

Copyright © 2025
