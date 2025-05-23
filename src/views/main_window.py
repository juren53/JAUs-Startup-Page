import os
import sys
import subprocess
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QListWidgetItem, QTabWidget,
    QMessageBox, QFileDialog, QSplitter, QGroupBox, QScrollArea,
    QStatusBar, QToolBar, QApplication, QDialog, QAbstractItemView
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QColor, QPalette, QTransform, QWheelEvent

from src.utils.html_parser import HtmlParser
from src.utils.settings_manager import SettingsManager
from src.views.card_editor import CardEditorDialog
from src.models.card_model import Card, StartupPageModel


class CardPreviewWidget(QWidget):
    """Widget for displaying a preview of a card."""
    
    # Signal to notify when zoom level changes
    zoomChanged = pyqtSignal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.card = None
        self._scale_factor = 1.0
        self.initUI()
    
    def initUI(self):
        """Initialize the user interface."""
        self.layout = QVBoxLayout(self)
        
        self.titleLabel = QLabel("No card selected")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        
        self.linksContainer = QWidget()
        self.linksLayout = QVBoxLayout(self.linksContainer)
        
        # Create a scroll area for links
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(self.linksContainer)
        
        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(scrollArea)
        
        # Apply some basic styling
        self.setStyleSheet("""
            QLabel { padding: 8px; }
            QGroupBox { border: 1px solid #ccc; border-radius: 4px; margin-top: 1ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }
        """)
    
    @property
    def scale_factor(self):
        """Get the current scale factor."""
        return self._scale_factor
        
    @scale_factor.setter
    def scale_factor(self, value):
        """Set the scale factor and apply scaling."""
        # Ensure scale factor is within reasonable limits
        self._scale_factor = max(0.5, min(3.0, value))
        self.applyScaling()
        # Emit signal to notify of zoom change
        self.zoomChanged.emit(self._scale_factor)
    
    def applyScaling(self):
        """Apply the current scale factor to the widget contents."""
        # Apply scaling to the linksContainer
        self.linksContainer.setStyleSheet(f"""
            font-size: {100 * self._scale_factor}%;
            QGroupBox {{
                font-size: {12 * self._scale_factor}px;
                font-weight: bold;
                padding: {5 * self._scale_factor}px;
                margin-top: {10 * self._scale_factor}px;
            }}
            QGroupBox::title {{
                font-size: {12 * self._scale_factor}px;
            }}
            QLabel {{
                padding: {4 * self._scale_factor}px;
            }}
        """)
        
        # Adjust the title label separately as it's not in the linksContainer
        self.titleLabel.setStyleSheet(f"font-size: {16 * self._scale_factor}px; font-weight: bold; padding: 10px;")
        
        # If a card is loaded, update the links to reflect the new scale factor
        if self.card:
            self.setCard(self.card, update_for_zoom=True)
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel events for zooming when Ctrl is pressed."""
        # Check if Ctrl key is pressed
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Calculate zoom delta (typical step is 0.1 or 10%)
            delta = event.angleDelta().y()
            zoom_delta = 0.1 if delta > 0 else -0.1
            
            # Update scale factor
            self.scale_factor = self._scale_factor + zoom_delta
            
            # Accept the event to prevent it from being propagated
            event.accept()
        else:
            # If Ctrl is not pressed, let the default behavior handle the event
            super().wheelEvent(event)
    
    def setCard(self, card, update_for_zoom=False):
        """Update the preview with the specified card."""
        self.card = card
        
        # If we're just updating for zoom changes and already have a card, don't clear
        # This helps prevent flickering during zoom operations
        if not update_for_zoom:
            # Clear the current layout
            while self.linksLayout.count():
                child = self.linksLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        else:
            # For zoom updates, remove widgets but keep a reference to rebuild them
            widgets_to_remove = []
            for i in range(self.linksLayout.count()):
                widgets_to_remove.append(self.linksLayout.itemAt(i).widget())
            
            for widget in widgets_to_remove:
                if widget:
                    widget.deleteLater()
        
        if not card:
            self.titleLabel.setText("No card selected")
            return
        
        self.titleLabel.setText(f"{card.title}")
        
        # Main links
        if card.links:
            linksGroup = QGroupBox("Main Links")
            linksGroup.setStyleSheet(f"font-size: {12 * self._scale_factor}px; font-weight: bold;")
            linksLayout = QVBoxLayout(linksGroup)
            linksLayout.setSpacing(int(4 * self._scale_factor))
            
            for link in card.links:
                linkLabel = self._create_styled_link(link)
                linksLayout.addWidget(linkLabel)
            
            self.linksLayout.addWidget(linksGroup)
        
        # Subsection links
        for title, links in card.subsections.items():
            if links:
                subGroup = QGroupBox(title)
                subGroup.setStyleSheet(f"font-size: {12 * self._scale_factor}px; font-weight: bold;")
                subLayout = QVBoxLayout(subGroup)
                subLayout.setSpacing(int(4 * self._scale_factor))
                
                for link in links:
                    linkLabel = self._create_styled_link(link)
                    subLayout.addWidget(linkLabel)
                
                self.linksLayout.addWidget(subGroup)
        
    def _create_styled_link(self, link):
        """Create a styled link label with proper scaling applied."""
        linkLabel = QLabel()
        
        # Determine base styling from link properties
        style = ""
        if hasattr(link, 'font_size') and link.font_size:
            # Convert em-based font size to pixel size with scale factor applied
            if 'em' in link.font_size:
                base_size = float(link.font_size.replace('em', ''))
                scaled_size = base_size * self._scale_factor
                style += f"font-size: {scaled_size}em; "
            elif 'px' in link.font_size:
                base_size = float(link.font_size.replace('px', ''))
                scaled_size = base_size * self._scale_factor
                style += f"font-size: {scaled_size}px; "
            elif '%' in link.font_size:
                base_size = float(link.font_size.replace('%', ''))
                scaled_size = base_size * self._scale_factor
                style += f"font-size: {scaled_size}%; "
            else:
                # For other units, just use as is
                style += f"font-size: {link.font_size}; "
        else:
            # Default size with scale factor
            style += f"font-size: {1.0 * self._scale_factor}em; "
        
        if hasattr(link, 'font_color') and link.font_color:
            style += f"color: {link.font_color}; "
        
        # Add hover effect
        style += "text-decoration: none; "
        
        # Set the label text with styling
        if style:
            linkLabel.setText(f'<a href="{link.url}" style="{style}">{link.name}</a>')
        else:
            linkLabel.setText(f'<a href="{link.url}">{link.name}</a>')
        
        # Enable link opening
        linkLabel.setOpenExternalLinks(True)
        linkLabel.setTextFormat(Qt.TextFormat.RichText)
        linkLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        
        # Add scale transform on hover using stylesheet
        linkLabel.setStyleSheet(f"""
            QLabel:hover {{
                transform: scale(1.05);
            }}
        """)
        
        return linkLabel
    
    def resetZoom(self):
        """Reset zoom to 100%."""
        self.scale_factor = 1.0
                


class MainWindow(QMainWindow):
    """Main window of the Startup Dashboard Editor application."""
    
    # Signal to notify when application-wide zoom level changes
    zoomChanged = pyqtSignal(float)
    
    def __init__(self, last_commit_date=None):
        super().__init__()
        
        self.model = StartupPageModel()
        self.current_file = None
        self.dark_mode = False
        self.last_commit_date = last_commit_date or ""
        self.zoomIndicator = None  # Initialize the zoomIndicator attribute
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Set dark mode from settings if available
        saved_dark_mode = self.settings_manager.get_setting("dark_mode", False)
        if saved_dark_mode:
            self.dark_mode = saved_dark_mode
            
        # Initialize zoom level from settings
        self.zoom_level = self.settings_manager.get_setting("zoom_level", 1.0)
        
        # List of UI components that should be scaled with zoom
        self.scalable_components = []
        
        self.initUI()
        
        # Load last file if available
        last_file = self.settings_manager.get_last_file()
        if last_file and os.path.exists(last_file):
            self.open_file(last_file)
    
    def initUI(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("The Startup Dashboard Editor")
        self.setMinimumSize(1000, 700)
        
        # Create menu bar
        self.createMenuBar()
        
        # Create toolbar
        self.createToolBar()
        
        # Create central widget
        self.createCentralWidget()
        
        # Create status bar with zoom indicator
        self.statusBar().showMessage("Ready")
        
        # Add zoom indicator to the status bar
        self.zoomIndicator = QLabel(f"Zoom: {int(self.zoom_level * 100)}%")
        self.statusBar().addPermanentWidget(self.zoomIndicator)
        
        # Ensure the zoomIndicator is visible and correctly initialized
        self.zoomIndicator.setVisible(True)
    
    def createMenuBar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        fileMenu = menubar.addMenu("&File")
        
        openAction = QAction("&Open...", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip("Open an existing HTML file")
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)
        
        saveAction = QAction("&Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("Save the current file")
        saveAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAction)
        
        saveAsAction = QAction("Save &As...", self)
        saveAsAction.setShortcut("Ctrl+Shift+S")
        saveAsAction.setStatusTip("Save the file with a new name")
        saveAsAction.triggered.connect(self.saveFileAs)
        fileMenu.addAction(saveAsAction)
        
        fileMenu.addSeparator()
        
        exitAction = QAction("E&xit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit the application")
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
        # Edit menu
        editMenu = menubar.addMenu("&Edit")
        
        addCardAction = QAction("Add &Card", self)
        addCardAction.setStatusTip("Add a new card section")
        addCardAction.triggered.connect(self.addCard)
        editMenu.addAction(addCardAction)
        
        # View menu
        viewMenu = menubar.addMenu("&View")
        
        toggleThemeAction = QAction("Toggle &Dark Mode", self)
        toggleThemeAction.setShortcut("Ctrl+D")
        toggleThemeAction.setStatusTip("Toggle between light and dark mode")
        toggleThemeAction.triggered.connect(self.toggleTheme)
        viewMenu.addAction(toggleThemeAction)
        
        # Zoom actions
        viewMenu.addSeparator()
        
        zoomInAction = QAction("Zoom &In", self)
        zoomInAction.setShortcut("Ctrl++")
        zoomInAction.setStatusTip("Increase zoom level")
        zoomInAction.triggered.connect(self.zoomIn)
        viewMenu.addAction(zoomInAction)
        
        zoomOutAction = QAction("Zoom &Out", self)
        zoomOutAction.setShortcut("Ctrl+-")
        zoomOutAction.setStatusTip("Decrease zoom level")
        zoomOutAction.triggered.connect(self.zoomOut)
        viewMenu.addAction(zoomOutAction)
        
        resetZoomAction = QAction("&Reset Zoom", self)
        resetZoomAction.setShortcut("Ctrl+0")
        resetZoomAction.setStatusTip("Reset zoom to 100%")
        resetZoomAction.triggered.connect(self.resetZoom)
        viewMenu.addAction(resetZoomAction)
        
        # Help menu
        helpMenu = menubar.addMenu("&Help")
        
        viewSummaryAction = QAction("View &Summary", self)
        viewSummaryAction.setStatusTip("Open the project summary document")
        viewSummaryAction.triggered.connect(self.viewSummary)
        helpMenu.addAction(viewSummaryAction)
        
        aboutAction = QAction("&About", self)
        aboutAction.setStatusTip("Show information about the application")
        aboutAction.triggered.connect(self.showAbout)
        helpMenu.addAction(aboutAction)
    
    def createToolBar(self):
        """Create the application toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        
        openAction = QAction("Open", self)
        openAction.setStatusTip("Open an existing HTML file")
        openAction.triggered.connect(self.openFile)
        toolbar.addAction(openAction)
        
        saveAction = QAction("Save", self)
        saveAction.setStatusTip("Save the current file")
        saveAction.triggered.connect(self.saveFile)
        toolbar.addAction(saveAction)
        
        toolbar.addSeparator()
        
        addCardAction = QAction("Add Card", self)
        addCardAction.setStatusTip("Add a new card section")
        addCardAction.triggered.connect(self.addCard)
        toolbar.addAction(addCardAction)
        
        editCardAction = QAction("Edit Card", self)
        editCardAction.setStatusTip("Edit the selected card")
        editCardAction.triggered.connect(self.editCard)
        toolbar.addAction(editCardAction)
        
        removeCardAction = QAction("Remove Card", self)
        removeCardAction.setStatusTip("Remove the selected card")
        removeCardAction.triggered.connect(self.removeCard)
        toolbar.addAction(removeCardAction)
        
        toolbar.addSeparator()
        
        toggleThemeAction = QAction("Toggle Theme", self)
        toggleThemeAction.setStatusTip("Toggle between light and dark mode")
        toggleThemeAction.triggered.connect(self.toggleTheme)
        toolbar.addAction(toggleThemeAction)
        
        toolbar.addSeparator()
        
        zoomInAction = QAction("Zoom In", self)
        zoomInAction.setStatusTip("Increase zoom level")
        zoomInAction.triggered.connect(self.zoomIn)
        toolbar.addAction(zoomInAction)
        
        zoomOutAction = QAction("Zoom Out", self)
        zoomOutAction.setStatusTip("Decrease zoom level")
        zoomOutAction.triggered.connect(self.zoomOut)
        toolbar.addAction(zoomOutAction)
        
        resetZoomAction = QAction("Reset Zoom", self)
        resetZoomAction.setStatusTip("Reset zoom to 100%")
        resetZoomAction.triggered.connect(self.resetZoom)
        toolbar.addAction(resetZoomAction)
        
        self.addToolBar(toolbar)
    
    def createCentralWidget(self):
        """Create the central widget with card list and preview."""
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel: Card list
        leftPanel = QWidget()
        leftLayout = QVBoxLayout(leftPanel)
        
        cardListLabel = QLabel("Cards")
        cardListLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardListLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.scalable_components.append({"widget": cardListLabel, "base_font_size": 14})
        
        self.cardListWidget = QListWidget()
        self.cardListWidget.setMinimumWidth(250)
        self.cardListWidget.currentItemChanged.connect(self.onCardSelected)
        self.scalable_components.append({"widget": self.cardListWidget, "base_font_size": 9})
        
        # Enable drag and drop reordering
        self.cardListWidget.setDragEnabled(True)
        self.cardListWidget.setAcceptDrops(True)
        self.cardListWidget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.cardListWidget.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.cardListWidget.model().rowsMoved.connect(self.onCardOrderChanged)
        
        buttonLayout = QHBoxLayout()
        addButton = QPushButton("Add Card")
        addButton.clicked.connect(self.addCard)
        self.scalable_components.append({"widget": addButton, "base_font_size": 9})
        
        editButton = QPushButton("Edit Card")
        editButton.clicked.connect(self.editCard)
        self.scalable_components.append({"widget": editButton, "base_font_size": 9})
        
        removeButton = QPushButton("Remove Card")
        removeButton.clicked.connect(self.removeCard)
        self.scalable_components.append({"widget": removeButton, "base_font_size": 9})
        
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(editButton)
        buttonLayout.addWidget(removeButton)
        
        leftLayout.addWidget(cardListLabel)
        leftLayout.addWidget(self.cardListWidget)
        leftLayout.addLayout(buttonLayout)
        
        # Right panel: Card preview
        rightPanel = QWidget()
        rightLayout = QVBoxLayout(rightPanel)
        
        previewLabel = QLabel("Preview")
        previewLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        previewLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.scalable_components.append({"widget": previewLabel, "base_font_size": 14})
        
        self.previewWidget = CardPreviewWidget()
        
        # Connect zoom changed signal to update UI
        self.previewWidget.zoomChanged.connect(self.onZoomChanged)
        
        # Set initial zoom level from settings
        self.previewWidget.scale_factor = self.zoom_level
        
        # Apply initial scaling to all scalable components
        self.applyGlobalScaling(self.zoom_level)
        
        rightLayout.addWidget(previewLabel)
        rightLayout.addWidget(self.previewWidget)
        
        # Add panels to splitter
        splitter.addWidget(leftPanel)
        splitter.addWidget(rightPanel)
        
        # Set initial sizes (30% / 70%)
        splitter.setSizes([300, 700])
        
        # Install event filter on the main window to capture wheel events anywhere in the application
        self.installEventFilter(self)
        
        self.setCentralWidget(splitter)
    
    def onCardSelected(self, current, previous):
        """Handle card selection in the list."""
        if current:
            card = current.data(Qt.ItemDataRole.UserRole)
            self.previewWidget.setCard(card)
        else:
            self.previewWidget.setCard(None)
    
    def addCard(self):
        """Add a new card to the page."""
        dialog = CardEditorDialog(parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            card = dialog.card
            self.model.add_card(card)
            
            item = QListWidgetItem(card.title)
            item.setData(Qt.ItemDataRole.UserRole, card)
            self.cardListWidget.addItem(item)
            
            self.statusBar().showMessage(f"Added new card: {card.title}")
    
    def editCard(self):
        """Edit the selected card."""
        current_item = self.cardListWidget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a card to edit.")
            return
        
        card = current_item.data(Qt.ItemDataRole.UserRole)
        dialog = CardEditorDialog(card, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update item text
            current_item.setText(card.title)
            # Update preview
            self.previewWidget.setCard(card)
            
            self.statusBar().showMessage(f"Updated card: {card.title}")
    
    def removeCard(self):
        """Remove the selected card."""
        current_item = self.cardListWidget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a card to remove.")
            return
        
        card = current_item.data(Qt.ItemDataRole.UserRole)
        
        # Ask for confirmation
        confirm = QMessageBox.question(
            self, "Confirm Removal", 
            f"Are you sure you want to remove the card '{card.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.model.remove_card(card)
            self.cardListWidget.takeItem(self.cardListWidget.row(current_item))
            self.previewWidget.setCard(None)
            
            self.statusBar().showMessage(f"Removed card: {card.title}")
    
    def open_file(self, file_path):
        """Open the specified file."""
        try:
            self.model = HtmlParser.load_from_file(file_path)
            self.current_file = file_path
            self.settings_manager.set_last_file(file_path)
            self.updateCardList()
            
            self.statusBar().showMessage(f"Opened file: {file_path}")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
            return False
    
    def openFile(self):
        """Open an HTML file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open HTML File", "", "HTML Files (*.html);;All Files (*)"
        )
        
        if file_path:
            self.open_file(file_path)
    
    def saveFile(self):
        """Save the current file."""
        if not self.current_file:
            self.saveFileAs()
            return
        
        try:
            HtmlParser.save_to_file(self.model, self.current_file)
            self.settings_manager.set_last_file(self.current_file)
            self.statusBar().showMessage(f"Saved file: {self.current_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
    
    def saveFileAs(self):
        """Save the file with a new name."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save HTML File", "", "HTML Files (*.html);;All Files (*)"
        )
        
        if file_path:
            try:
                HtmlParser.save_to_file(self.model, file_path)
                self.current_file = file_path
                self.settings_manager.set_last_file(file_path)
                self.statusBar().showMessage(f"Saved file as: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
    
    def updateCardList(self):
        """Update the card list with the current model."""
        self.cardListWidget.clear()
        for card in self.model.cards:
            item = QListWidgetItem(card.title)
            item.setData(Qt.ItemDataRole.UserRole, card)
            self.cardListWidget.addItem(item)
    
    def toggleTheme(self):
        """Toggle between light and dark mode."""
        self.dark_mode = not self.dark_mode
        
        # Save dark mode setting
        self.settings_manager.set_setting("dark_mode", self.dark_mode)
        
        app = QApplication.instance()
        palette = QPalette()
        
        if self.dark_mode:
            # Dark theme
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
            palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            
            app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
            
            self.statusBar().showMessage("Dark theme applied")
        else:
            # Light theme (default)
            palette = app.style().standardPalette()
            
            app.setStyleSheet("")
            
            self.statusBar().showMessage("Light theme applied")
        
        app.setPalette(palette)
    
    def showAbout(self):
        """Show information about the application."""
        # Format the last commit info
        commit_info = f"<p>Last commit: {self.last_commit_date}</p>" if self.last_commit_date else ""
        
        # Create the about dialog HTML
        about_html = f"""<h1>The Startup Dashboard Editor</h1>
            <p>Version 1.0</p>
            <p>A Qt6-based editor for managing your Startup dashboard.</p>
            {commit_info}
            <p><a href="https://github.com/juren53/JAUs-Startup-Page/commits/main">View Commit History</a></p>
            <p>Copyright &copy; 2025</p>"""
        
        QMessageBox.about(
            self, "About The Startup Dashboard Editor", 
            about_html
        )
    
    def viewSummary(self):
        """Open the SUMMARY.md file with the system's default application."""
        try:
            # Check if the file exists in the docs directory
            summary_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                     "docs", "SUMMARY.md")
            
            if os.path.exists(summary_path):
                # Open the file with the default application
                if sys.platform == 'win32':
                    os.startfile(summary_path)
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', summary_path], check=True)
                else:  # Linux and others
                    subprocess.run(['xdg-open', summary_path], check=True)
                
                self.statusBar().showMessage(f"Opened Summary document: {summary_path}")
            else:
                # Check if it's in the root directory instead
                summary_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                         "FINAL_SUMMARY.md")
                if os.path.exists(summary_path):
                    if sys.platform == 'win32':
                        os.startfile(summary_path)
                    elif sys.platform == 'darwin':  # macOS
                        subprocess.run(['open', summary_path], check=True)
                    else:  # Linux and others
                        subprocess.run(['xdg-open', summary_path], check=True)
                    
                    self.statusBar().showMessage(f"Opened Summary document: {summary_path}")
                else:
                    QMessageBox.warning(self, "File Not Found", "Summary document not found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open Summary document: {str(e)}")
    
    def onCardOrderChanged(self, parent, start, end, destination, row):
        """Handle reordering of cards in the list."""
        # Update the model to reflect the new order
        new_order = []
        for i in range(self.cardListWidget.count()):
            item = self.cardListWidget.item(i)
            card = item.data(Qt.ItemDataRole.UserRole)
            new_order.append(card)
        
        self.model.cards = new_order
        self.statusBar().showMessage("Card order updated")
    
    def zoomIn(self):
        """Increase zoom level."""
        self.previewWidget.scale_factor = self.previewWidget.scale_factor + 0.1
    
    def zoomOut(self):
        """Decrease zoom level."""
        self.previewWidget.scale_factor = self.previewWidget.scale_factor - 0.1
    
    def resetZoom(self):
        """Reset zoom to 100%."""
        self.previewWidget.resetZoom()
    
    def onZoomChanged(self, scale_factor):
        """Handle zoom level changes."""
        # Update zoom level in settings
        self.zoom_level = scale_factor
        self.settings_manager.set_setting("zoom_level", scale_factor)
        
        # Apply scaling to all scalable components
        self.applyGlobalScaling(scale_factor)
        
        # Update zoom indicator in status bar
        if self.zoomIndicator:
            self.zoomIndicator.setText(f"Zoom: {int(scale_factor * 100)}%")
        
        # Emit signal for other components that might need to respond to zoom changes
        self.zoomChanged.emit(scale_factor)
    
    def applyGlobalScaling(self, scale_factor):
        """Apply scaling to all scalable components in the UI."""
        # Scale all registered scalable components
        for component in self.scalable_components:
            widget = component["widget"]
            base_size = component["base_font_size"]
            
            # Apply font scaling
            font = widget.font()
            font.setPointSizeF(base_size * scale_factor)
            widget.setFont(font)
            
            # For list widget, adjust item heights
            if isinstance(widget, QListWidget):
                for i in range(widget.count()):
                    item = widget.item(i)
                    item.setSizeHint(QSize(item.sizeHint().width(), int(24 * scale_factor)))
    
    def eventFilter(self, watched, event):
        """Event filter to capture wheel events for zooming anywhere in the application."""
        if event.type() == event.Type.Wheel and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Get wheel delta and calculate zoom change
            delta = event.angleDelta().y()
            zoom_delta = 0.1 if delta > 0 else -0.1
            
            # Update zoom level through the preview widget, which will propagate changes
            new_scale = self.zoom_level + zoom_delta
            new_scale = max(0.5, min(3.0, new_scale))  # Ensure zoom stays within bounds
            
            # Only update if the zoom level actually changed
            if new_scale != self.zoom_level:
                self.previewWidget.scale_factor = new_scale
            
            # Consume the event
            return True
            
        # Let other events pass through
        return super().eventFilter(watched, event)
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Check if there are unsaved changes
        if self.model.cards:
            reply = QMessageBox.question(
                self, "Confirm Exit", 
                "Are you sure you want to exit? Any unsaved changes will be lost.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

