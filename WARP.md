# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python PyQt6-based desktop application project consisting of **two main components**: 

1. **JAU's Startup Page**: Static HTML bookmark manager with organized link collections
2. **The Startup Dashboard Editor**: PyQt6 GUI application for visually editing the HTML startup page

**Development Environment**: Linux LMDE system used for all development, testing, and local execution.

## Architecture

### Core Application Architecture

**PyQt6 Desktop Application Layer**
- `src/main.py` - Main application entry point with git integration and window management
- `src/views/main_window.py` - Primary GUI with comprehensive menu system, toolbar, and event handling
- `src/views/card_editor.py` - Dialog for editing individual cards and their links

**Data Model Layer**
- `src/models/card_model.py` - Data structures representing cards, links, and dashboard organization
- Card hierarchy: Card → Main Links + Additional Link Sections → Individual Links

**Utility & Management Layer**
- `src/utils/html_parser.py` - BeautifulSoup4-based HTML file parsing and generation
- `src/utils/theme_manager.py` - 8 comprehensive UI themes (Default, Dark, Solarized, Monokai, etc.)
- `src/utils/settings_manager.py` - Persistent settings storage in `~/.startup-dashboard-editor/settings.json`

**HTML Output Layer**
- Masonry-style responsive layout generation (3/2/1 column responsive design)
- Preserves CSS styling and page structure
- Generates clean, browser-compatible HTML with embedded CSS

### Key Integrations

**Git Integration**
- Automatic commit date retrieval for application versioning
- Built-in "Git Commit & Push" functionality (Ctrl+G)
- Version tracking through git log integration

**File System Integration**  
- Persistent settings in user home directory (`~/.startup-dashboard-editor/`)
- Desktop integration with proper .desktop file and PNG icon
- Cross-platform file operations (Windows, macOS, Linux)

**Browser Integration**
- Direct browser opening with file:// URLs (Ctrl+B)
- HTML generation compatible with modern web browsers
- Responsive design that adapts to different screen sizes

## Essential Commands

### Development Setup

```bash
# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install PyQt6 dependencies
pip install -r qt_editor_requirements.txt

# Alternative dependencies (includes testing/build tools)
pip install -r requirements-editor.txt
```

### Running the Application

```bash
# Primary method - executable script
./startup_dashboard_editor.py

# Alternative - simple run script
./run

# Direct Python execution
python3 startup_dashboard_editor.py

# From source directory
python3 src/main.py
```

### Development Testing

```bash
# Test module imports and basic functionality
./test_dashboard_editor.py

# Verify PyQt6 installation
python3 -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"

# Check BeautifulSoup HTML parsing
python3 -c "from bs4 import BeautifulSoup; print('HTML parsing OK')"
```

### Git Workflow (Built-in)

```bash
# From within the application
# File → Git Commit & Push (Ctrl+G)

# Manual git operations
git add .
git commit -m "Update dashboard configuration"
git push
```

### Icon Management

```bash
# Convert icon format (utility script included)
python3 convert_icon.py

# Update desktop integration
cp startup-dashboard-editor.desktop ~/.local/share/applications/
```

## Key Features & Capabilities

### Card Management System
- **Create/Edit/Delete Cards**: Complete CRUD operations for dashboard sections
- **Drag-and-Drop Reordering**: Cards and links can be reordered via drag-and-drop
- **Link Organization**: Main links + multiple subsections per card
- **Real-time Preview**: Live preview of cards before saving

### Advanced UI Features
- **8 Built-in Themes**: Default, Dark, Solarized (Light/Dark), High Contrast, Monokai, Purple Night, Terminal Green
- **Comprehensive Zoom System**: Ctrl+Mouse Wheel, menu controls, persistent zoom levels
- **Keyboard Shortcuts**: Full keyboard navigation and shortcuts for power users
- **Responsive Scaling**: All UI elements scale with zoom level

### File Operations
- **Smart File Handling**: Remembers last opened file, auto-loads on startup
- **HTML Structure Preservation**: Maintains CSS and JavaScript when editing
- **Save/Save As**: Standard file operations with proper error handling

### Theme Management
- **Theme Persistence**: Selected theme saved between sessions
- **Live Theme Preview**: See themes before applying
- **Consistent Styling**: All UI elements properly themed across all themes

## Configuration Patterns

### Theme System
- **Theme Storage**: `~/.startup-dashboard-editor/settings.json`
- **Available Themes**: 8 predefined themes covering light/dark/specialized needs
- **Theme Application**: Real-time CSS generation and application

### Settings Management
```json
{
  "theme": "Dark",
  "zoom_level": 1.2,
  "last_file": "/path/to/startup.html",
  "window_geometry": "..."
}
```

### HTML Generation Patterns
- **Masonry Layout**: CSS Grid-based responsive design
- **Link Structure**: Organized hierarchy with proper semantic markup
- **Responsive Breakpoints**: 3 columns (desktop) → 2 columns (tablet) → 1 column (mobile)

## Key Files for Development

**Main Application Files**
- `startup_dashboard_editor.py` - Primary executable entry point
- `src/main.py` - Core application logic and window management
- `src/views/main_window.py` - Main GUI implementation (800+ lines)
- `src/views/card_editor.py` - Card editing dialog implementation

**Data & Configuration Files**
- `src/models/card_model.py` - Core data structures
- `src/utils/theme_manager.py` - Complete theme system implementation  
- `src/utils/settings_manager.py` - Settings persistence layer
- `src/utils/html_parser.py` - HTML file I/O operations

**Dependencies & Requirements**
- `qt_editor_requirements.txt` - Core runtime dependencies (PyQt6, BeautifulSoup4, lxml, PyYAML)
- `requirements-editor.txt` - Extended dependencies including testing tools (pytest, pyinstaller)

**Documentation & History**
- `CHANGELOG.md` - Complete version history and feature documentation
- `FINAL_SUMMARY.md` - Comprehensive project overview
- `README.md` - User-facing documentation and setup instructions

## Development Context

This is a **mature desktop application** with comprehensive GUI features, theme system, and professional user experience. The architecture follows **MVC patterns** with clear separation between data models, UI views, and utility functions.

**When making changes:**
- Test theme switching to ensure new components are properly styled
- Verify zoom functionality works with any new UI elements
- Check drag-and-drop operations still function correctly
- Test HTML generation preserves structure and styling
- Ensure keyboard shortcuts remain functional
- Verify cross-platform compatibility (Windows, macOS, Linux)

**Key Technical Decisions:**
- PyQt6 chosen for modern Qt6 support and cross-platform compatibility
- BeautifulSoup4 for robust HTML parsing without breaking existing structure  
- JSON-based settings for simple, human-readable configuration
- Embedded CSS generation for theme consistency
- Git integration for version tracking built into the application

The application represents a complete, production-ready desktop tool with sophisticated UI features, comprehensive theme support, and professional user experience design patterns.
