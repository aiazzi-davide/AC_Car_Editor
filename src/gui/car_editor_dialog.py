"""
Car Editor Dialog - Main editor window for modifying car parameters
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QMessageBox, QWidget, QGroupBox,
    QFormLayout, QLineEdit, QLabel, QDoubleSpinBox,
    QSpinBox, QComboBox
)
from PyQt5.QtCore import Qt

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.ini_parser import IniParser
from core.lut_parser import LUTCurve
from gui.curve_editor_dialog import CurveEditorDialog


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
        self.suspension_ini = None
        self.drivetrain_ini = None
        self.car_ini = None
        self.aero_ini = None
        self.init_parsers()
        
        self.init_ui()
        self.load_data()
        
    def init_parsers(self):
        """Initialize INI and LUT parsers for car files"""
        engine_path = os.path.join(self.car_data_path, 'engine.ini')
        if os.path.exists(engine_path):
            try:
                self.engine_ini = IniParser(engine_path)
            except Exception as e:
                print(f"Failed to load engine.ini: {e}")
                self.engine_ini = None
        
        suspension_path = os.path.join(self.car_data_path, 'suspensions.ini')
        if os.path.exists(suspension_path):
            try:
                self.suspension_ini = IniParser(suspension_path)
            except Exception as e:
                print(f"Failed to load suspensions.ini: {e}")
                self.suspension_ini = None
        
        drivetrain_path = os.path.join(self.car_data_path, 'drivetrain.ini')
        if os.path.exists(drivetrain_path):
            try:
                self.drivetrain_ini = IniParser(drivetrain_path)
            except Exception as e:
                print(f"Failed to load drivetrain.ini: {e}")
                self.drivetrain_ini = None
        
        car_path = os.path.join(self.car_data_path, 'car.ini')
        if os.path.exists(car_path):
            try:
                self.car_ini = IniParser(car_path)
            except Exception as e:
                print(f"Failed to load car.ini: {e}")
                self.car_ini = None
        
        aero_path = os.path.join(self.car_data_path, 'aero.ini')
        if os.path.exists(aero_path):
            try:
                self.aero_ini = IniParser(aero_path)
            except Exception as e:
                print(f"Failed to load aero.ini: {e}")
                self.aero_ini = None
    
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
        
        self.suspension_tab = self.create_suspension_tab()
        self.tabs.addTab(self.suspension_tab, "Suspension")
        
        self.differential_tab = self.create_differential_tab()
        self.tabs.addTab(self.differential_tab, "Differential")
        
        self.weight_tab = self.create_weight_tab()
        self.tabs.addTab(self.weight_tab, "Weight")
        
        self.aero_tab = self.create_aero_tab()
        self.tabs.addTab(self.aero_tab, "Aerodynamics")
        
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
        
        # Curve editor group
        curve_group = QGroupBox("Power and Coast Curves")
        curve_layout = QVBoxLayout()
        
        # Power curve button
        power_curve_btn = QPushButton("Edit Power Curve (power.lut)")
        power_curve_btn.clicked.connect(self.edit_power_curve)
        curve_layout.addWidget(power_curve_btn)
        
        # Coast curve button
        coast_curve_btn = QPushButton("Edit Coast Curve (coast.lut)")
        coast_curve_btn.clicked.connect(self.edit_coast_curve)
        curve_layout.addWidget(coast_curve_btn)
        
        curve_group.setLayout(curve_layout)
        layout.addWidget(curve_group)
        
        layout.addStretch()
        
        return widget
    
    def create_suspension_tab(self):
        """Create suspension parameters tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Front suspension group
        front_group = QGroupBox("Front Suspension")
        front_layout = QFormLayout()
        
        # Front spring rate
        self.front_spring_rate = QDoubleSpinBox()
        self.front_spring_rate.setRange(0, 300000)
        self.front_spring_rate.setSuffix(" N/m")
        self.front_spring_rate.setDecimals(0)
        front_layout.addRow("Spring Rate:", self.front_spring_rate)
        
        # Front damper fast bump
        self.front_damper_fast_bump = QDoubleSpinBox()
        self.front_damper_fast_bump.setRange(0, 20000)
        self.front_damper_fast_bump.setSuffix(" N/(m/s)")
        self.front_damper_fast_bump.setDecimals(0)
        front_layout.addRow("Damper Fast Bump:", self.front_damper_fast_bump)
        
        # Front damper fast rebound
        self.front_damper_fast_rebound = QDoubleSpinBox()
        self.front_damper_fast_rebound.setRange(0, 20000)
        self.front_damper_fast_rebound.setSuffix(" N/(m/s)")
        self.front_damper_fast_rebound.setDecimals(0)
        front_layout.addRow("Damper Fast Rebound:", self.front_damper_fast_rebound)
        
        # Front damper slow bump
        self.front_damper_slow_bump = QDoubleSpinBox()
        self.front_damper_slow_bump.setRange(0, 20000)
        self.front_damper_slow_bump.setSuffix(" N/(m/s)")
        self.front_damper_slow_bump.setDecimals(0)
        front_layout.addRow("Damper Slow Bump:", self.front_damper_slow_bump)
        
        # Front damper slow rebound
        self.front_damper_slow_rebound = QDoubleSpinBox()
        self.front_damper_slow_rebound.setRange(0, 20000)
        self.front_damper_slow_rebound.setSuffix(" N/(m/s)")
        self.front_damper_slow_rebound.setDecimals(0)
        front_layout.addRow("Damper Slow Rebound:", self.front_damper_slow_rebound)
        
        # Front rod length
        self.front_rod_length = QDoubleSpinBox()
        self.front_rod_length.setRange(0, 1.0)
        self.front_rod_length.setSuffix(" m")
        self.front_rod_length.setDecimals(3)
        self.front_rod_length.setSingleStep(0.001)
        front_layout.addRow("Rod Length:", self.front_rod_length)
        
        front_group.setLayout(front_layout)
        layout.addWidget(front_group)
        
        # Rear suspension group
        rear_group = QGroupBox("Rear Suspension")
        rear_layout = QFormLayout()
        
        # Rear spring rate
        self.rear_spring_rate = QDoubleSpinBox()
        self.rear_spring_rate.setRange(0, 300000)
        self.rear_spring_rate.setSuffix(" N/m")
        self.rear_spring_rate.setDecimals(0)
        rear_layout.addRow("Spring Rate:", self.rear_spring_rate)
        
        # Rear damper fast bump
        self.rear_damper_fast_bump = QDoubleSpinBox()
        self.rear_damper_fast_bump.setRange(0, 20000)
        self.rear_damper_fast_bump.setSuffix(" N/(m/s)")
        self.rear_damper_fast_bump.setDecimals(0)
        rear_layout.addRow("Damper Fast Bump:", self.rear_damper_fast_bump)
        
        # Rear damper fast rebound
        self.rear_damper_fast_rebound = QDoubleSpinBox()
        self.rear_damper_fast_rebound.setRange(0, 20000)
        self.rear_damper_fast_rebound.setSuffix(" N/(m/s)")
        self.rear_damper_fast_rebound.setDecimals(0)
        rear_layout.addRow("Damper Fast Rebound:", self.rear_damper_fast_rebound)
        
        # Rear damper slow bump
        self.rear_damper_slow_bump = QDoubleSpinBox()
        self.rear_damper_slow_bump.setRange(0, 20000)
        self.rear_damper_slow_bump.setSuffix(" N/(m/s)")
        self.rear_damper_slow_bump.setDecimals(0)
        rear_layout.addRow("Damper Slow Bump:", self.rear_damper_slow_bump)
        
        # Rear damper slow rebound
        self.rear_damper_slow_rebound = QDoubleSpinBox()
        self.rear_damper_slow_rebound.setRange(0, 20000)
        self.rear_damper_slow_rebound.setSuffix(" N/(m/s)")
        self.rear_damper_slow_rebound.setDecimals(0)
        rear_layout.addRow("Damper Slow Rebound:", self.rear_damper_slow_rebound)
        
        # Rear rod length
        self.rear_rod_length = QDoubleSpinBox()
        self.rear_rod_length.setRange(0, 1.0)
        self.rear_rod_length.setSuffix(" m")
        self.rear_rod_length.setDecimals(3)
        self.rear_rod_length.setSingleStep(0.001)
        rear_layout.addRow("Rod Length:", self.rear_rod_length)
        
        rear_group.setLayout(rear_layout)
        layout.addWidget(rear_group)
        
        layout.addStretch()
        
        return widget
    
    def create_differential_tab(self):
        """Create differential parameters tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Traction type group
        traction_group = QGroupBox("Traction")
        traction_layout = QFormLayout()
        
        # Traction type (editable combo box)
        self.traction_type = QComboBox()
        self.traction_type.addItems(["RWD", "FWD", "AWD"])
        traction_layout.addRow("Type:", self.traction_type)
        
        traction_group.setLayout(traction_layout)
        layout.addWidget(traction_group)
        
        # Differential group
        diff_group = QGroupBox("Differential Settings")
        diff_layout = QFormLayout()
        
        # Differential type (editable combo box)
        self.diff_type = QComboBox()
        self.diff_type.addItems(["LSD", "SPOOL", "VISCOUS"])
        diff_layout.addRow("Type:", self.diff_type)
        
        # Power setting
        self.diff_power = QDoubleSpinBox()
        self.diff_power.setRange(0, 1.0)
        self.diff_power.setDecimals(2)
        self.diff_power.setSingleStep(0.05)
        diff_layout.addRow("Power:", self.diff_power)
        
        # Coast setting
        self.diff_coast = QDoubleSpinBox()
        self.diff_coast.setRange(0, 1.0)
        self.diff_coast.setDecimals(2)
        self.diff_coast.setSingleStep(0.05)
        diff_layout.addRow("Coast:", self.diff_coast)
        
        # Preload setting
        self.diff_preload = QDoubleSpinBox()
        self.diff_preload.setRange(0, 500)
        self.diff_preload.setSuffix(" Nm")
        self.diff_preload.setDecimals(0)
        diff_layout.addRow("Preload:", self.diff_preload)
        
        diff_group.setLayout(diff_layout)
        layout.addWidget(diff_group)
        
        layout.addStretch()
        
        return widget
    
    def create_weight_tab(self):
        """Create weight and balance parameters tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Basic weight group
        weight_group = QGroupBox("Weight Settings")
        weight_layout = QFormLayout()
        
        # Total mass
        self.total_mass = QDoubleSpinBox()
        self.total_mass.setRange(0, 5000)
        self.total_mass.setSuffix(" kg")
        self.total_mass.setDecimals(0)
        weight_layout.addRow("Total Mass:", self.total_mass)
        
        weight_group.setLayout(weight_layout)
        layout.addWidget(weight_group)
        
        # Center of gravity group
        cg_group = QGroupBox("Center of Gravity")
        cg_layout = QFormLayout()
        
        # CG X
        self.cg_location_x = QDoubleSpinBox()
        self.cg_location_x.setRange(-5.0, 5.0)
        self.cg_location_x.setSuffix(" m")
        self.cg_location_x.setDecimals(3)
        self.cg_location_x.setSingleStep(0.01)
        cg_layout.addRow("X (lateral):", self.cg_location_x)
        
        # CG Y
        self.cg_location_y = QDoubleSpinBox()
        self.cg_location_y.setRange(-5.0, 5.0)
        self.cg_location_y.setSuffix(" m")
        self.cg_location_y.setDecimals(3)
        self.cg_location_y.setSingleStep(0.01)
        cg_layout.addRow("Y (vertical):", self.cg_location_y)
        
        # CG Z
        self.cg_location_z = QDoubleSpinBox()
        self.cg_location_z.setRange(-5.0, 5.0)
        self.cg_location_z.setSuffix(" m")
        self.cg_location_z.setDecimals(3)
        self.cg_location_z.setSingleStep(0.01)
        cg_layout.addRow("Z (longitudinal):", self.cg_location_z)
        
        cg_group.setLayout(cg_layout)
        layout.addWidget(cg_group)
        
        layout.addStretch()
        
        return widget
    
    def create_aero_tab(self):
        """Create aerodynamics parameters tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Basic aero group
        basic_group = QGroupBox("Drag Settings")
        basic_layout = QFormLayout()
        
        # Drag coefficient
        self.drag_coeff = QDoubleSpinBox()
        self.drag_coeff.setRange(0, 2.0)
        self.drag_coeff.setDecimals(3)
        self.drag_coeff.setSingleStep(0.01)
        basic_layout.addRow("Drag Coefficient:", self.drag_coeff)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Front downforce group
        front_group = QGroupBox("Front Downforce")
        front_layout = QFormLayout()
        
        # Front lift coefficient (negative = downforce)
        self.front_lift_coeff = QDoubleSpinBox()
        self.front_lift_coeff.setRange(-5.0, 5.0)
        self.front_lift_coeff.setDecimals(3)
        self.front_lift_coeff.setSingleStep(0.01)
        front_layout.addRow("Lift Coefficient:", self.front_lift_coeff)
        
        # Front CL gain
        self.front_cl_gain = QDoubleSpinBox()
        self.front_cl_gain.setRange(0, 0.1)
        self.front_cl_gain.setDecimals(4)
        self.front_cl_gain.setSingleStep(0.0001)
        front_layout.addRow("CL Gain:", self.front_cl_gain)
        
        front_group.setLayout(front_layout)
        layout.addWidget(front_group)
        
        # Rear downforce group
        rear_group = QGroupBox("Rear Downforce")
        rear_layout = QFormLayout()
        
        # Rear lift coefficient (negative = downforce)
        self.rear_lift_coeff = QDoubleSpinBox()
        self.rear_lift_coeff.setRange(-5.0, 5.0)
        self.rear_lift_coeff.setDecimals(3)
        self.rear_lift_coeff.setSingleStep(0.01)
        rear_layout.addRow("Lift Coefficient:", self.rear_lift_coeff)
        
        # Rear CL gain
        self.rear_cl_gain = QDoubleSpinBox()
        self.rear_cl_gain.setRange(0, 0.1)
        self.rear_cl_gain.setDecimals(4)
        self.rear_cl_gain.setSingleStep(0.0001)
        rear_layout.addRow("CL Gain:", self.rear_cl_gain)
        
        rear_group.setLayout(rear_layout)
        layout.addWidget(rear_group)
        
        layout.addStretch()
        
        return widget
        
    def load_data(self):
        """Load car data into UI fields"""
        # Load engine data
        if self.engine_ini and self.engine_ini.has_section('ENGINE_DATA'):
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
        if self.engine_ini and self.engine_ini.has_section('TURBO_0'):
            max_boost = self.engine_ini.get_value('TURBO_0', 'MAX_BOOST', '0.0')
            wastegate = self.engine_ini.get_value('TURBO_0', 'WASTEGATE', '0.0')
            
            self.max_boost.setValue(float(max_boost))
            self.wastegate.setValue(float(wastegate))
            
            self.original_values['max_boost'] = float(max_boost)
            self.original_values['wastegate'] = float(wastegate)
        
        # Load suspension data
        if self.suspension_ini:
            # Front suspension
            if self.suspension_ini.has_section('FRONT'):
                front_spring = self.suspension_ini.get_value('FRONT', 'SPRING_RATE', '80000')
                front_fast_bump = self.suspension_ini.get_value('FRONT', 'DAMPER_FAST_BUMP', '3500')
                front_fast_rebound = self.suspension_ini.get_value('FRONT', 'DAMPER_FAST_REBOUND', '5500')
                front_slow_bump = self.suspension_ini.get_value('FRONT', 'DAMPER_SLOW_BUMP', '2500')
                front_slow_rebound = self.suspension_ini.get_value('FRONT', 'DAMPER_SLOW_REBOUND', '4500')
                front_rod = self.suspension_ini.get_value('FRONT', 'ROD_LENGTH', '0.3')
                
                self.front_spring_rate.setValue(float(front_spring))
                self.front_damper_fast_bump.setValue(float(front_fast_bump))
                self.front_damper_fast_rebound.setValue(float(front_fast_rebound))
                self.front_damper_slow_bump.setValue(float(front_slow_bump))
                self.front_damper_slow_rebound.setValue(float(front_slow_rebound))
                self.front_rod_length.setValue(float(front_rod))
                
                self.original_values['front_spring_rate'] = float(front_spring)
                self.original_values['front_damper_fast_bump'] = float(front_fast_bump)
                self.original_values['front_damper_fast_rebound'] = float(front_fast_rebound)
                self.original_values['front_damper_slow_bump'] = float(front_slow_bump)
                self.original_values['front_damper_slow_rebound'] = float(front_slow_rebound)
                self.original_values['front_rod_length'] = float(front_rod)
            
            # Rear suspension
            if self.suspension_ini.has_section('REAR'):
                rear_spring = self.suspension_ini.get_value('REAR', 'SPRING_RATE', '85000')
                rear_fast_bump = self.suspension_ini.get_value('REAR', 'DAMPER_FAST_BUMP', '4000')
                rear_fast_rebound = self.suspension_ini.get_value('REAR', 'DAMPER_FAST_REBOUND', '6000')
                rear_slow_bump = self.suspension_ini.get_value('REAR', 'DAMPER_SLOW_BUMP', '3000')
                rear_slow_rebound = self.suspension_ini.get_value('REAR', 'DAMPER_SLOW_REBOUND', '5000')
                rear_rod = self.suspension_ini.get_value('REAR', 'ROD_LENGTH', '0.3')
                
                self.rear_spring_rate.setValue(float(rear_spring))
                self.rear_damper_fast_bump.setValue(float(rear_fast_bump))
                self.rear_damper_fast_rebound.setValue(float(rear_fast_rebound))
                self.rear_damper_slow_bump.setValue(float(rear_slow_bump))
                self.rear_damper_slow_rebound.setValue(float(rear_slow_rebound))
                self.rear_rod_length.setValue(float(rear_rod))
                
                self.original_values['rear_spring_rate'] = float(rear_spring)
                self.original_values['rear_damper_fast_bump'] = float(rear_fast_bump)
                self.original_values['rear_damper_fast_rebound'] = float(rear_fast_rebound)
                self.original_values['rear_damper_slow_bump'] = float(rear_slow_bump)
                self.original_values['rear_damper_slow_rebound'] = float(rear_slow_rebound)
                self.original_values['rear_rod_length'] = float(rear_rod)
        
        # Load drivetrain data
        if self.drivetrain_ini:
            # Traction type
            if self.drivetrain_ini.has_section('TRACTION'):
                traction_type = self.drivetrain_ini.get_value('TRACTION', 'TYPE', 'RWD')
                index = self.traction_type.findText(traction_type)
                if index >= 0:
                    self.traction_type.setCurrentIndex(index)
                self.original_values['traction_type'] = traction_type
            
            # Differential
            if self.drivetrain_ini.has_section('DIFFERENTIAL'):
                diff_type = self.drivetrain_ini.get_value('DIFFERENTIAL', 'TYPE', 'LSD')
                diff_power = self.drivetrain_ini.get_value('DIFFERENTIAL', 'POWER', '0.25')
                diff_coast = self.drivetrain_ini.get_value('DIFFERENTIAL', 'COAST', '0.15')
                diff_preload = self.drivetrain_ini.get_value('DIFFERENTIAL', 'PRELOAD', '50')
                
                index = self.diff_type.findText(diff_type)
                if index >= 0:
                    self.diff_type.setCurrentIndex(index)
                self.diff_power.setValue(float(diff_power))
                self.diff_coast.setValue(float(diff_coast))
                self.diff_preload.setValue(float(diff_preload))
                
                self.original_values['diff_type'] = diff_type
                self.original_values['diff_power'] = float(diff_power)
                self.original_values['diff_coast'] = float(diff_coast)
                self.original_values['diff_preload'] = float(diff_preload)
        
        # Load car/weight data
        if self.car_ini:
            if self.car_ini.has_section('BASIC'):
                total_mass = self.car_ini.get_value('BASIC', 'TOTALMASS', '1350')
                self.total_mass.setValue(float(total_mass))
                self.original_values['total_mass'] = float(total_mass)
            
            if self.car_ini.has_section('GRAPHICS'):
                cg_location = self.car_ini.get_value('GRAPHICS', 'CG_LOCATION', '0.0,0.35,0.0')
                cg_parts = [float(x.strip()) for x in cg_location.split(',')]
                if len(cg_parts) == 3:
                    self.cg_location_x.setValue(cg_parts[0])
                    self.cg_location_y.setValue(cg_parts[1])
                    self.cg_location_z.setValue(cg_parts[2])
                    
                    self.original_values['cg_location_x'] = cg_parts[0]
                    self.original_values['cg_location_y'] = cg_parts[1]
                    self.original_values['cg_location_z'] = cg_parts[2]
        
        # Load aero data
        if self.aero_ini:
            if self.aero_ini.has_section('SETTINGS'):
                drag_coeff = self.aero_ini.get_value('SETTINGS', 'DRAG_COEFF', '0.34')
                self.drag_coeff.setValue(float(drag_coeff))
                self.original_values['drag_coeff'] = float(drag_coeff)
            
            if self.aero_ini.has_section('FRONT'):
                front_lift = self.aero_ini.get_value('FRONT', 'LIFTCOEFF', '-0.15')
                front_cl_gain = self.aero_ini.get_value('FRONT', 'CL_GAIN', '0.0025')
                self.front_lift_coeff.setValue(float(front_lift))
                self.front_cl_gain.setValue(float(front_cl_gain))
                
                self.original_values['front_lift_coeff'] = float(front_lift)
                self.original_values['front_cl_gain'] = float(front_cl_gain)
            
            if self.aero_ini.has_section('REAR'):
                rear_lift = self.aero_ini.get_value('REAR', 'LIFTCOEFF', '-0.45')
                rear_cl_gain = self.aero_ini.get_value('REAR', 'CL_GAIN', '0.005')
                self.rear_lift_coeff.setValue(float(rear_lift))
                self.rear_cl_gain.setValue(float(rear_cl_gain))
                
                self.original_values['rear_lift_coeff'] = float(rear_lift)
                self.original_values['rear_cl_gain'] = float(rear_cl_gain)
    
    def edit_power_curve(self):
        """Open curve editor for power.lut"""
        power_lut_path = os.path.join(self.car_data_path, 'power.lut')
        
        if not os.path.exists(power_lut_path):
            reply = QMessageBox.question(
                self, "File Not Found",
                "power.lut file not found. Create a new one?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        # Open curve editor dialog
        dialog = CurveEditorDialog(
            lut_file_path=power_lut_path if os.path.exists(power_lut_path) else None,
            x_label="RPM",
            y_label="Power (kW)",
            parent=self
        )
        dialog.exec_()
    
    def edit_coast_curve(self):
        """Open curve editor for coast.lut"""
        coast_lut_path = os.path.join(self.car_data_path, 'coast.lut')
        
        if not os.path.exists(coast_lut_path):
            reply = QMessageBox.question(
                self, "File Not Found",
                "coast.lut file not found. Create a new one?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        # Open curve editor dialog
        dialog = CurveEditorDialog(
            lut_file_path=coast_lut_path if os.path.exists(coast_lut_path) else None,
            x_label="RPM",
            y_label="Torque (Nm)",
            parent=self
        )
        dialog.exec_()
    
    def save_changes(self):
        """Save changes to car files"""
        try:
            # Save engine data
            if self.engine_ini:
                self.engine_ini.set_value('ENGINE_DATA', 'MINIMUM', str(self.minimum_rpm.value()))
                self.engine_ini.set_value('ENGINE_DATA', 'MAXIMUM', str(self.maximum_rpm.value()))
                self.engine_ini.set_value('ENGINE_DATA', 'LIMITER', str(self.limiter_rpm.value()))
                
                # Save turbo data if section exists
                if self.engine_ini.has_section('TURBO_0'):
                    self.engine_ini.set_value('TURBO_0', 'MAX_BOOST', str(self.max_boost.value()))
                    self.engine_ini.set_value('TURBO_0', 'WASTEGATE', str(self.wastegate.value()))
                
                # Save to file with backup
                self.engine_ini.save(backup=True)
            
            # Save suspension data
            if self.suspension_ini:
                if self.suspension_ini.has_section('FRONT'):
                    self.suspension_ini.set_value('FRONT', 'SPRING_RATE', str(self.front_spring_rate.value()))
                    self.suspension_ini.set_value('FRONT', 'DAMPER_FAST_BUMP', str(self.front_damper_fast_bump.value()))
                    self.suspension_ini.set_value('FRONT', 'DAMPER_FAST_REBOUND', str(self.front_damper_fast_rebound.value()))
                    self.suspension_ini.set_value('FRONT', 'DAMPER_SLOW_BUMP', str(self.front_damper_slow_bump.value()))
                    self.suspension_ini.set_value('FRONT', 'DAMPER_SLOW_REBOUND', str(self.front_damper_slow_rebound.value()))
                    self.suspension_ini.set_value('FRONT', 'ROD_LENGTH', str(self.front_rod_length.value()))
                
                if self.suspension_ini.has_section('REAR'):
                    self.suspension_ini.set_value('REAR', 'SPRING_RATE', str(self.rear_spring_rate.value()))
                    self.suspension_ini.set_value('REAR', 'DAMPER_FAST_BUMP', str(self.rear_damper_fast_bump.value()))
                    self.suspension_ini.set_value('REAR', 'DAMPER_FAST_REBOUND', str(self.rear_damper_fast_rebound.value()))
                    self.suspension_ini.set_value('REAR', 'DAMPER_SLOW_BUMP', str(self.rear_damper_slow_bump.value()))
                    self.suspension_ini.set_value('REAR', 'DAMPER_SLOW_REBOUND', str(self.rear_damper_slow_rebound.value()))
                    self.suspension_ini.set_value('REAR', 'ROD_LENGTH', str(self.rear_rod_length.value()))
                
                self.suspension_ini.save(backup=True)
            
            # Save drivetrain data
            if self.drivetrain_ini:
                # Save traction type
                if self.drivetrain_ini.has_section('TRACTION'):
                    self.drivetrain_ini.set_value('TRACTION', 'TYPE', self.traction_type.currentText())
                
                # Save differential settings
                if self.drivetrain_ini.has_section('DIFFERENTIAL'):
                    self.drivetrain_ini.set_value('DIFFERENTIAL', 'TYPE', self.diff_type.currentText())
                    self.drivetrain_ini.set_value('DIFFERENTIAL', 'POWER', str(self.diff_power.value()))
                    self.drivetrain_ini.set_value('DIFFERENTIAL', 'COAST', str(self.diff_coast.value()))
                    self.drivetrain_ini.set_value('DIFFERENTIAL', 'PRELOAD', str(self.diff_preload.value()))
                
                self.drivetrain_ini.save(backup=True)
            
            # Save car/weight data
            if self.car_ini:
                if self.car_ini.has_section('BASIC'):
                    self.car_ini.set_value('BASIC', 'TOTALMASS', str(self.total_mass.value()))
                
                if self.car_ini.has_section('GRAPHICS'):
                    cg_location = f"{self.cg_location_x.value()},{self.cg_location_y.value()},{self.cg_location_z.value()}"
                    self.car_ini.set_value('GRAPHICS', 'CG_LOCATION', cg_location)
                
                self.car_ini.save(backup=True)
            
            # Save aero data
            if self.aero_ini:
                if self.aero_ini.has_section('SETTINGS'):
                    self.aero_ini.set_value('SETTINGS', 'DRAG_COEFF', str(self.drag_coeff.value()))
                
                if self.aero_ini.has_section('FRONT'):
                    self.aero_ini.set_value('FRONT', 'LIFTCOEFF', str(self.front_lift_coeff.value()))
                    self.aero_ini.set_value('FRONT', 'CL_GAIN', str(self.front_cl_gain.value()))
                
                if self.aero_ini.has_section('REAR'):
                    self.aero_ini.set_value('REAR', 'LIFTCOEFF', str(self.rear_lift_coeff.value()))
                    self.aero_ini.set_value('REAR', 'CL_GAIN', str(self.rear_cl_gain.value()))
                
                self.aero_ini.save(backup=True)
            
            QMessageBox.information(
                self,
                "Success",
                "Changes saved successfully!\n\n"
                "Backups of the original files were created with .bak extension."
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
        # Engine values
        if 'minimum' in self.original_values:
            self.minimum_rpm.setValue(self.original_values['minimum'])
            self.maximum_rpm.setValue(self.original_values['maximum'])
            self.limiter_rpm.setValue(self.original_values['limiter'])
        
        if 'max_boost' in self.original_values:
            self.max_boost.setValue(self.original_values['max_boost'])
            self.wastegate.setValue(self.original_values['wastegate'])
        
        # Suspension values
        if 'front_spring_rate' in self.original_values:
            self.front_spring_rate.setValue(self.original_values['front_spring_rate'])
            self.front_damper_fast_bump.setValue(self.original_values['front_damper_fast_bump'])
            self.front_damper_fast_rebound.setValue(self.original_values['front_damper_fast_rebound'])
            self.front_damper_slow_bump.setValue(self.original_values['front_damper_slow_bump'])
            self.front_damper_slow_rebound.setValue(self.original_values['front_damper_slow_rebound'])
            self.front_rod_length.setValue(self.original_values['front_rod_length'])
        
        if 'rear_spring_rate' in self.original_values:
            self.rear_spring_rate.setValue(self.original_values['rear_spring_rate'])
            self.rear_damper_fast_bump.setValue(self.original_values['rear_damper_fast_bump'])
            self.rear_damper_fast_rebound.setValue(self.original_values['rear_damper_fast_rebound'])
            self.rear_damper_slow_bump.setValue(self.original_values['rear_damper_slow_bump'])
            self.rear_damper_slow_rebound.setValue(self.original_values['rear_damper_slow_rebound'])
            self.rear_rod_length.setValue(self.original_values['rear_rod_length'])
        
        # Differential values
        if 'diff_type' in self.original_values:
            index = self.diff_type.findText(self.original_values['diff_type'])
            if index >= 0:
                self.diff_type.setCurrentIndex(index)
        
        if 'diff_power' in self.original_values:
            self.diff_power.setValue(self.original_values['diff_power'])
            self.diff_coast.setValue(self.original_values['diff_coast'])
            self.diff_preload.setValue(self.original_values['diff_preload'])
        
        # Traction type values
        if 'traction_type' in self.original_values:
            index = self.traction_type.findText(self.original_values['traction_type'])
            if index >= 0:
                self.traction_type.setCurrentIndex(index)
        
        # Weight values
        if 'total_mass' in self.original_values:
            self.total_mass.setValue(self.original_values['total_mass'])
        
        if 'cg_location_x' in self.original_values:
            self.cg_location_x.setValue(self.original_values['cg_location_x'])
            self.cg_location_y.setValue(self.original_values['cg_location_y'])
            self.cg_location_z.setValue(self.original_values['cg_location_z'])
        
        # Aero values
        if 'drag_coeff' in self.original_values:
            self.drag_coeff.setValue(self.original_values['drag_coeff'])
        
        if 'front_lift_coeff' in self.original_values:
            self.front_lift_coeff.setValue(self.original_values['front_lift_coeff'])
            self.front_cl_gain.setValue(self.original_values['front_cl_gain'])
        
        if 'rear_lift_coeff' in self.original_values:
            self.rear_lift_coeff.setValue(self.original_values['rear_lift_coeff'])
            self.rear_cl_gain.setValue(self.original_values['rear_cl_gain'])
