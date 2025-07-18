from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QPushButton, QGroupBox, 
    QTabWidget, QListWidget, QListWidgetItem, QMessageBox,
    QWidget, QAbstractItemView, QComboBox, QColorDialog, QFrame,
    QPlainTextEdit, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
import re
from src.models.card_model import Card, Link


class LinkEditorDialog(QDialog):
    """Dialog for editing a single link."""
    
    def __init__(self, link=None, parent=None):
        super().__init__(parent)
        
        self.link = link if link else Link()
        self.setWindowTitle("Edit Link")
        self.setMinimumWidth(450)  # Increased width for new controls
        
        self.initUI()
    
    def initUI(self):
        """Initialize the UI components."""
        layout = QFormLayout(self)
        
        # Name field
        self.nameEdit = QLineEdit(self.link.name)
        layout.addRow("Name:", self.nameEdit)
        
        # URL field with Parse button
        urlLayout = QHBoxLayout()
        self.urlEdit = QLineEdit(self.link.url)
        self.parseButton = QPushButton("Parse URL,Description")
        self.parseButton.clicked.connect(self.parseUrlDescription)
        urlLayout.addWidget(self.urlEdit)
        urlLayout.addWidget(self.parseButton)
        layout.addRow("URL:", urlLayout)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addRow("Styling:", separator)
        
        # Font size dropdown
        self.fontSizeCombo = QComboBox()
        self.fontSizeCombo.addItem("Default", "")
        self.fontSizeCombo.addItem("Smaller (0.8em)", "0.8em")
        self.fontSizeCombo.addItem("Small (0.9em)", "0.9em")
        self.fontSizeCombo.addItem("Normal (1em)", "1em")
        self.fontSizeCombo.addItem("Large (1.2em)", "1.2em")
        self.fontSizeCombo.addItem("Larger (1.5em)", "1.5em")
        self.fontSizeCombo.addItem("Extra Large (2em)", "2em")
        
        # Set the current value if it exists
        if self.link.font_size:
            index = self.fontSizeCombo.findData(self.link.font_size)
            if index >= 0:
                self.fontSizeCombo.setCurrentIndex(index)
        
        layout.addRow("Font Size:", self.fontSizeCombo)
        
        # Font color picker
        colorLayout = QHBoxLayout()
        self.fontColorEdit = QLineEdit(self.link.font_color)
        self.fontColorEdit.setPlaceholderText("e.g., #FF0000 or rgb(255,0,0)")
        
        self.colorPickerBtn = QPushButton("Pick Color")
        self.colorPickerBtn.clicked.connect(self.openColorPicker)
        
        colorLayout.addWidget(self.fontColorEdit)
        colorLayout.addWidget(self.colorPickerBtn)
        
        layout.addRow("Font Color:", colorLayout)
        
        # Preview label
        self.previewLabel = QLabel()
        self.updatePreview()
        layout.addRow("Preview:", self.previewLabel)
        
        # Connect signals to update preview
        self.nameEdit.textChanged.connect(self.updatePreview)
        self.fontSizeCombo.currentIndexChanged.connect(self.updatePreview)
        self.fontColorEdit.textChanged.connect(self.updatePreview)
        
        # Button box
        buttonBox = QHBoxLayout()
        
        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.accept)
        
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.reject)
        
        buttonBox.addWidget(saveButton)
        buttonBox.addWidget(cancelButton)
        buttonBox.setContentsMargins(0, 20, 0, 0)
        
        layout.addRow("", buttonBox)
    
    def openColorPicker(self):
        """Open a color picker dialog and update the color field."""
        # Initialize with current color if it exists
        current_color = self.fontColorEdit.text()
        initial_color = QColor(current_color) if current_color else QColor(0, 0, 0)
        
        color = QColorDialog.getColor(initial_color, self, "Select Font Color")
        if color.isValid():
            self.fontColorEdit.setText(color.name())
    
    def updatePreview(self):
        """Update the preview label with current settings."""
        name = self.nameEdit.text()
        font_size = self.fontSizeCombo.currentData()
        font_color = self.fontColorEdit.text()
        
        style = ""
        if font_size:
            style += f"font-size: {font_size}; "
        if font_color:
            style += f"color: {font_color}; "
        
        if style:
            self.previewLabel.setText(f'<span style="{style}">{name}</span>')
        else:
            self.previewLabel.setText(name)
    
    def accept(self):
        """Called when the user accepts the dialog."""
        name = self.nameEdit.text().strip()
        url = self.urlEdit.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Validation Error", "Link name cannot be empty.")
            return
        
        if not url:
            QMessageBox.warning(self, "Validation Error", "Link URL cannot be empty.")
            return
        
        # Get font styling
        font_size = self.fontSizeCombo.currentData()
        font_color = self.fontColorEdit.text().strip()
        
        # Validate color if provided
        if font_color and not self.isValidColor(font_color):
            QMessageBox.warning(self, "Validation Error", "Invalid color format. Use hex (#RRGGBB) or rgb(r,g,b).")
            return
        
        self.link.name = name
        self.link.url = url
        self.link.font_size = font_size
        self.link.font_color = font_color
        
        super().accept()
    
    def isValidColor(self, color):
        """Check if the provided color string is valid."""
        # Simple validation for hex and rgb formats
        hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        rgb_pattern = r'^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$'
        
        if re.match(hex_pattern, color) or re.match(rgb_pattern, color):
            return True
        return False
        
    def parseUrlDescription(self):
        """Parse a URL,Description pair and populate the fields."""
        text, ok = QInputDialog.getText(
            self, 
            "Parse URL,Description", 
            "Enter in format 'URL,Description':",
            QLineEdit.EchoMode.Normal
        )
        
        if ok and text:
            # Split at the first comma
            parts = text.split(',', 1)
            if len(parts) != 2:
                QMessageBox.warning(
                    self, 
                    "Invalid Format", 
                    "Input must be in the format 'URL,Description'"
                )
                return
                
            url = parts[0].strip()
            name = parts[1].strip()
            
            if not url or not name:
                QMessageBox.warning(
                    self, 
                    "Invalid Format", 
                    "Both URL and Description must be non-empty"
                )
                return
                
            # Set the values
            self.urlEdit.setText(url)
            self.nameEdit.setText(name)
            
            # Update the preview
            self.updatePreview()


