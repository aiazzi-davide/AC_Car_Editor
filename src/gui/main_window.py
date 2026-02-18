"""
Main Window GUI for AC Car Editor
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QLabel, QPushButton, QStatusBar,
    QMenuBar, QAction, QFileDialog, QMessageBox,
    QSplitter, QGroupBox, QTextEdit, QDialog, QLineEdit
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config import ConfigManager
from core.car_file_manager import CarFileManager
from core.component_library import ComponentLibrary
from gui.car_editor_dialog import CarEditorDialog
from gui.component_library_dialog import ComponentLibraryDialog


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
        
        # Full car list for filtering
        self.all_cars = []
        
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
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Filter cars...")
        self.search_box.textChanged.connect(self.filter_cars)
        
        clear_btn = QPushButton("✕")
        clear_btn.setMaximumWidth(30)
        clear_btn.setToolTip("Clear filter")
        clear_btn.clicked.connect(self.clear_filter)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(clear_btn)
        layout.addLayout(search_layout)
        
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
        
        # Preview image
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(150)
        self.preview_label.setMaximumHeight(250)
        self.preview_label.setStyleSheet("QLabel { background-color: #f0f0f0; border: 1px solid #ccc; }")
        self.preview_label.setText("No preview image")
        layout.addWidget(self.preview_label)
        
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
        self.all_cars = self.car_manager.get_car_list()
        
        # Clear search box and display all cars
        self.search_box.clear()
        self.car_list.clear()
        self.car_list.addItems(self.all_cars)
        
        self.statusBar.showMessage(f"Loaded {len(self.all_cars)} cars from {cars_path}")
        
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
        
        # Load and display preview image
        preview_path = self.car_manager.get_car_preview_path(car_name)
        if preview_path:
            pixmap = QPixmap(preview_path)
            if not pixmap.isNull():
                # Scale to fit while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    self.preview_label.width() - 10,
                    self.preview_label.height() - 10,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled_pixmap)
            else:
                self.preview_label.setText("Failed to load preview image")
        else:
            self.preview_label.clear()
            self.preview_label.setText("No preview image")
        
        # Build details text
        details = []
        details.append(f"Folder: {car_name}")
        if car_info.get('brand'):
            details.append(f"Brand: {car_info['brand']}")
        details.append(f"Has data folder: {'Yes' if car_info['has_data_folder'] else 'No'}")
        details.append(f"Has data.acd: {'Yes' if car_info['has_data_acd'] else 'No'}")
        
        self.car_details.setPlainText('\n'.join(details))
        
        # Enable edit button if car has data folder OR data.acd
        can_edit = car_info['has_data_folder'] or car_info['has_data_acd']
        self.edit_btn.setEnabled(can_edit)
        
        # Enable backup button only if car has unpacked data folder
        can_backup = car_info['has_data_folder']
        self.backup_btn.setEnabled(can_backup)
        
        if not can_edit:
            self.statusBar.showMessage(
                f"Car '{car_name}' has no data folder or data.acd file. Cannot edit."
            )
        else:
            status_msg = f"Selected car: {car_name}"
            if car_info['has_data_acd'] and not car_info['has_data_folder']:
                status_msg += " (will need unpacking)"
            self.statusBar.showMessage(status_msg)
    
    def filter_cars(self, text):
        """Filter car list based on search text"""
        if not text:
            # Show all cars if search is empty
            self.car_list.clear()
            self.car_list.addItems(self.all_cars)
            return
        
        # Filter cars that match the search text (case-insensitive)
        search_lower = text.lower()
        filtered_cars = [car for car in self.all_cars if search_lower in car.lower()]
        
        # Update list
        self.car_list.clear()
        self.car_list.addItems(filtered_cars)
        
        # Update status bar
        self.statusBar.showMessage(f"Showing {len(filtered_cars)} of {len(self.all_cars)} cars")
    
    def clear_filter(self):
        """Clear the search filter"""
        self.search_box.clear()
        
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
        
        # Check if car has data.acd and no data folder
        has_data_folder = self.car_manager.has_data_folder(self.current_car)
        has_data_acd = self.car_manager.has_data_acd(self.current_car)
        
        if not has_data_folder and has_data_acd:
            # Ask user if they want to unpack data.acd
            reply = QMessageBox.question(
                self,
                "Unpack data.acd",
                f"Car '{self.current_car}' has a packed data.acd file.\n\n"
                "Do you want to unpack it for editing?\n\n"
                "Note: The data.acd file will be renamed to data.acd.bak after unpacking "
                "to ensure AC uses the unpacked files.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                # Unpack data.acd
                self.statusBar.showMessage("Unpacking data.acd...")
                success = self.car_manager.unpack_data_acd(self.current_car, delete_acd=True)
                
                if not success:
                    QMessageBox.critical(
                        self,
                        "Unpacking Failed",
                        "Failed to unpack data.acd file.\n"
                        "Make sure quickBMS is installed in the tools folder."
                    )
                    return
                
                self.statusBar.showMessage("data.acd unpacked successfully")
            else:
                return
        
        elif not has_data_folder:
            QMessageBox.warning(
                self,
                "Error",
                f"Car '{self.current_car}' has no data folder and no data.acd file."
            )
            return
        
        # Get car data path
        car_data_path = self.car_manager.get_car_data_path(self.current_car)
        
        # Open car editor dialog
        editor = CarEditorDialog(self.current_car, car_data_path, self)
        result = editor.exec_()
        
        # After editing, prompt to rename data.acd if it still exists
        if result == QDialog.Accepted and self.car_manager.has_data_acd(self.current_car):
            reply = QMessageBox.question(
                self,
                "Rename data.acd",
                f"Car '{self.current_car}' still has a data.acd file.\n\n"
                "Assetto Corsa prioritizes data.acd over the unpacked data folder.\n"
                "Do you want to rename data.acd to data.acd.bak to ensure your changes are used in-game?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                if self.car_manager.delete_data_acd(self.current_car):
                    self.statusBar.showMessage("data.acd renamed to data.acd.bak")
                    QMessageBox.information(
                        self,
                        "Success",
                        "data.acd renamed to data.acd.bak. Your changes will now be used in-game."
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Failed to rename data.acd. You may need to rename it manually."
                    )
        
    def open_component_library(self):
        """Open component library manager"""
        dialog = ComponentLibraryDialog(self)
        dialog.exec_()
        
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
