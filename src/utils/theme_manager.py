#!/usr/bin/env python3
"""
Theme Manager for Startup Dashboard Editor
Manages application themes and styling
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDialogButtonBox
from PyQt6.QtCore import Qt


class ThemeManager:
    """Manages application themes and styling"""
    
    def __init__(self):
        self.themes = {
            'Default': {
                'name': 'Default',
                'background': '#ffffff',
                'text': '#000000',
                'selection_bg': '#3399ff',
                'selection_text': '#ffffff',
                'menubar_bg': '#f0f0f0',
                'menubar_text': '#000000',
                'toolbar_bg': '#f5f5f5',
                'statusbar_bg': '#e0e0e0',
                'statusbar_text': '#000000',
                'button_bg': '#e1e1e1',
                'button_text': '#000000',
                'button_hover': '#d4d4d4',
                'border': '#c0c0c0',
                'card_bg': '#f9f9f9',
                'card_border': '#dddddd'
            },
            'Dark': {
                'name': 'Dark',
                'background': '#2b2b2b',
                'text': '#ffffff',
                'selection_bg': '#4a9eff',
                'selection_text': '#ffffff',
                'menubar_bg': '#3c3c3c',
                'menubar_text': '#ffffff',
                'toolbar_bg': '#404040',
                'statusbar_bg': '#333333',
                'statusbar_text': '#ffffff',
                'button_bg': '#454545',
                'button_text': '#ffffff',
                'button_hover': '#555555',
                'border': '#555555',
                'card_bg': '#353535',
                'card_border': '#555555'
            },
            'Solarized Light': {
                'name': 'Solarized Light',
                'background': '#fdf6e3',
                'text': '#657b83',
                'selection_bg': '#268bd2',
                'selection_text': '#fdf6e3',
                'menubar_bg': '#eee8d5',
                'menubar_text': '#657b83',
                'toolbar_bg': '#f5f0e7',
                'statusbar_bg': '#eee8d5',
                'statusbar_text': '#657b83',
                'button_bg': '#eee8d5',
                'button_text': '#657b83',
                'button_hover': '#e8e2d4',
                'border': '#d3cbb7',
                'card_bg': '#faf5e6',
                'card_border': '#d3cbb7'
            },
            'Solarized Dark': {
                'name': 'Solarized Dark',
                'background': '#002b36',
                'text': '#839496',
                'selection_bg': '#268bd2',
                'selection_text': '#002b36',
                'menubar_bg': '#073642',
                'menubar_text': '#839496',
                'toolbar_bg': '#0a3c47',
                'statusbar_bg': '#073642',
                'statusbar_text': '#839496',
                'button_bg': '#073642',
                'button_text': '#839496',
                'button_hover': '#0c4956',
                'border': '#586e75',
                'card_bg': '#073642',
                'card_border': '#586e75'
            },
            'High Contrast': {
                'name': 'High Contrast',
                'background': '#000000',
                'text': '#ffffff',
                'selection_bg': '#ffff00',
                'selection_text': '#000000',
                'menubar_bg': '#000000',
                'menubar_text': '#ffffff',
                'toolbar_bg': '#000000',
                'statusbar_bg': '#000000',
                'statusbar_text': '#ffffff',
                'button_bg': '#333333',
                'button_text': '#ffffff',
                'button_hover': '#555555',
                'border': '#ffffff',
                'card_bg': '#1a1a1a',
                'card_border': '#ffffff'
            },
            'Monokai': {
                'name': 'Monokai',
                'background': '#272822',
                'text': '#f8f8f2',
                'selection_bg': '#49483e',
                'selection_text': '#f8f8f2',
                'menubar_bg': '#3e3d32',
                'menubar_text': '#f8f8f2',
                'toolbar_bg': '#414339',
                'statusbar_bg': '#3e3d32',
                'statusbar_text': '#f8f8f2',
                'button_bg': '#49483e',
                'button_text': '#f8f8f2',
                'button_hover': '#5a594d',
                'border': '#75715e',
                'card_bg': '#383833',
                'card_border': '#75715e'
            },
            'Purple Night': {
                'name': 'Purple Night',
                'background': '#1e1e2e',
                'text': '#cdd6f4',
                'selection_bg': '#7c3aed',
                'selection_text': '#ffffff',
                'menubar_bg': '#2a2a40',
                'menubar_text': '#cdd6f4',
                'toolbar_bg': '#313244',
                'statusbar_bg': '#2a2a40',
                'statusbar_text': '#cdd6f4',
                'button_bg': '#45475a',
                'button_text': '#cdd6f4',
                'button_hover': '#585b70',
                'border': '#6c7086',
                'card_bg': '#313244',
                'card_border': '#6c7086'
            },
            'Terminal Green': {
                'name': 'Terminal Green',
                'background': '#000000',
                'text': '#00ff00',
                'selection_bg': '#008000',
                'selection_text': '#000000',
                'menubar_bg': '#001100',
                'menubar_text': '#00ff00',
                'toolbar_bg': '#002200',
                'statusbar_bg': '#001100',
                'statusbar_text': '#00ff00',
                'button_bg': '#003300',
                'button_text': '#00ff00',
                'button_hover': '#004400',
                'border': '#008000',
                'card_bg': '#001a00',
                'card_border': '#008000'
            }
        }
        self.current_theme = 'Default'
    
    def get_theme_names(self):
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def get_theme(self, theme_name):
        """Get theme data by name"""
        return self.themes.get(theme_name, self.themes['Default'])
    
    def generate_stylesheet(self, theme_name):
        """Generate CSS stylesheet for the given theme"""
        theme = self.get_theme(theme_name)
        
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        
        /* Central Widget and Splitter */
        QWidget {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        
        QSplitter::handle {{
            background-color: {theme['border']};
            width: 2px;
        }}
        
        QSplitter::handle:hover {{
            background-color: {theme['selection_bg']};
        }}
        
        /* List Widget */
        QListWidget {{
            background-color: {theme['background']};
            color: {theme['text']};
            selection-background-color: {theme['selection_bg']};
            selection-color: {theme['selection_text']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
        }}
        
        QListWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {theme['border']};
        }}
        
        QListWidget::item:selected {{
            background-color: {theme['selection_bg']};
            color: {theme['selection_text']};
        }}
        
        QListWidget::item:hover {{
            background-color: {theme['button_hover']};
        }}
        
        /* Card Preview Widget */
        CardPreviewWidget {{
            background-color: {theme['card_bg']};
            border: 1px solid {theme['card_border']};
            border-radius: 8px;
            padding: 10px;
        }}
        
        /* Group Box */
        QGroupBox {{
            background-color: {theme['card_bg']};
            border: 2px solid {theme['card_border']};
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            background-color: {theme['card_bg']};
            color: {theme['text']};
        }}
        
        /* Scroll Area */
        QScrollArea {{
            background-color: {theme['background']};
            border: 1px solid {theme['border']};
        }}
        
        QScrollBar:vertical {{
            background-color: {theme['button_bg']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {theme['border']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {theme['selection_bg']};
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {theme['menubar_bg']};
            color: {theme['menubar_text']};
            border-bottom: 1px solid {theme['border']};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 8px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {theme['selection_bg']};
            color: {theme['selection_text']};
        }}
        
        QMenu {{
            background-color: {theme['menubar_bg']};
            color: {theme['menubar_text']};
            border: 1px solid {theme['border']};
        }}
        
        QMenu::item {{
            background-color: transparent;
            padding: 6px 12px;
        }}
        
        QMenu::item:selected {{
            background-color: {theme['selection_bg']};
            color: {theme['selection_text']};
        }}
        
        QMenu::separator {{
            height: 1px;
            background-color: {theme['border']};
            margin: 2px 0;
        }}
        
        /* Tool Bar */
        QToolBar {{
            background-color: {theme['toolbar_bg']};
            color: {theme['text']};
            border: 1px solid {theme['border']};
            spacing: 2px;
        }}
        
        QToolBar::separator {{
            background-color: {theme['border']};
            width: 1px;
            margin: 2px;
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {theme['statusbar_bg']};
            color: {theme['statusbar_text']};
            border-top: 1px solid {theme['border']};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {theme['button_bg']};
            color: {theme['button_text']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
            padding: 8px 16px;
            min-width: 80px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {theme['button_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {theme['selection_bg']};
            color: {theme['selection_text']};
        }}
        
        QPushButton:disabled {{
            background-color: {theme['border']};
            color: {theme['statusbar_text']};
        }}
        
        /* Combo Box */
        QComboBox {{
            background-color: {theme['button_bg']};
            color: {theme['button_text']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
            padding: 4px 8px;
            min-width: 100px;
        }}
        
        QComboBox:hover {{
            background-color: {theme['button_hover']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {theme['text']};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {theme['menubar_bg']};
            color: {theme['menubar_text']};
            selection-background-color: {theme['selection_bg']};
            selection-color: {theme['selection_text']};
            border: 1px solid {theme['border']};
        }}
        
        /* Labels */
        QLabel {{
            background-color: transparent;
            color: {theme['text']};
        }}
        
        /* Line Edit */
        QLineEdit {{
            background-color: {theme['background']};
            color: {theme['text']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
            padding: 4px;
            selection-background-color: {theme['selection_bg']};
            selection-color: {theme['selection_text']};
        }}
        
        /* Text Edit */
        QTextEdit, QPlainTextEdit {{
            background-color: {theme['background']};
            color: {theme['text']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
            selection-background-color: {theme['selection_bg']};
            selection-color: {theme['selection_text']};
        }}
        
        /* Dialog */
        QDialog {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        
        QDialogButtonBox QPushButton {{
            min-width: 70px;
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {theme['border']};
            background-color: {theme['background']};
        }}
        
        QTabBar::tab {{
            background-color: {theme['button_bg']};
            color: {theme['button_text']};
            border: 1px solid {theme['border']};
            padding: 8px 16px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {theme['selection_bg']};
            color: {theme['selection_text']};
        }}
        
        QTabBar::tab:hover {{
            background-color: {theme['button_hover']};
        }}
        """


