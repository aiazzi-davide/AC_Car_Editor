"""
Car Editor Dialog - Main editor window for modifying car parameters
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QMessageBox, QWidget, QGroupBox,
    QFormLayout, QLineEdit, QLabel, QDoubleSpinBox,
    QSpinBox
)
from PyQt5.QtCore import Qt

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.ini_parser import IniParser
from core.lut_parser import LUTCurve


class CarEditorDialog(QDialog):
    """Dialog for editing car parameters"""
    
    def __init__(self, car_name, car_data_path, parent=None):
        """
        Initialize car editor dialog
        
        Args:
            car_name: Name of the car
            car_data_path: Path to car's data folder
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.car_name = car_name
        self.car_data_path = car_data_path
        
        # Store original values for reset
        self.original_values = {}
        
        # Initialize parsers
        self.engine_ini = None
        self.init_parsers()
        
        self.init_ui()
        self.load_data()
        
    def init_parsers(self):
        """Initialize INI and LUT parsers for car files"""
        engine_path = os.path.join(self.car_data_path, 'engine.ini')
        if os.path.exists(engine_path):
            self.engine_ini = IniParser(engine_path)
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(f"Edit Car: {self.car_name}")
        self.setGeometry(150, 150, 800, 600)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.engine_tab = self.create_engine_tab()
        self.tabs.addTab(self.engine_tab, "Engine")
        
        # TODO: Add more tabs in future (Suspension, Differential, etc.)
        
        layout.addWidget(self.tabs)
        
        # Button bar
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_changes)
        button_layout.addWidget(self.save_btn)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_values)
        button_layout.addWidget(self.reset_btn)
        
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
    def create_engine_tab(self):
        """Create engine parameters tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Basic engine data group
        basic_group = QGroupBox("Basic Engine Data")
        basic_layout = QFormLayout()
        
        # MINIMUM RPM
        self.minimum_rpm = QSpinBox()
        self.minimum_rpm.setRange(0, 20000)
        self.minimum_rpm.setSuffix(" RPM")
        basic_layout.addRow("Minimum RPM:", self.minimum_rpm)
        
        # MAXIMUM RPM
        self.maximum_rpm = QSpinBox()
        self.maximum_rpm.setRange(0, 20000)
        self.maximum_rpm.setSuffix(" RPM")
        basic_layout.addRow("Maximum RPM:", self.maximum_rpm)
        
        # LIMITER RPM
        self.limiter_rpm = QSpinBox()
        self.limiter_rpm.setRange(0, 20000)
        self.limiter_rpm.setSuffix(" RPM")
        basic_layout.addRow("Limiter RPM:", self.limiter_rpm)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Turbo group (if applicable)
        turbo_group = QGroupBox("Turbo")
        turbo_layout = QFormLayout()
        
        # MAX_BOOST
        self.max_boost = QDoubleSpinBox()
        self.max_boost.setRange(0, 5.0)
        self.max_boost.setDecimals(2)
        self.max_boost.setSingleStep(0.1)
        self.max_boost.setSuffix(" bar")
        turbo_layout.addRow("Max Boost:", self.max_boost)
        
        # WASTEGATE
        self.wastegate = QDoubleSpinBox()
        self.wastegate.setRange(0, 5.0)
        self.wastegate.setDecimals(2)
        self.wastegate.setSingleStep(0.1)
        self.wastegate.setSuffix(" bar")
        turbo_layout.addRow("Wastegate:", self.wastegate)
        
        turbo_group.setLayout(turbo_layout)
        layout.addWidget(turbo_group)
        
        layout.addStretch()
        
        return widget
        
    def load_data(self):
        """Load car data into UI fields"""
        if not self.engine_ini:
            return
        
        # Load engine data
        if self.engine_ini.has_section('ENGINE_DATA'):
            minimum = self.engine_ini.get_value('ENGINE_DATA', 'MINIMUM', '1000')
            maximum = self.engine_ini.get_value('ENGINE_DATA', 'MAXIMUM', '7000')
            limiter = self.engine_ini.get_value('ENGINE_DATA', 'LIMITER', '7500')
            
            self.minimum_rpm.setValue(int(minimum))
            self.maximum_rpm.setValue(int(maximum))
            self.limiter_rpm.setValue(int(limiter))
            
            # Store original values
            self.original_values['minimum'] = int(minimum)
            self.original_values['maximum'] = int(maximum)
            self.original_values['limiter'] = int(limiter)
        
        # Load turbo data if exists
        if self.engine_ini.has_section('TURBO_0'):
            max_boost = self.engine_ini.get_value('TURBO_0', 'MAX_BOOST', '0.0')
            wastegate = self.engine_ini.get_value('TURBO_0', 'WASTEGATE', '0.0')
            
            self.max_boost.setValue(float(max_boost))
            self.wastegate.setValue(float(wastegate))
            
            self.original_values['max_boost'] = float(max_boost)
            self.original_values['wastegate'] = float(wastegate)
    
    def save_changes(self):
        """Save changes to car files"""
        if not self.engine_ini:
            QMessageBox.warning(self, "Error", "No engine.ini file found")
            return
        
        try:
            # Save engine data
            self.engine_ini.set_value('ENGINE_DATA', 'MINIMUM', str(self.minimum_rpm.value()))
            self.engine_ini.set_value('ENGINE_DATA', 'MAXIMUM', str(self.maximum_rpm.value()))
            self.engine_ini.set_value('ENGINE_DATA', 'LIMITER', str(self.limiter_rpm.value()))
            
            # Save turbo data if section exists
            if self.engine_ini.has_section('TURBO_0'):
                self.engine_ini.set_value('TURBO_0', 'MAX_BOOST', str(self.max_boost.value()))
                self.engine_ini.set_value('TURBO_0', 'WASTEGATE', str(self.wastegate.value()))
            
            # Save to file with backup
            self.engine_ini.save(backup=True)
            
            QMessageBox.information(
                self,
                "Success",
                "Changes saved successfully!\n\n"
                "A backup of the original file was created with .bak extension."
            )
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving",
                f"Failed to save changes:\n{str(e)}"
            )
    
    def reset_values(self):
        """Reset all values to original"""
        if 'minimum' in self.original_values:
            self.minimum_rpm.setValue(self.original_values['minimum'])
            self.maximum_rpm.setValue(self.original_values['maximum'])
            self.limiter_rpm.setValue(self.original_values['limiter'])
        
        if 'max_boost' in self.original_values:
            self.max_boost.setValue(self.original_values['max_boost'])
            self.wastegate.setValue(self.original_values['wastegate'])