class CardEditorDialog(QDialog):
    """Dialog for editing a card with its links and subsections."""
    
    def __init__(self, card=None, parent=None):
        super().__init__(parent)
        
        self.card = card if card else Card()
        self.setWindowTitle("Edit Card")
        self.setMinimumSize(550, 350)
        
        self.initUI()
    
    def initUI(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # Reduce outer margins
        layout.setSpacing(6)  # Reduce spacing between elements
        
        # Card title
        formLayout = QFormLayout()
        formLayout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        formLayout.setSpacing(6)  # Reduce spacing
        self.titleEdit = QLineEdit(self.card.title)
        formLayout.addRow("Title:", self.titleEdit)
        
        # Icon (optional)
        self.iconEdit = QLineEdit(self.card.icon)
        formLayout.addRow("Icon (optional):", self.iconEdit)
        
        # Background Color
        colorLayout = QHBoxLayout()
        self.bgColorEdit = QLineEdit(self.card.background_color if hasattr(self.card, 'background_color') else "")
        self.bgColorEdit.setPlaceholderText("e.g., #F5F5F5 or rgb(245,245,245)")
        
        self.bgColorPickerBtn = QPushButton("Pick Color")
        self.bgColorPickerBtn.clicked.connect(self.openBackgroundColorPicker)
        
        colorLayout.addWidget(self.bgColorEdit)
        colorLayout.addWidget(self.bgColorPickerBtn)
        
        formLayout.addRow("Background Color:", colorLayout)
        
        # Preview color indicator
        self.colorPreview = QFrame()
        self.colorPreview.setMinimumSize(20, 20)
        self.colorPreview.setFrameShape(QFrame.Shape.Box)
        self.updateColorPreview()
        
        # Connect signal to update preview
        self.bgColorEdit.textChanged.connect(self.updateColorPreview)
        
        formLayout.addRow("Color Preview:", self.colorPreview)
        
        layout.addLayout(formLayout)
        
        # Tabs for main links and subsections
        tabWidget = QTabWidget()
        
        # Main links tab
        mainLinksTab = QWidget()
        mainLinksLayout = QVBoxLayout(mainLinksTab)
        mainLinksLayout.setContentsMargins(6, 6, 6, 6)  # Reduce margins
        mainLinksLayout.setSpacing(6)  # Reduce spacing
        
        # Create a title label at the top
        mainLinksLabel = QLabel("Main Links:")
        mainLinksLabel.setStyleSheet("font-size: 12px; font-weight: bold;")  # Smaller font
        mainLinksLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        mainLinksLayout.addWidget(mainLinksLabel, 0, Qt.AlignmentFlag.AlignTop)
        
        # Create the list widget
        self.mainLinksList = QListWidget()
        self.updateMainLinksList()
        self.mainLinksList.setMinimumHeight(120)  # Reduced from 200
        self.mainLinksList.setDragEnabled(True)
        self.mainLinksList.setAcceptDrops(True)
        self.mainLinksList.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.mainLinksList.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.mainLinksList.model().rowsMoved.connect(self.onMainLinksOrderChanged)
        
        # Add the list with stretch factor to ensure it fills available space
        mainLinksLayout.addWidget(self.mainLinksList, 1)
        
        # Create button layout with smaller buttons
        mainLinksButtonLayout = QHBoxLayout()
        mainLinksButtonLayout.setContentsMargins(0, 0, 0, 0)
        mainLinksButtonLayout.setSpacing(4)  # Reduce spacing between buttons
        
        addMainLinkButton = QPushButton("Add Link")
        addMainLinkButton.setMinimumHeight(32)  # Increased button height for readability
        addMainLinkButton.clicked.connect(self.addMainLink)
        
        addMultipleMainLinksButton = QPushButton("Add Multiple Links")
        addMultipleMainLinksButton.setMinimumHeight(32)
        addMultipleMainLinksButton.clicked.connect(self.addMultipleMainLinks)
        
        editMainLinkButton = QPushButton("Edit Link")
        editMainLinkButton.setMinimumHeight(32)
        editMainLinkButton.clicked.connect(self.editMainLink)
        
        removeMainLinkButton = QPushButton("Remove Link")
        removeMainLinkButton.setMinimumHeight(32)
        removeMainLinkButton.clicked.connect(self.removeMainLink)
        
        mainLinksButtonLayout.addWidget(addMainLinkButton)
        mainLinksButtonLayout.addWidget(addMultipleMainLinksButton)
        mainLinksButtonLayout.addWidget(editMainLinkButton)
        mainLinksButtonLayout.addWidget(removeMainLinkButton)
        
        # Add button layout at the bottom with no stretch factor
        mainLinksLayout.addLayout(mainLinksButtonLayout, 0)
        
        tabWidget.addTab(mainLinksTab, "Main Links")
        
        # Subsections tab - apply similar changes
        subsectionsTab = QWidget()
        subsectionsLayout = QVBoxLayout(subsectionsTab)
        subsectionsLayout.setContentsMargins(6, 6, 6, 6)  # Reduce margins
        subsectionsLayout.setSpacing(6)  # Reduce spacing
        
        # Create a title label at the top
        subsectionsLabel = QLabel("Additional Links:")
        subsectionsLabel.setStyleSheet("font-size: 12px; font-weight: bold;")  # Smaller font
        subsectionsLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        subsectionsLayout.addWidget(subsectionsLabel, 0, Qt.AlignmentFlag.AlignTop)
        
        # Create the list widget
        self.subsectionLinksList = QListWidget()
        self.updateSubsectionLinksList()
        self.subsectionLinksList.setMinimumHeight(120)  # Reduced from 200
        self.subsectionLinksList.setDragEnabled(True)
        self.subsectionLinksList.setAcceptDrops(True)
        self.subsectionLinksList.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.subsectionLinksList.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.subsectionLinksList.model().rowsMoved.connect(self.onSubsectionLinksOrderChanged)
        
        # Add the list with stretch factor to ensure it fills available space
        subsectionsLayout.addWidget(self.subsectionLinksList, 1)
        
        # Create button layout with smaller buttons
        subsectionButtonLayout = QHBoxLayout()
        subsectionButtonLayout.setContentsMargins(0, 0, 0, 0)
        subsectionButtonLayout.setSpacing(4)  # Reduce spacing between buttons
        
        addSubsectionLinkButton = QPushButton("Add Link")
        addSubsectionLinkButton.setMinimumHeight(32)  # Increased button height for readability
        addSubsectionLinkButton.clicked.connect(self.addSubsectionLink)
        
        addMultipleSubsectionLinksButton = QPushButton("Add Multiple Links")
        addMultipleSubsectionLinksButton.setMinimumHeight(32)
        addMultipleSubsectionLinksButton.clicked.connect(self.addMultipleSubsectionLinks)
        
        editSubsectionLinkButton = QPushButton("Edit Link")
        editSubsectionLinkButton.setMinimumHeight(32)
        editSubsectionLinkButton.clicked.connect(self.editSubsectionLink)
        
        removeSubsectionLinkButton = QPushButton("Remove Link")
        removeSubsectionLinkButton.setMinimumHeight(32)
        removeSubsectionLinkButton.clicked.connect(self.removeSubsectionLink)
        
        subsectionButtonLayout.addWidget(addSubsectionLinkButton)
        subsectionButtonLayout.addWidget(addMultipleSubsectionLinksButton)
        subsectionButtonLayout.addWidget(editSubsectionLinkButton)
        subsectionButtonLayout.addWidget(removeSubsectionLinkButton)
        
        # Add button layout at the bottom with no stretch factor
        subsectionsLayout.addLayout(subsectionButtonLayout, 0)
        
        tabWidget.addTab(subsectionsTab, "Additional Links")
        
        layout.addWidget(tabWidget)
        
        # Dialog buttons
        buttonLayout = QHBoxLayout()
        saveButton = QPushButton("Save")
        saveButton.setMinimumHeight(32)  # Increased button height for readability
        saveButton.clicked.connect(self.accept)
        
        cancelButton = QPushButton("Cancel")
        cancelButton.setMinimumHeight(32)  # Increased button height for readability
        cancelButton.clicked.connect(self.reject)
        
        buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(cancelButton)
        buttonLayout.setContentsMargins(0, 10, 0, 0)  # Reduced top margin
        
        layout.addLayout(buttonLayout)
    
    def onMainLinksOrderChanged(self, parent, start, end, destination, row):
        """Handle reordering of main links in the list."""
        # Update the card's links to reflect the new order
        new_order = []
        for i in range(self.mainLinksList.count()):
            item = self.mainLinksList.item(i)
            link = item.data(Qt.ItemDataRole.UserRole)
            new_order.append(link)
        
        self.card.links = new_order

    def onSubsectionLinksOrderChanged(self, parent, start, end, destination, row):
        """Handle reordering of subsection links in the list."""
        # Update the card's subsection links to reflect the new order
        subsection_title = "Additional Links"
        new_order = []
        for i in range(self.subsectionLinksList.count()):
            item = self.subsectionLinksList.item(i)
            link = item.data(Qt.ItemDataRole.UserRole)
            new_order.append(link)
        
        if subsection_title in self.card.subsections:
            self.card.subsections[subsection_title] = new_order
    
    def updateMainLinksList(self):
        """Update the list of main links."""
        self.mainLinksList.clear()
        for link in self.card.links:
            item = QListWidgetItem(f"{link.name} - {link.url}")
            item.setData(Qt.ItemDataRole.UserRole, link)
            self.mainLinksList.addItem(item)
    
    def updateSubsectionLinksList(self):
        """Update the list of subsection links."""
        self.subsectionLinksList.clear()
        
        # For simplicity, we're just showing the first subsection (if it exists)
        subsection_title = "Additional Links"
        if subsection_title in self.card.subsections:
            for link in self.card.subsections[subsection_title]:
                item = QListWidgetItem(f"{link.name} - {link.url}")
                item.setData(Qt.ItemDataRole.UserRole, link)
                self.subsectionLinksList.addItem(item)
    
    def addMainLink(self):
        """Add a new link to the main section."""
        dialog = LinkEditorDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.card.add_link(dialog.link)
            self.updateMainLinksList()
    
    def editMainLink(self):
        """Edit the selected main link."""
        selected_item = self.mainLinksList.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Warning", "Please select a link to edit.")
            return
        
        link = selected_item.data(Qt.ItemDataRole.UserRole)
        dialog = LinkEditorDialog(link, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.updateMainLinksList()
    
    def removeMainLink(self):
        """Remove the selected main link."""
        selected_item = self.mainLinksList.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Warning", "Please select a link to remove.")
            return
        
        link = selected_item.data(Qt.ItemDataRole.UserRole)
        
        # Ask for confirmation
        confirm = QMessageBox.question(
            self, "Confirm Removal", 
            f"Are you sure you want to remove '{link.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.card.remove_link(link)
            self.updateMainLinksList()
    
    def addSubsectionLink(self):
        """Add a new link to the subsection."""
        dialog = LinkEditorDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            subsection_title = "Additional Links"
            self.card.add_subsection_link(subsection_title, dialog.link)
            self.updateSubsectionLinksList()
    
    def editSubsectionLink(self):
        """Edit the selected subsection link."""
        selected_item = self.subsectionLinksList.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Warning", "Please select a link to edit.")
            return
        
        link = selected_item.data(Qt.ItemDataRole.UserRole)
        dialog = LinkEditorDialog(link, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.updateSubsectionLinksList()
    
    def removeSubsectionLink(self):
        """Remove the selected subsection link."""
        selected_item = self.subsectionLinksList.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Warning", "Please select a link to remove.")
            return
        
        link = selected_item.data(Qt.ItemDataRole.UserRole)
        
        # Ask for confirmation
        confirm = QMessageBox.question(
            self, "Confirm Removal", 
            f"Are you sure you want to remove '{link.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            subsection_title = "Additional Links"
            self.card.remove_subsection_link(subsection_title, link)
            self.updateSubsectionLinksList()
    
    def addMultipleMainLinks(self):
        """Add multiple links to the main section from URL,Description pairs."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Multiple Links")
        dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Instructions
        instructionsLabel = QLabel(
            "Enter one URL,Description pair per line.\n"
            "Format: URL,Description"
        )
        layout.addWidget(instructionsLabel)
        
        # Text input area
        textEdit = QPlainTextEdit()
        layout.addWidget(textEdit)
        
        # Button box
        buttonBox = QHBoxLayout()
        addButton = QPushButton("Add Links")
        cancelButton = QPushButton("Cancel")
        
        buttonBox.addWidget(addButton)
        buttonBox.addWidget(cancelButton)
        layout.addLayout(buttonBox)
        
        # Connect signals
        addButton.clicked.connect(dialog.accept)
        cancelButton.clicked.connect(dialog.reject)
        
        # Show dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text = textEdit.toPlainText()
            lines = text.strip().split('\n')
            
            added_count = 0
            skipped_count = 0
            
            for line in lines:
                if not line.strip():
                    continue
                    
                parts = line.split(',', 1)
                if len(parts) == 2:
                    url = parts[0].strip()
                    name = parts[1].strip()
                    
                    if url and name:
                        link = Link(name=name, url=url)
                        self.card.add_link(link)
                        added_count += 1
                    else:
                        skipped_count += 1
                else:
                    skipped_count += 1
            
            self.updateMainLinksList()
            
            # Show results
            QMessageBox.information(
                self,
                "Links Added",
                f"Added {added_count} links to main section.\n"
                f"Skipped {skipped_count} invalid entries."
            )
    
    def addMultipleSubsectionLinks(self):
        """Add multiple links to the subsection from URL,Description pairs."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Multiple Links")
        dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Instructions
        instructionsLabel = QLabel(
            "Enter one URL,Description pair per line.\n"
            "Format: URL,Description"
        )
        layout.addWidget(instructionsLabel)
        
        # Text input area
        textEdit = QPlainTextEdit()
        layout.addWidget(textEdit)
        
        # Button box
        buttonBox = QHBoxLayout()
        addButton = QPushButton("Add Links")
        cancelButton = QPushButton("Cancel")
        
        buttonBox.addWidget(addButton)
        buttonBox.addWidget(cancelButton)
        layout.addLayout(buttonBox)
        
        # Connect signals
        addButton.clicked.connect(dialog.accept)
        cancelButton.clicked.connect(dialog.reject)
        
        # Show dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text = textEdit.toPlainText()
            lines = text.strip().split('\n')
            
            subsection_title = "Additional Links"
            added_count = 0
            skipped_count = 0
            
            for line in lines:
                if not line.strip():
                    continue
                    
                parts = line.split(',', 1)
                if len(parts) == 2:
                    url = parts[0].strip()
                    name = parts[1].strip()
                    
                    if url and name:
                        link = Link(name=name, url=url)
                        self.card.add_subsection_link(subsection_title, link)
                        added_count += 1
                    else:
                        skipped_count += 1
                else:
                    skipped_count += 1
            
            self.updateSubsectionLinksList()
            
            # Show results
            QMessageBox.information(
                self,
                "Links Added",
                f"Added {added_count} links to additional section.\n"
                f"Skipped {skipped_count} invalid entries."
            )
    
    def accept(self):
        """Called when the user accepts the dialog."""
        title = self.titleEdit.text().strip()
        
        if not title:
            QMessageBox.warning(self, "Validation Error", "Card title cannot be empty.")
            return
        
        self.card.title = title
        self.card.icon = self.iconEdit.text().strip()
        self.card.background_color = self.bgColorEdit.text().strip()
        
        super().accept()
    
    def openBackgroundColorPicker(self):
        """Open a color picker dialog for the card background color."""
        current_color = self.bgColorEdit.text()
        initial_color = QColor(current_color) if current_color else QColor(245, 245, 245)  # Default light gray
        
        color = QColorDialog.getColor(initial_color, self, "Select Background Color")
        if color.isValid():
            self.bgColorEdit.setText(color.name())
    
    def updateColorPreview(self):
        """Update the color preview panel."""
        color_text = self.bgColorEdit.text()
        if color_text:
            try:
                self.colorPreview.setStyleSheet(f"background-color: {color_text};")
            except:
                # If invalid color, show red
                self.colorPreview.setStyleSheet("background-color: red;")
        else:
            # Default preview color
            self.colorPreview.setStyleSheet("background-color: #F5F5F5;")