class ThemeDialog(QDialog):
    """Dialog for selecting application theme"""
    
    def __init__(self, current_theme, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.selected_theme = current_theme
        
        self.setWindowTitle("Select Theme")
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout(self)
        
        # Theme selection
        layout.addWidget(QLabel("Choose a theme:"))
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.get_theme_names())
        self.theme_combo.setCurrentText(current_theme)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        layout.addWidget(self.theme_combo)
        
        # Preview label
        self.preview_label = QLabel("Preview: This is how text will look with the selected theme")
        self.preview_label.setStyleSheet("padding: 15px; border: 1px solid gray; min-height: 40px;")
        self.preview_label.setWordWrap(True)
        layout.addWidget(self.preview_label)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Set initial preview
        self.update_preview()
    
    def on_theme_changed(self, theme_name):
        """Handle theme selection change"""
        self.selected_theme = theme_name
        self.update_preview()
    
    def update_preview(self):
        """Update the preview with selected theme colors"""
        theme = self.theme_manager.get_theme(self.selected_theme)
        self.preview_label.setStyleSheet(f"""
            background-color: {theme['background']};
            color: {theme['text']};
            padding: 10px;
            border: 1px solid {theme['border']};
        """)
    
    def get_selected_theme(self):
        """Get the selected theme name"""
        return self.selected_theme

