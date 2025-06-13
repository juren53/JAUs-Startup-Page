# Changelog

All notable changes to the JAU's Startup Page Editor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional theme customization options
- Export functionality for sharing card configurations
- Enhanced card templates and presets
- Bulk card operations (import/export)

## [1.1.0] - 2025-06-13

### Added
- **Comprehensive UI Theme System** with 8 beautiful themes:
  - Default (clean light theme)
  - Dark (modern dark theme for reduced eye strain)
  - Solarized Light (warm, easy-on-the-eyes light theme)
  - Solarized Dark (popular dark theme with excellent contrast)
  - High Contrast (black background with bright text for accessibility)
  - Monokai (popular editor theme with rich colors)
  - Purple Night (modern purple-themed dark mode)
  - Terminal Green (retro green-on-black terminal style)
- **ThemeDialog** with real-time preview for easy theme selection
- **Theme persistence** - selected theme is saved and restored between sessions
- **Enhanced About dialog** with features list and keyboard shortcuts
- **Keyboard shortcuts** for theme management:
  - `Ctrl+T` - Open theme selection dialog
  - Toolbar toggle button for quick Default/Dark switching

### Changed
- **View Menu Enhancement** - Added "Change Theme..." option with keyboard shortcut
- **Toolbar Addition** - Added quick theme toggle button for convenient switching
- **Window title updates** - Shows current theme name when not using Default theme
- **Improved user experience** with organized theme management

### Enhanced
- **Comprehensive CSS styling** - All UI elements consistently themed across all themes
- **Professional appearance** - Modern, polished interface with multiple style options
- **Accessibility improvements** - High contrast theme for better accessibility
- **User customization** - Multiple theme options to suit different preferences and environments
- **Settings integration** - Theme preferences saved and restored automatically

### Technical
- Added `ThemeManager` class for centralized theme management
- Implemented comprehensive CSS stylesheet generation system
- Added `ThemeDialog` class with live preview functionality
- Enhanced settings system to include theme preferences
- Added comprehensive styling for all PyQt6 widgets including:
  - Main window and dialogs
  - List widgets and buttons
  - Scroll areas and group boxes
  - Menu bars and toolbars
  - Card preview widgets
  - Status bars and labels
- Improved code organization with modular theme management

## [1.0.0] - 2025-06-12

### Added
- Initial release of JAU's Startup Dashboard Editor
- **PyQt6-based modern interface** for managing startup page cards
- **Card Management System** with full CRUD operations:
  - Add new cards with custom titles
  - Edit existing cards with comprehensive link management
  - Remove cards with confirmation dialogs
  - Drag-and-drop reordering of cards
- **Link Management** within cards:
  - Main links section
  - Multiple subsections for organized link grouping
  - Custom link names and URLs
  - Font size and color customization for individual links
- **Real-time Preview System**:
  - Live preview of selected cards
  - Styled link display with hover effects
  - Zoom support with Ctrl+Mouse Wheel
  - Responsive scaling of all preview elements
- **File Operations**:
  - Open existing HTML startup page files
  - Save changes to current file
  - Save As functionality for creating new files
  - Last file memory for convenience
- **Advanced Zoom System**:
  - Application-wide zoom with Ctrl+Mouse Wheel
  - Zoom controls in View menu and toolbar
  - Zoom indicator in status bar
  - Zoom persistence between sessions
  - Scalable UI components that resize with zoom level
- **Professional UI Features**:
  - Resizable split-pane layout
  - Comprehensive menu system
  - Intuitive toolbar with common actions
  - Status bar with helpful messages
  - Keyboard shortcuts for common operations
- **Settings Management**:
  - Persistent zoom level settings
  - Last opened file tracking
  - Application preferences storage

### Technical Features
- **Modular Architecture** with clear separation of concerns:
  - Model-View separation for card data management
  - Dedicated HTML parser for file I/O operations
  - Settings manager for persistent configuration
  - Theme manager for UI customization
- **Robust Error Handling** with user-friendly error messages
- **Cross-platform Compatibility** (Linux, Windows, macOS)
- **Git Integration** for version tracking and commit date display
- **Professional Packaging** with proper Python project structure

### User Experience
- **Intuitive Interface** designed for ease of use
- **Visual Feedback** with status messages and confirmations
- **Keyboard Shortcuts** for power users:
  - `Ctrl+O` - Open file
  - `Ctrl+S` - Save file
  - `Ctrl+Shift+S` - Save As
  - `Ctrl+Q` - Exit application
  - `Ctrl++/-` - Zoom In/Out
  - `Ctrl+0` - Reset Zoom
  - `Ctrl+T` - Change Theme
- **Help System** with About dialog and project documentation links
- **Smart Defaults** for new users while maintaining flexibility for advanced users

## [0.1.0] - 2025-06-11

### Added
- Initial project structure and development setup
- Basic card data model implementation
- HTML parser foundation for file operations
- Core PyQt6 application framework

---

## Version History Summary

- **v1.1.0**: Added comprehensive UI theme system with 8 themes, theme persistence, and enhanced user experience
- **v1.0.0**: Full-featured startup page editor with card management, zoom system, and professional UI
- **v0.1.0**: Initial development version with basic framework

## Future Roadmap

### Planned Features
- **Enhanced Card Templates** - Pre-defined card layouts and styles
- **Export/Import Functionality** - Share card configurations between users
- **Advanced Theme Customization** - User-created custom themes
- **Bulk Operations** - Import multiple cards from CSV/JSON
- **Enhanced Link Management** - Favicon fetching, link validation
- **Search and Filter** - Find cards and links quickly
- **Backup and Restore** - Automatic backups of startup page configurations

### Potential Enhancements
- **Plugin System** for custom card types and integrations
- **Cloud Sync** for sharing configurations across devices
- **Advanced Styling** - Custom CSS injection for cards
- **Performance Optimization** for handling large numbers of cards
- **Accessibility Improvements** - Enhanced screen reader support
- **Internationalization** - Multi-language support
- **Advanced Preview** - WYSIWYG editing with live HTML preview
- **Integration Features** - Browser bookmark import, RSS feed integration

