"""
Component Selector Dialog - Select a component from library to apply to car
"""

import sys
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QLabel,
    QPushButton, QGroupBox, QTextEdit, QListWidgetItem,
    QMessageBox
)
from PyQt5.QtCore import Qt

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.component_library import ComponentLibrary


class ComponentSelectorDialog(QDialog):
    """Dialog for selecting a component from the library"""
    
    def __init__(self, component_type, parent=None):
        """
        Initialize component selector dialog
        
        Args:
            component_type: Type of component to select ('engine', 'suspension', etc.)
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.component_type = component_type
        self.library = ComponentLibrary()
        self.selected_component = None
        
        self.init_ui()
        self.load_components()
        
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(f"Select {self.component_type.capitalize()} Component")
        self.setGeometry(250, 250, 700, 500)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Select a {self.component_type} component from the library:")
        title.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(title)
        
        # Main content with splitter layout
        content_layout = QHBoxLayout()
        
        # Left panel - Component list
        list_panel = QGroupBox("Available Components")
        list_layout = QVBoxLayout()
        
        self.component_list = QListWidget()
        self.component_list.currentItemChanged.connect(self.on_component_selected)
        list_layout.addWidget(self.component_list)
        
        list_panel.setLayout(list_layout)
        content_layout.addWidget(list_panel)
        
        # Right panel - Component details
        details_panel = QGroupBox("Component Details")
        details_layout = QVBoxLayout()
        
        self.name_label = QLabel("-")
        self.name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        details_layout.addWidget(QLabel("Name:"))
        details_layout.addWidget(self.name_label)
        
        self.tags_label = QLabel("-")
        details_layout.addWidget(QLabel("Tags:"))
        details_layout.addWidget(self.tags_label)
        
        details_layout.addWidget(QLabel("Description:"))
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setMaximumHeight(80)
        details_layout.addWidget(self.description_text)
        
        details_layout.addWidget(QLabel("Parameters:"))
        self.data_text = QTextEdit()
        self.data_text.setReadOnly(True)
        self.data_text.setStyleSheet("font-family: monospace;")
        details_layout.addWidget(self.data_text)
        
        details_panel.setLayout(details_layout)
        content_layout.addWidget(details_panel)
        
        content_layout.setStretch(0, 1)
        content_layout.setStretch(1, 2)
        
        layout.addLayout(content_layout)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        apply_btn = QPushButton("Apply Component")
        apply_btn.clicked.connect(self.apply_component)
        button_layout.addWidget(apply_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def load_components(self):
        """Load components of the specified type"""
        self.component_list.clear()
        components = self.library.get_components(self.component_type)
        
        if not components:
            item = QListWidgetItem("No components available")
            item.setFlags(Qt.NoItemFlags)
            self.component_list.addItem(item)
            return
        
        for component in components:
            item = QListWidgetItem(component.get('name', 'Unnamed'))
            item.setData(Qt.UserRole, component)
            self.component_list.addItem(item)
        
        # Select first item by default
        if self.component_list.count() > 0:
            self.component_list.setCurrentRow(0)
            
    def on_component_selected(self, current, previous):
        """Handle component selection"""
        if current is None:
            self.clear_details()
            return
        
        component = current.data(Qt.UserRole)
        if component is None:
            self.clear_details()
            return
            
        self.selected_component = component
        
        # Update details
        self.name_label.setText(component.get('name', '-'))
        
        tags = component.get('tags', [])
        self.tags_label.setText(', '.join(tags) if tags else '-')
        
        self.description_text.setPlainText(component.get('description', ''))
        
        # Format data
        data = component.get('data', {})
        if data:
            data_text = []
            for key, value in data.items():
                data_text.append(f"{key} = {value}")
            self.data_text.setPlainText('\n'.join(data_text))
        else:
            self.data_text.setPlainText("No parameters")
            
    def clear_details(self):
        """Clear component details"""
        self.name_label.setText("-")
        self.tags_label.setText("-")
        self.description_text.clear()
        self.data_text.clear()
        self.selected_component = None
        
    def apply_component(self):
        """Apply the selected component"""
        if not self.selected_component:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a component to apply."
            )
            return
        
        # Confirm application
        component_name = self.selected_component.get('name', 'Unknown')
        reply = QMessageBox.question(
            self,
            "Apply Component",
            f"Apply '{component_name}' to the car?\n\n"
            "This will update the current values in the editor.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.accept()
            
    def get_selected_component(self):
        """Get the selected component data"""
        return self.selected_component
