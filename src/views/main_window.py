import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QListWidgetItem, QTabWidget,
    QMessageBox, QFileDialog, QSplitter, QGroupBox, QScrollArea,
    QStatusBar, QToolBar, QApplication, QDialog, QAbstractItemView
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QColor, QPalette

from src.utils.html_parser import HtmlParser
from src.utils.settings_manager import SettingsManager
from src.views.card_editor import CardEditorDialog
from src.models.card_model import Card, StartupPageModel


class CardPreviewWidget(QWidget):
    """Widget for displaying a preview of a card."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.card = None
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
    
    def setCard(self, card):
        """Update the preview with the specified card."""
        self.card = card
        
        # Clear the current layout
        while self.linksLayout.count():
            child = self.linksLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not card:
            self.titleLabel.setText("No card selected")
            return
        
        self.titleLabel.setText(f"{card.title}")
        
        # Main links
        if card.links:
            linksGroup = QGroupBox("Main Links")
            linksLayout = QVBoxLayout(linksGroup)
            
            for link in card.links:
                # Build inline style if needed
                style = ""
                if hasattr(link, 'font_size') and link.font_size:
                    style += f"font-size: {link.font_size}; "
                if hasattr(link, 'font_color') and link.font_color:
                    style += f"color: {link.font_color}; "
                
                style_attr = f' style="{style}"' if style else ""
                linkLabel = QLabel(f'<a href="{link.url}"{style_attr}>{link.name}</a>')
                linkLabel.setTextFormat(Qt.TextFormat.RichText)
                linkLabel.setOpenExternalLinks(True)
                linksLayout.addWidget(linkLabel)
            
            self.linksLayout.addWidget(linksGroup)
        
        # Subsection links
        for title, links in card.subsections.items():
            if links:
                subGroup = QGroupBox(title)
                subLayout = QVBoxLayout(subGroup)
                
                for link in links:
                    # Build inline style if needed
                    style = ""
                    if hasattr(link, 'font_size') and link.font_size:
                        style += f"font-size: {link.font_size}; "
                    if hasattr(link, 'font_color') and link.font_color:
                        style += f"color: {link.font_color}; "
                    
                    style_attr = f' style="{style}"' if style else ""
                    linkLabel = QLabel(f'<a href="{link.url}"{style_attr}>{link.name}</a>')
                    linkLabel.setTextFormat(Qt.TextFormat.RichText)
                    linkLabel.setOpenExternalLinks(True)
                    subLayout.addWidget(linkLabel)
                
                self.linksLayout.addWidget(subGroup)
                


class MainWindow(QMainWindow):
    """Main window of the Startup Dashboard Editor application."""
    
    def __init__(self, last_commit_date=None):
        super().__init__()
        
        self.model = StartupPageModel()
        self.current_file = None
        self.dark_mode = False
        self.last_commit_date = last_commit_date or ""
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Set dark mode from settings if available
        saved_dark_mode = self.settings_manager.get_setting("dark_mode", False)
        if saved_dark_mode:
            self.dark_mode = saved_dark_mode
        
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
        
        # Create status bar
        self.statusBar().showMessage("Ready")
    
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
        
        # Help menu
        helpMenu = menubar.addMenu("&Help")
        
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
        
        self.cardListWidget = QListWidget()
        self.cardListWidget.setMinimumWidth(250)
        self.cardListWidget.currentItemChanged.connect(self.onCardSelected)
        
        # Enable drag and drop reordering
        self.cardListWidget.setDragEnabled(True)
        self.cardListWidget.setAcceptDrops(True)
        self.cardListWidget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.cardListWidget.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.cardListWidget.model().rowsMoved.connect(self.onCardOrderChanged)
        
        buttonLayout = QHBoxLayout()
        addButton = QPushButton("Add Card")
        addButton.clicked.connect(self.addCard)
        editButton = QPushButton("Edit Card")
        editButton.clicked.connect(self.editCard)
        removeButton = QPushButton("Remove Card")
        removeButton.clicked.connect(self.removeCard)
        
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
        
        self.previewWidget = CardPreviewWidget()
        
        rightLayout.addWidget(previewLabel)
        rightLayout.addWidget(self.previewWidget)
        
        # Add panels to splitter
        splitter.addWidget(leftPanel)
        splitter.addWidget(rightPanel)
        
        # Set initial sizes (30% / 70%)
        splitter.setSizes([300, 700])
        
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

