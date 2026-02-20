"""
UI Editor Dialog - Edit ui_car.json metadata for AC cars
"""

import sys
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QMessageBox, QGroupBox, QLineEdit,
    QSpinBox, QTextEdit, QLabel, QComboBox
)
from PyQt5.QtCore import Qt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.ui_manager import UIManager
from gui.theme import COLORS, btn_primary
from gui.toast import show_toast
from gui.segmented_button import SegmentedButtonGroup


class UIEditorDialog(QDialog):
    """Dialog for editing ui_car.json metadata"""
    
    def __init__(self, car_name, car_path, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.car_name = car_name
        self.car_path = car_path
        self.ui_manager = UIManager(car_path)
        
        # Create default if doesn't exist
        if not self.ui_manager.has_ui_car_json():
            self.ui_manager.create_default_ui_car_json(car_name)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(f"Edit UI Metadata: {self.car_name}")
        self.setGeometry(200, 150, 600, 650)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Basic info group
        basic_group = QGroupBox("Basic Information")
        basic_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setToolTip("Display name shown in AC car selection menu")
        basic_layout.addRow("Car Name:", self.name_edit)
        
        self.brand_edit = QLineEdit()
        self.brand_edit.setToolTip("Car brand/manufacturer (e.g., 'Ferrari', 'Porsche')")
        basic_layout.addRow("Brand:", self.brand_edit)
        
        self.class_combo = SegmentedButtonGroup(['street', 'race', 'drift', 'vintage', 'concept'])
        self.class_combo.setToolTip("Car class category")
        basic_layout.addRow("Class:", self.class_combo)
        
        self.country_edit = QLineEdit()
        self.country_edit.setToolTip("Country of origin (e.g., 'Italy', 'Germany', 'Japan')")
        basic_layout.addRow("Country:", self.country_edit)
        
        self.year_spin = QSpinBox()
        self.year_spin.setRange(1900, 2100)
        self.year_spin.setValue(2000)
        self.year_spin.setToolTip("Year of production")
        basic_layout.addRow("Year:", self.year_spin)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Description group
        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout()
        
        self.description_edit = QTextEdit()
        self.description_edit.setToolTip("Car description shown in AC menu (supports HTML tags like <br>)")
        self.description_edit.setMaximumHeight(80)
        desc_layout.addWidget(self.description_edit)
        
        desc_group.setLayout(desc_layout)
        layout.addWidget(desc_group)
        
        # Tags group
        tags_group = QGroupBox("Tags")
        tags_layout = QVBoxLayout()
        
        tag_label = QLabel("Comma-separated tags (e.g., 'turbo, fwd, manual, street')")
        tags_layout.addWidget(tag_label)
        
        self.tags_edit = QLineEdit()
        self.tags_edit.setToolTip("Comma-separated list of tags for filtering/search")
        tags_layout.addWidget(self.tags_edit)
        
        tags_group.setLayout(tags_layout)
        layout.addWidget(tags_group)
        
        # Specs group
        specs_group = QGroupBox("Specifications")
        specs_layout = QFormLayout()
        
        self.bhp_edit = QLineEdit()
        self.bhp_edit.setToolTip("Power specification (e.g., '180 bhp')")
        specs_layout.addRow("Power:", self.bhp_edit)
        
        self.torque_edit = QLineEdit()
        self.torque_edit.setToolTip("Torque specification (e.g., '320 Nm')")
        specs_layout.addRow("Torque:", self.torque_edit)
        
        self.weight_edit = QLineEdit()
        self.weight_edit.setToolTip("Weight specification (e.g., '1425 kg')")
        specs_layout.addRow("Weight:", self.weight_edit)
        
        self.topspeed_edit = QLineEdit()
        self.topspeed_edit.setToolTip("Top speed specification (e.g., '236 km/h')")
        specs_layout.addRow("Top Speed:", self.topspeed_edit)
        
        self.acceleration_edit = QLineEdit()
        self.acceleration_edit.setToolTip("0-100 km/h acceleration (e.g., '7.8s 0-100')")
        specs_layout.addRow("0-100:", self.acceleration_edit)
        
        self.pwratio_edit = QLineEdit()
        self.pwratio_edit.setToolTip("Power to weight ratio (e.g., '8.33 kg/hp')")
        specs_layout.addRow("Power/Weight:", self.pwratio_edit)
        
        specs_group.setLayout(specs_layout)
        layout.addWidget(specs_group)
        
        # Author info group
        author_group = QGroupBox("Author Information")
        author_layout = QFormLayout()
        
        self.author_edit = QLineEdit()
        self.author_edit.setToolTip("Mod author name")
        author_layout.addRow("Author:", self.author_edit)
        
        self.version_edit = QLineEdit()
        self.version_edit.setToolTip("Mod version (e.g., '1.0', '2.5 Beta')")
        author_layout.addRow("Version:", self.version_edit)
        
        author_group.setLayout(author_layout)
        layout.addWidget(author_group)
        
        # Button bar
        btn_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾  Save")
        self.save_btn.setStyleSheet(btn_primary())
        self.save_btn.clicked.connect(self.save_changes)
        btn_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def load_data(self):
        """Load data from UI manager into widgets"""
        self.name_edit.setText(self.ui_manager.get_name())
        self.brand_edit.setText(self.ui_manager.get_brand())
        
        car_class = self.ui_manager.get_class()
        index = self.class_combo.findText(car_class)
        if index >= 0:
            self.class_combo.setCurrentIndex(index)
        
        self.country_edit.setText(self.ui_manager.get_country())
        self.year_spin.setValue(self.ui_manager.get_year() or 2000)
        self.description_edit.setPlainText(self.ui_manager.get_description())
        
        tags = self.ui_manager.get_tags()
        self.tags_edit.setText(', '.join(tags))
        
        specs = self.ui_manager.get_specs()
        self.bhp_edit.setText(specs.get('bhp', ''))
        self.torque_edit.setText(specs.get('torque', ''))
        self.weight_edit.setText(specs.get('weight', ''))
        self.topspeed_edit.setText(specs.get('topspeed', ''))
        self.acceleration_edit.setText(specs.get('acceleration', ''))
        self.pwratio_edit.setText(specs.get('pwratio', ''))
        
        self.author_edit.setText(self.ui_manager.get_author())
        self.version_edit.setText(self.ui_manager.get_version())
    
    def save_changes(self):
        """Save changes to ui_car.json"""
        try:
            # Update UI manager with values from widgets
            self.ui_manager.set_name(self.name_edit.text())
            self.ui_manager.set_brand(self.brand_edit.text())
            self.ui_manager.set_class(self.class_combo.currentText())
            self.ui_manager.set_country(self.country_edit.text())
            self.ui_manager.set_year(self.year_spin.value())
            self.ui_manager.set_description(self.description_edit.toPlainText())
            
            # Parse tags
            tags_text = self.tags_edit.text()
            tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
            self.ui_manager.set_tags(tags)
            
            # Update specs
            specs = {
                'bhp': self.bhp_edit.text(),
                'torque': self.torque_edit.text(),
                'weight': self.weight_edit.text(),
                'topspeed': self.topspeed_edit.text(),
                'acceleration': self.acceleration_edit.text(),
                'pwratio': self.pwratio_edit.text(),
            }
            self.ui_manager.set_specs(specs)
            
            self.ui_manager.set_author(self.author_edit.text())
            self.ui_manager.set_version(self.version_edit.text())
            
            # Save to file
            if self.ui_manager.save(backup=True):
                show_toast(self.parent() if self.parent() else self,
                           "✅  UI metadata saved successfully!", kind='success')
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Failed to save UI metadata."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error saving UI metadata: {e}"
            )
