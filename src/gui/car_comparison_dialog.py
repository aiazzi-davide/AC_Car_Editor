"""
Car Comparison Dialog for comparing two cars side-by-side
"""

import sys
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QGroupBox, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.ini_parser import IniParser


class CarComparisonDialog(QDialog):
    """Dialog for comparing two cars side-by-side"""
    
    def __init__(self, car_manager, parent=None):
        """
        Initialize comparison dialog
        
        Args:
            car_manager: CarFileManager instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.car_manager = car_manager
        self.car_list = car_manager.get_car_list()
        
        # Filter cars that have data folder or data.acd
        self.available_cars = []
        for car in self.car_list:
            info = car_manager.get_car_info(car)
            if info['has_data_folder'] or info['has_data_acd']:
                self.available_cars.append(car)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Compare Cars")
        self.setGeometry(100, 100, 1000, 700)
        
        layout = QVBoxLayout()
        
        # Car selection section
        selection_layout = QHBoxLayout()
        
        # Car 1 selection
        car1_group = QGroupBox("Car 1")
        car1_layout = QVBoxLayout()
        self.car1_combo = QComboBox()
        self.car1_combo.addItems(self.available_cars)
        self.car1_combo.currentTextChanged.connect(self.update_comparison)
        car1_layout.addWidget(self.car1_combo)
        
        # Preview for car 1
        self.car1_preview = QLabel()
        self.car1_preview.setAlignment(Qt.AlignCenter)
        self.car1_preview.setMaximumHeight(150)
        self.car1_preview.setText("No preview")
        self.car1_preview.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        car1_layout.addWidget(self.car1_preview)
        
        self.car1_name_label = QLabel()
        self.car1_name_label.setStyleSheet("font-weight: bold;")
        car1_layout.addWidget(self.car1_name_label)
        
        car1_group.setLayout(car1_layout)
        selection_layout.addWidget(car1_group)
        
        # Car 2 selection
        car2_group = QGroupBox("Car 2")
        car2_layout = QVBoxLayout()
        self.car2_combo = QComboBox()
        self.car2_combo.addItems(self.available_cars)
        if len(self.available_cars) > 1:
            self.car2_combo.setCurrentIndex(1)
        self.car2_combo.currentTextChanged.connect(self.update_comparison)
        car2_layout.addWidget(self.car2_combo)
        
        # Preview for car 2
        self.car2_preview = QLabel()
        self.car2_preview.setAlignment(Qt.AlignCenter)
        self.car2_preview.setMaximumHeight(150)
        self.car2_preview.setText("No preview")
        self.car2_preview.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        car2_layout.addWidget(self.car2_preview)
        
        self.car2_name_label = QLabel()
        self.car2_name_label.setStyleSheet("font-weight: bold;")
        car2_layout.addWidget(self.car2_name_label)
        
        car2_group.setLayout(car2_layout)
        selection_layout.addWidget(car2_group)
        
        layout.addLayout(selection_layout)
        
        # Comparison table
        self.comparison_table = QTableWidget()
        self.comparison_table.setColumnCount(3)
        self.comparison_table.setHorizontalHeaderLabels(["Specification", "Car 1", "Car 2"])
        
        # Set column widths
        header = self.comparison_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        layout.addWidget(self.comparison_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Initial comparison
        if len(self.available_cars) >= 2:
            self.update_comparison()
    
    def update_car_preview(self, car_name, preview_label, name_label):
        """
        Update preview image for a car
        
        Args:
            car_name: Name of the car
            preview_label: QLabel to display preview
            name_label: QLabel to display car name
        """
        car_info = self.car_manager.get_car_info(car_name)
        name_label.setText(car_info.get('display_name', car_name))
        
        preview_path = car_info.get('preview_path')
        if preview_path and os.path.exists(preview_path):
            pixmap = QPixmap(preview_path)
            scaled_pixmap = pixmap.scaled(
                preview_label.width() - 10,
                preview_label.maximumHeight() - 10,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            preview_label.setPixmap(scaled_pixmap)
        else:
            preview_label.clear()
            preview_label.setText("No preview")
    
    def update_comparison(self):
        """Update comparison table with selected cars"""
        car1_name = self.car1_combo.currentText()
        car2_name = self.car2_combo.currentText()
        
        if not car1_name or not car2_name:
            return
        
        # Update previews
        self.update_car_preview(car1_name, self.car1_preview, self.car1_name_label)
        self.update_car_preview(car2_name, self.car2_preview, self.car2_name_label)
        
        # Get car specs
        car1_specs = self.get_car_specs(car1_name)
        car2_specs = self.get_car_specs(car2_name)
        
        # Populate comparison table
        self.populate_comparison_table(car1_specs, car2_specs)
    
    def get_car_specs(self, car_name):
        """
        Extract key specifications from car data
        
        Args:
            car_name: Car folder name
            
        Returns:
            Dictionary of specifications
        """
        specs = {}
        
        try:
            # Engine specs
            engine_path = self.car_manager.get_ini_file_path(car_name, 'engine.ini')
            if os.path.exists(engine_path):
                engine_parser = IniParser(engine_path)
                
                # Get power curve max (approximate HP)
                power_lut_path = os.path.join(
                    self.car_manager.get_car_data_path(car_name),
                    'power.lut'
                )
                if os.path.exists(power_lut_path):
                    try:
                        with open(power_lut_path, 'r') as f:
                            max_power = 0
                            for line in f:
                                line = line.split('#')[0].split(';')[0].strip()
                                if '|' in line:
                                    parts = line.split('|')
                                    if len(parts) == 2:
                                        power = float(parts[1])
                                        max_power = max(max_power, power)
                            specs['Max Power (HP)'] = f"{int(max_power)}"
                    except:
                        pass
                
                specs['Limiter (RPM)'] = engine_parser.get_value('ENGINE_DATA', 'LIMITER', 'N/A')
                specs['Inertia'] = engine_parser.get_value('ENGINE_DATA', 'INERTIA', 'N/A')
                
            # Car specs (weight, distribution)
            car_path = self.car_manager.get_ini_file_path(car_name, 'car.ini')
            if os.path.exists(car_path):
                car_parser = IniParser(car_path)
                specs['Total Mass (kg)'] = car_parser.get_value('BASIC', 'TOTALMASS', 'N/A')
                specs['Weight Distribution'] = car_parser.get_value('BASIC', 'WEIGHTDISTRIBUTION', 'N/A')
                specs['Screen Name'] = car_parser.get_value('BASIC', 'SCREEN_NAME', 'N/A')
            
            # Suspension specs
            susp_path = self.car_manager.get_ini_file_path(car_name, 'suspensions.ini')
            if os.path.exists(susp_path):
                susp_parser = IniParser(susp_path)
                specs['Wheelbase (m)'] = susp_parser.get_value('BASIC', 'WHEELBASE', 'N/A')
                specs['Front Track (m)'] = susp_parser.get_value('FRONT', 'TRACK', 'N/A')
                specs['Rear Track (m)'] = susp_parser.get_value('REAR', 'TRACK', 'N/A')
            
            # Drivetrain
            dt_path = self.car_manager.get_ini_file_path(car_name, 'drivetrain.ini')
            if os.path.exists(dt_path):
                dt_parser = IniParser(dt_path)
                specs['Traction Type'] = dt_parser.get_value('TRACTION', 'TYPE', 'N/A')
                specs['Final Ratio'] = dt_parser.get_value('GEARS', 'FINAL', 'N/A')
            
            # Aero
            aero_path = self.car_manager.get_ini_file_path(car_name, 'aero.ini')
            if os.path.exists(aero_path):
                aero_parser = IniParser(aero_path)
                specs['Drag Coefficient'] = aero_parser.get_value('DATA', 'CD', 'N/A')
                specs['Frontal Area (m²)'] = aero_parser.get_value('DATA', 'CL_FRONT', 'N/A')
            
            # Brakes
            brakes_path = self.car_manager.get_ini_file_path(car_name, 'brakes.ini')
            if os.path.exists(brakes_path):
                brakes_parser = IniParser(brakes_path)
                specs['Front Brake Bias'] = brakes_parser.get_value('DATA', 'FRONT_SHARE', 'N/A')
                specs['Max Torque (Nm)'] = brakes_parser.get_value('DATA', 'MAX_TORQUE', 'N/A')
                
        except Exception as e:
            print(f"Error getting specs for {car_name}: {e}")
        
        return specs
    
    def populate_comparison_table(self, car1_specs, car2_specs):
        """
        Populate comparison table with car specifications
        
        Args:
            car1_specs: Specifications for car 1
            car2_specs: Specifications for car 2
        """
        # Get all unique spec keys
        all_keys = set(car1_specs.keys()) | set(car2_specs.keys())
        sorted_keys = sorted(all_keys)
        
        self.comparison_table.setRowCount(len(sorted_keys))
        
        for row, key in enumerate(sorted_keys):
            # Specification name
            spec_item = QTableWidgetItem(key)
            spec_item.setFlags(spec_item.flags() & ~Qt.ItemIsEditable)
            self.comparison_table.setItem(row, 0, spec_item)
            
            # Car 1 value
            car1_value = car1_specs.get(key, 'N/A')
            car1_item = QTableWidgetItem(str(car1_value))
            car1_item.setFlags(car1_item.flags() & ~Qt.ItemIsEditable)
            self.comparison_table.setItem(row, 1, car1_item)
            
            # Car 2 value
            car2_value = car2_specs.get(key, 'N/A')
            car2_item = QTableWidgetItem(str(car2_value))
            car2_item.setFlags(car2_item.flags() & ~Qt.ItemIsEditable)
            self.comparison_table.setItem(row, 2, car2_item)
            
            # Highlight differences
            if car1_value != car2_value:
                try:
                    # Try to compare numerically
                    val1 = float(car1_value) if car1_value != 'N/A' else None
                    val2 = float(car2_value) if car2_value != 'N/A' else None
                    
                    if val1 is not None and val2 is not None:
                        if val1 > val2:
                            car1_item.setBackground(Qt.green)
                            car2_item.setBackground(Qt.yellow)
                        elif val1 < val2:
                            car1_item.setBackground(Qt.yellow)
                            car2_item.setBackground(Qt.green)
                except:
                    # If not numeric, just mark as different with light gray
                    car1_item.setBackground(Qt.lightGray)
                    car2_item.setBackground(Qt.lightGray)
