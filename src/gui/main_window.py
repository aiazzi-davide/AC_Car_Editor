"""
Main Window GUI for AC Car Editor
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QLabel, QPushButton, QStatusBar,
    QMenuBar, QAction, QFileDialog, QMessageBox,
    QSplitter, QGroupBox, QTextEdit
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config import ConfigManager
from core.car_file_manager import CarFileManager
from core.component_library import ComponentLibrary
from gui.car_editor_dialog import CarEditorDialog


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        
        # Initialize managers
        self.config_manager = ConfigManager()
        self.car_manager = None
        self.component_library = ComponentLibrary()
        
        # Current car
        self.current_car = None
        
        self.init_ui()
        self.load_cars()
        
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("AC Car Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Car list
        left_panel = self.create_car_list_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Car info
        right_panel = self.create_car_info_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter sizes
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # Set AC Path action
        set_path_action = QAction("Set AC Path...", self)
        set_path_action.triggered.connect(self.set_ac_path)
        file_menu.addAction(set_path_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        # Component library action
        library_action = QAction("Component Library...", self)
        library_action.triggered.connect(self.open_component_library)
        tools_menu.addAction(library_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_car_list_panel(self):
        """Create car list panel"""
        panel = QGroupBox("Cars")
        layout = QVBoxLayout()
        
        # Search/filter could be added here
        
        # Car list
        self.car_list = QListWidget()
        self.car_list.currentItemChanged.connect(self.on_car_selected)
        layout.addWidget(self.car_list)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh List")
        refresh_btn.clicked.connect(self.load_cars)
        layout.addWidget(refresh_btn)
        
        panel.setLayout(layout)
        return panel
        
    def create_car_info_panel(self):
        """Create car info panel"""
        panel = QGroupBox("Car Information")
        layout = QVBoxLayout()
        
        # Car name label
        self.car_name_label = QLabel("No car selected")
        self.car_name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.car_name_label)
        
        # Car details
        self.car_details = QTextEdit()
        self.car_details.setReadOnly(True)
        self.car_details.setMaximumHeight(150)
        layout.addWidget(self.car_details)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Edit Car")
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.edit_car)
        button_layout.addWidget(self.edit_btn)
        
        self.backup_btn = QPushButton("Create Backup")
        self.backup_btn.setEnabled(False)
        self.backup_btn.clicked.connect(self.create_backup)
        button_layout.addWidget(self.backup_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
        
    def load_cars(self):
        """Load list of cars from AC directory"""
        ac_path = self.config_manager.get_ac_path()
        cars_path = self.config_manager.get_cars_path()
        
        if not os.path.exists(cars_path):
            self.statusBar.showMessage(f"AC cars path not found: {cars_path}")
            QMessageBox.warning(
                self,
                "Path Not Found",
                f"The Assetto Corsa cars folder was not found at:\n{cars_path}\n\n"
                "Please set the correct path using File > Set AC Path..."
            )
            return
        
        self.car_manager = CarFileManager(cars_path)
        cars = self.car_manager.get_car_list()
        
        self.car_list.clear()
        self.car_list.addItems(cars)
        
        self.statusBar.showMessage(f"Loaded {len(cars)} cars from {cars_path}")
        
    def on_car_selected(self, current, previous):
        """Handle car selection"""
        if current is None:
            return
        
        car_name = current.text()
        self.current_car = car_name
        
        # Get car info
        car_info = self.car_manager.get_car_info(car_name)
        
        # Update UI
        self.car_name_label.setText(car_info.get('display_name', car_name))
        
        # Build details text
        details = []
        details.append(f"Folder: {car_name}")
        if car_info.get('brand'):
            details.append(f"Brand: {car_info['brand']}")
        details.append(f"Has data folder: {'Yes' if car_info['has_data_folder'] else 'No'}")
        details.append(f"Has data.acd: {'Yes' if car_info['has_data_acd'] else 'No'}")
        
        self.car_details.setPlainText('\n'.join(details))
        
        # Enable buttons if car has data folder
        can_edit = car_info['has_data_folder']
        self.edit_btn.setEnabled(can_edit)
        self.backup_btn.setEnabled(can_edit)
        
        if not can_edit:
            self.statusBar.showMessage(
                f"Car '{car_name}' has no unpacked data folder. Cannot edit."
            )
        else:
            self.statusBar.showMessage(f"Selected car: {car_name}")
        
    def set_ac_path(self):
        """Set Assetto Corsa installation path"""
        current_path = self.config_manager.get_ac_path()
        
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Assetto Corsa Installation Folder",
            current_path
        )
        
        if path:
            self.config_manager.set_ac_path(path)
            self.statusBar.showMessage(f"AC path set to: {path}")
            self.load_cars()
            
    def create_backup(self):
        """Create backup of current car"""
        if not self.current_car:
            return
        
        backup_path = self.config_manager.get_backup_path()
        result = self.car_manager.create_backup(self.current_car, backup_path)
        
        if result:
            QMessageBox.information(
                self,
                "Backup Created",
                f"Backup created successfully:\n{result}"
            )
            self.statusBar.showMessage("Backup created successfully")
        else:
            QMessageBox.warning(
                self,
                "Backup Failed",
                "Failed to create backup. Check console for details."
            )
            
    def edit_car(self):
        """Open car editor"""
        if not self.current_car:
            return
        
        # Get car data path
        car_data_path = self.car_manager.get_car_data_path(self.current_car)
        
        if not os.path.exists(car_data_path):
            QMessageBox.warning(
                self,
                "Error",
                f"Car data folder not found:\n{car_data_path}"
            )
            return
        
        # Open car editor dialog
        editor = CarEditorDialog(self.current_car, car_data_path, self)
        editor.exec_()
        
    def open_component_library(self):
        """Open component library manager (placeholder)"""
        QMessageBox.information(
            self,
            "Coming Soon",
            "Component library manager will be implemented in future updates.\n\n"
            "This will allow you to:\n"
            "- Manage pre-built components\n"
            "- Apply components to cars\n"
            "- Import/export components"
        )
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About AC Car Editor",
            "<h3>AC Car Editor</h3>"
            "<p>Version 0.1.0</p>"
            "<p>A tool for modifying Assetto Corsa car configurations.</p>"
            "<p>Allows editing of engine, suspension, differential, and other car parameters.</p>"
        )
