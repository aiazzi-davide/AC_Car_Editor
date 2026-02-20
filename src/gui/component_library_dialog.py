"""
Component Library Manager Dialog
"""

import sys
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QLabel,
    QPushButton, QGroupBox, QTextEdit, QComboBox, QLineEdit,
    QFormLayout, QMessageBox, QFileDialog, QInputDialog,
    QListWidgetItem, QSplitter, QTabWidget
)
from PyQt5.QtCore import Qt

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.component_library import ComponentLibrary
from gui.theme import COLORS
from gui.toast import show_toast


class ComponentLibraryDialog(QDialog):
    """Component Library Manager Dialog"""
    
    def __init__(self, parent=None):
        """Initialize component library dialog"""
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.library = ComponentLibrary()
        self.current_component_type = 'engine'
        self.current_component = None
        
        self.init_ui()
        self.load_components()
        
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Component Library Manager")
        self.setGeometry(200, 200, 1000, 600)
        
        main_layout = QVBoxLayout()
        
        # Component type selector
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Component Type:"))
        
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            'Engine',
            'Suspension',
            'Differential',
            'Drivetrain',
            'Aero',
            'Tyres'
        ])
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        
        # Search box
        type_layout.addWidget(QLabel("Search:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by name, description, or tags...")
        self.search_box.textChanged.connect(self.filter_components)
        type_layout.addWidget(self.search_box)
        
        main_layout.addLayout(type_layout)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Component list
        left_panel = self.create_list_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Component details
        right_panel = self.create_details_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        # Import/Export buttons
        import_btn = QPushButton("Import Component...")
        import_btn.clicked.connect(self.import_component)
        button_layout.addWidget(import_btn)
        
        import_all_btn = QPushButton("Import Library...")
        import_all_btn.clicked.connect(self.import_library)
        button_layout.addWidget(import_all_btn)
        
        export_btn = QPushButton("Export Component...")
        export_btn.clicked.connect(self.export_component)
        button_layout.addWidget(export_btn)
        
        export_all_btn = QPushButton("Export All...")
        export_all_btn.clicked.connect(self.export_all)
        button_layout.addWidget(export_all_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def create_list_panel(self):
        """Create component list panel"""
        panel = QGroupBox("Components")
        layout = QVBoxLayout()
        
        # Component list
        self.component_list = QListWidget()
        self.component_list.currentItemChanged.connect(self.on_component_selected)
        layout.addWidget(self.component_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add New")
        add_btn.clicked.connect(self.add_component)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_component)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_component)
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
        panel.setLayout(layout)
        return panel
        
    def create_details_panel(self):
        """Create component details panel"""
        panel = QGroupBox("Component Details")
        layout = QVBoxLayout()
        
        # Component info
        info_layout = QFormLayout()
        
        self.name_label = QLabel("-")
        self.name_label.setStyleSheet(f"font-weight: bold; font-size: 14px; color: {COLORS['text']};")
        info_layout.addRow("Name:", self.name_label)
        
        self.id_label = QLabel("-")
        info_layout.addRow("ID:", self.id_label)
        
        self.tags_label = QLabel("-")
        info_layout.addRow("Tags:", self.tags_label)
        
        layout.addLayout(info_layout)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setMaximumHeight(80)
        layout.addWidget(self.description_text)
        
        # Component data
        layout.addWidget(QLabel("Component Data:"))
        self.data_text = QTextEdit()
        self.data_text.setReadOnly(True)
        self.data_text.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.data_text)
        
        # Apply button (for future integration)
        self.apply_btn = QPushButton("Apply to Car")
        self.apply_btn.clicked.connect(self.apply_component)
        self.apply_btn.setEnabled(False)  # Disabled for now
        layout.addWidget(self.apply_btn)
        
        panel.setLayout(layout)
        return panel
        
    def on_type_changed(self):
        """Handle component type change"""
        type_name = self.type_combo.currentText().lower()
        self.current_component_type = type_name
        self.load_components()
        
    def load_components(self):
        """Load components of current type"""
        self.component_list.clear()
        components = self.library.get_components(self.current_component_type)
        
        for component in components:
            item = QListWidgetItem(component.get('name', 'Unnamed'))
            item.setData(Qt.UserRole, component)
            self.component_list.addItem(item)
        
        # Update status
        if components:
            self.component_list.setCurrentRow(0)
        else:
            self.clear_details()
            
    def filter_components(self):
        """Filter components based on search text"""
        search_text = self.search_box.text().strip()
        
        if not search_text:
            self.load_components()
            return
        
        self.component_list.clear()
        components = self.library.search_components(self.current_component_type, search_text)
        
        for component in components:
            item = QListWidgetItem(component.get('name', 'Unnamed'))
            item.setData(Qt.UserRole, component)
            self.component_list.addItem(item)
            
    def on_component_selected(self, current, previous):
        """Handle component selection"""
        if current is None:
            self.clear_details()
            return
        
        component = current.data(Qt.UserRole)
        self.current_component = component
        
        # Update details
        self.name_label.setText(component.get('name', '-'))
        self.id_label.setText(component.get('id', '-'))
        
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
            self.data_text.setPlainText("No data")
            
    def clear_details(self):
        """Clear component details"""
        self.name_label.setText("-")
        self.id_label.setText("-")
        self.tags_label.setText("-")
        self.description_text.clear()
        self.data_text.clear()
        self.current_component = None
        
    def add_component(self):
        """Add new component"""
        dialog = ComponentEditorDialog(self.current_component_type, None, self)
        if dialog.exec_() == QDialog.Accepted:
            component = dialog.get_component()
            if self.library.add_component(self.current_component_type, component):
                self.load_components()
                show_toast(self, "✅  Component added successfully!", kind='success')
            else:
                QMessageBox.warning(self, "Error", "Failed to add component. Component ID may already exist.")
                
    def edit_component(self):
        """Edit selected component"""
        if not self.current_component:
            QMessageBox.warning(self, "No Selection", "Please select a component to edit.")
            return
        
        dialog = ComponentEditorDialog(self.current_component_type, self.current_component, self)
        if dialog.exec_() == QDialog.Accepted:
            component = dialog.get_component()
            component_id = self.current_component.get('id')
            if self.library.update_component(self.current_component_type, component_id, component):
                self.load_components()
                show_toast(self, "✅  Component updated successfully!", kind='success')
            else:
                QMessageBox.warning(self, "Error", "Failed to update component.")
                
    def delete_component(self):
        """Delete selected component"""
        if not self.current_component:
            QMessageBox.warning(self, "No Selection", "Please select a component to delete.")
            return
        
        component_name = self.current_component.get('name')
        component_id = self.current_component.get('id')
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the component '{component_name}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.library.delete_component(self.current_component_type, component_id):
                self.load_components()
                show_toast(self, "✅  Component deleted.", kind='success')
            else:
                QMessageBox.warning(self, "Error", "Failed to delete component.")
                
    def import_component(self):
        """Import component from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Component",
            "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            # Ask about overwriting
            reply = QMessageBox.question(
                self,
                "Overwrite Existing?",
                "If a component with the same ID exists, should it be overwritten?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            overwrite = (reply == QMessageBox.Yes)
            
            if self.library.import_component(file_path, overwrite):
                self.load_components()
                show_toast(self, "✅  Component imported successfully!", kind='success')
            else:
                QMessageBox.warning(self, "Error", "Failed to import component.")
                
    def import_library(self):
        """Import multiple components from library file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Component Library",
            "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            if self.library.import_components(file_path):
                self.load_components()
                show_toast(self, "✅  Components imported successfully!", kind='success')
            else:
                QMessageBox.warning(self, "Error", "Failed to import components.")
                
    def export_component(self):
        """Export selected component to file"""
        if not self.current_component:
            QMessageBox.warning(self, "No Selection", "Please select a component to export.")
            return
        
        component_id = self.current_component.get('id')
        default_name = f"{component_id}.json"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Component",
            default_name,
            "JSON Files (*.json)"
        )
        
        if file_path:
            if self.library.export_component(self.current_component_type, component_id, file_path):
                show_toast(self, f"✅  Component exported to: {file_path}", kind='success')
            else:
                QMessageBox.warning(self, "Error", "Failed to export component.")
                
    def export_all(self):
        """Export all components to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export All Components",
            "component_library.json",
            "JSON Files (*.json)"
        )
        
        if file_path:
            if self.library.export_all_components(file_path):
                show_toast(self, f"✅  All components exported to: {file_path}", kind='success')
            else:
                QMessageBox.warning(self, "Error", "Failed to export components.")
                
    def apply_component(self):
        """Apply component to current car (placeholder)"""
        QMessageBox.information(
            self,
            "Coming Soon",
            "Applying components to cars will be implemented in a future update.\n\n"
            "You will be able to select a car and apply the component data directly."
        )


class ComponentEditorDialog(QDialog):
    """Dialog for adding/editing components"""
    
    def __init__(self, component_type, component=None, parent=None):
        """
        Initialize component editor
        
        Args:
            component_type: Type of component
            component: Existing component to edit (None for new)
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.component_type = component_type
        self.component = component or {}
        
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        """Initialize user interface"""
        title = "Edit Component" if self.component else "Add New Component"
        self.setWindowTitle(title)
        self.setGeometry(300, 300, 600, 500)
        
        layout = QVBoxLayout()
        
        # Form fields
        form_layout = QFormLayout()
        
        self.id_edit = QLineEdit()
        self.id_edit.setPlaceholderText("unique_component_id")
        form_layout.addRow("ID*:", self.id_edit)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Component Display Name")
        form_layout.addRow("Name*:", self.name_edit)
        
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("tag1, tag2, tag3")
        form_layout.addRow("Tags:", self.tags_edit)
        
        layout.addLayout(form_layout)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        layout.addWidget(self.description_edit)
        
        # Component data
        layout.addWidget(QLabel("Component Data (key=value, one per line):"))
        self.data_edit = QTextEdit()
        self.data_edit.setPlaceholderText("MINIMUM=1000\nLIMITER=8000\nINERTIA=0.15")
        self.data_edit.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.data_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def load_data(self):
        """Load component data into form"""
        if not self.component:
            return
        
        self.id_edit.setText(self.component.get('id', ''))
        self.id_edit.setEnabled(False)  # Don't allow changing ID when editing
        
        self.name_edit.setText(self.component.get('name', ''))
        
        tags = self.component.get('tags', [])
        self.tags_edit.setText(', '.join(tags))
        
        self.description_edit.setPlainText(self.component.get('description', ''))
        
        # Format data
        data = self.component.get('data', {})
        if data:
            data_lines = []
            for key, value in data.items():
                data_lines.append(f"{key}={value}")
            self.data_edit.setPlainText('\n'.join(data_lines))
            
    def save(self):
        """Validate and save component"""
        # Validate required fields
        component_id = self.id_edit.text().strip()
        name = self.name_edit.text().strip()
        
        if not component_id or not name:
            QMessageBox.warning(self, "Validation Error", "ID and Name are required fields.")
            return
        
        # Parse tags
        tags_text = self.tags_edit.text().strip()
        tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
        
        # Parse data
        data = {}
        data_text = self.data_edit.toPlainText().strip()
        if data_text:
            for line in data_text.split('\n'):
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Try to convert to number
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass  # Keep as string
                    
                    data[key] = value
        
        # Build component
        self.component = {
            'id': component_id,
            'name': name,
            'description': self.description_edit.toPlainText().strip(),
            'tags': tags,
            'data': data
        }
        
        self.accept()
        
    def get_component(self):
        """Get the component data"""
        return self.component
