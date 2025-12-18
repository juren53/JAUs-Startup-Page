# JAUs-Startup-Page and Dashboard Editor

This repository contains two main components:

1. **JAU's Startup Page**: An HTML page that collects and organizes bookmarks into an HTML table.
2. **The Startup Dashboard Editor**: A PyQt6-based GUI editor for managing the Startup dashboard page.

## JAU's Startup Page

The original component - an HTML page that provides an organized collection of bookmarks in a table format.

## The Startup Dashboard Editor

A newer component that provides a GUI for editing the Startup Page without directly editing HTML code.

### Features

#### Core Dashboard Management
- **Card Management**: Create, edit, and delete cards (sections) in the dashboard
- **Link Organization**: Manage links within each card with main and additional sections
- **Drag-and-Drop**: Intuitive reordering of cards and links
- **Live Preview**: Real-time preview of cards before saving changes
- **File Operations**: Full HTML file editing with CSS and structure preservation

#### Advanced UI Features
- **8 Professional Themes**: 
  - Default (clean light theme)
  - Dark (modern dark theme)
  - Solarized Light/Dark (eye-friendly color schemes)
  - High Contrast (accessibility focused)
  - Monokai (popular editor theme)
  - Purple Night (modern purple dark mode)
  - Terminal Green (retro terminal style)
- **Theme Persistence**: Selected theme automatically saved and restored
- **Masonry Layout**: Efficient card arrangement without gaps
- **Zoom System**: Application-wide zoom with Ctrl+Mouse Wheel
- **Responsive Design**: Adapts to different screen sizes

#### User Experience
- **Persistent Settings**: Remembers last file and preferences
- **Keyboard Shortcuts**: Power-user shortcuts for common operations
- **Status Bar**: Helpful messages and zoom indicators
- **Professional Interface**: Modern, polished UI with intuitive controls

### Installation

#### Prerequisites
- **Python 3.10 or higher** (recommended: 3.12+)
- **Git** (for cloning the repository)

#### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/juren53/JAUs-Startup-Page.git
   cd JAUs-Startup-Page
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or using the new pyproject.toml:
   ```bash
   pip install -e .
   ```

4. **Install CLI command (optional but recommended):**
   ```bash
   chmod +x bin/startup_dashboard_editor
   ln -sf "$(pwd)/bin/startup_dashboard_editor" ~/.local/bin/startup_dashboard_editor
   ```
    
    Ensure `~/.local/bin` is in your PATH:
    ```bash
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
   ```

#### Development Setup

For development with additional tools:
```bash
pip install -e ".[dev]"
```

This includes:
- **pytest** for testing
- **black** for code formatting
- **isort** for import sorting
- **mypy** for type checking

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

- **Open an existing HTML file**: File → Open or `Ctrl+O`
- **Save changes**: File → Save or `Ctrl+S`
- **Save As**: File → Save As or `Ctrl+Shift+S`
- **Add a new card**: Click "Add Card" or Edit → Add Card
- **Edit a card**: Select card, then click "Edit Card"
- **Remove a card**: Select card, then click "Remove Card"
- **Change theme**: View → Change Theme... or `Ctrl+T`
- **Quick theme toggle**: Toolbar button for Default/Dark switching
- **Zoom controls**: View → Zoom In/Out/Reset or `Ctrl++/-/0`
- **Application zoom**: `Ctrl+Mouse Wheel`
- **Reorder cards**: Drag and drop cards in the list to change their order
- **Reorder links**: When editing a card, drag and drop links to change their order
- **Exit application**: File → Exit or `Ctrl+Q`

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

## Troubleshooting

### Common Issues

#### Application Won't Start
- **Python Version**: Ensure you're using Python 3.10 or higher
- **Dependencies**: Run `pip install -r requirements.txt` to ensure all dependencies are installed
- **Virtual Environment**: Make sure your virtual environment is activated

#### Theme Not Applied
- **Settings File**: Check `~/.startup-dashboard-editor/settings.json` exists and is writable
- **Permissions**: Ensure the application has permission to write to your home directory

#### File Not Found Errors
- **Path**: Verify the HTML file path is correct
- **Permissions**: Ensure the file is readable and writable
- **Format**: Make sure the file is a valid HTML file generated by the editor

#### CLI Command Not Found
- **Installation**: Verify the CLI script was installed correctly
- **PATH**: Check that `~/.local/bin` is in your PATH
- **Permissions**: Ensure the script is executable: `chmod +x bin/startup_dashboard_editor`

#### Performance Issues
- **Large Files**: For very large HTML files, the editor may slow down
- **Memory**: Ensure sufficient system memory is available
- **Restart**: Try restarting the application

### Getting Help

- **GitHub Issues**: Report bugs at https://github.com/juren53/JAUs-Startup-Page/issues
- **Documentation**: Check the `docs/` directory for detailed guides
- **Testing**: Run `./tools/test_dashboard_editor.py` to verify installation

## License

Copyright © 2025
