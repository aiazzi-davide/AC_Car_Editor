"""
Main Window GUI for AC Car Editor
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QLabel, QPushButton, QStatusBar,
    QMenuBar, QAction, QFileDialog, QMessageBox,
    QSplitter, QGroupBox, QTextEdit, QDialog, QLineEdit, QCheckBox
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QPixmap

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.config import ConfigManager
from core.car_file_manager import CarFileManager
from core.component_library import ComponentLibrary
from gui.car_editor_dialog import CarEditorDialog
from gui.component_library_dialog import ComponentLibraryDialog
from gui.ui_editor_dialog import UIEditorDialog
from gui.theme import COLORS, btn_primary, btn_outline, section_title, card_style, muted_text
from gui.toast import show_toast


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
        QTimer.singleShot(200, self._show_startup_disclaimer)
        
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

        # Open backups folder
        open_backups_action = QAction("📁  Open Backups Folder", self)
        open_backups_action.triggered.connect(self.open_backups_folder)
        file_menu.addAction(open_backups_action)
        
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
        self.car_name_label.setStyleSheet(section_title())
        layout.addWidget(self.car_name_label)

        # Disclaimer banner (visible when no car selected)
        self.disclaimer_label = QLabel(
            "⚠️  <b>Nota di compatibilità</b><br>"
            "Questo programma è stato testato principalmente sulle auto ufficiali Kunos.<br>"
            "Con le auto <b>moddate</b> potrebbe non funzionare correttamente, "
            "anche se nella maggior parte dei casi funziona comunque.<br>"
            "Crea sempre un backup prima di modificare qualsiasi auto."
        )
        self.disclaimer_label.setWordWrap(True)
        self.disclaimer_label.setTextFormat(Qt.RichText)
        self.disclaimer_label.setStyleSheet(
            "QLabel { background-color: #fff8e1; color: #5d4037; border: 1px solid #ffcc02; "
            "border-radius: 6px; padding: 10px; font-size: 12px; }"
        )
        layout.addWidget(self.disclaimer_label)
        
        # Preview image
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(150)
        self.preview_label.setMaximumHeight(300)
        self.preview_label.setStyleSheet(
            f"QLabel {{ background-color: {COLORS['tab_inactive_bg']}; "
            f"border: 1px solid {COLORS['border']}; border-radius: 10px; }}"
        )
        self.preview_label.setText("No preview image")
        layout.addWidget(self.preview_label)
        
        # Car details
        self.car_details = QTextEdit()
        self.car_details.setReadOnly(True)
        self.car_details.setMaximumHeight(150)
        layout.addWidget(self.car_details)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("✏️  Edit Car")
        self.edit_btn.setEnabled(False)
        self.edit_btn.setStyleSheet(btn_primary())
        self.edit_btn.clicked.connect(self.edit_car)
        button_layout.addWidget(self.edit_btn)
        
        self.open_folder_btn = QPushButton("📁  Open Folder")
        self.open_folder_btn.clicked.connect(self.open_car_folder)
        button_layout.addWidget(self.open_folder_btn)
        
        self.edit_ui_btn = QPushButton("🎨  Edit UI")
        self.edit_ui_btn.setToolTip("Edit car name, brand, icons in ui/ folder")
        self.edit_ui_btn.setEnabled(False)
        self.edit_ui_btn.clicked.connect(self.edit_ui_metadata)
        button_layout.addWidget(self.edit_ui_btn)
        
        self.backup_btn = QPushButton("💾  Backup")
        self.backup_btn.setEnabled(False)
        self.backup_btn.clicked.connect(self.create_backup)
        button_layout.addWidget(self.backup_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
        
    def _show_startup_disclaimer(self):
        """Show one-time compatibility disclaimer on startup (no system sound)."""
        if not self.config_manager.get_show_disclaimer():
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("Nota di compatibilità")
        dlg.setFixedWidth(440)
        layout = QVBoxLayout(dlg)
        layout.setSpacing(12)
        layout.setContentsMargins(18, 18, 18, 14)

        text = QLabel(
            "<b>AC Car Editor</b> è stato testato principalmente sulle auto ufficiali "
            "<b>Kunos</b>.<br><br>"
            "Con le auto <b>moddate</b> il programma <i>spesso funziona correttamente</i>, "
            "ma potrebbe incontrare file INI con strutture non standard o sezioni mancanti.<br><br>"
            "Si consiglia sempre di creare un <b>backup</b> prima di apportare modifiche."
        )
        text.setWordWrap(True)
        text.setTextFormat(Qt.RichText)
        layout.addWidget(text)

        dont_show = QCheckBox("Non mostrare più questo messaggio")
        layout.addWidget(dont_show)

        ok_btn = QPushButton("OK")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(dlg.accept)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

        dlg.exec_()

        if dont_show.isChecked():
            self.config_manager.set_show_disclaimer(False)

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

        # Hide disclaimer when a car is selected
        self.disclaimer_label.setVisible(False)
        
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
                # Use fallback dimensions if the label hasn't been laid out yet
                label_w = max(self.preview_label.width() - 10, 300)
                label_h = max(self.preview_label.height() - 10, 150)
                scaled_pixmap = pixmap.scaled(
                    label_w,
                    label_h,
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
        
        # Enable UI edit button (no data folder required, just ui_car.json)
        self.edit_ui_btn.setEnabled(True)
        
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
            show_toast(self, f"✅  Backup created successfully: {result}", kind='success')
            self.statusBar.showMessage("Backup created successfully")
        else:
            QMessageBox.warning(
                self,
                "Backup Failed",
                "Failed to create backup. Check console for details."
            )
    
    def open_backups_folder(self):
        """Open the backups folder in the system file explorer."""
        import subprocess, platform
        backup_path = os.path.abspath(self.config_manager.get_backup_path())
        os.makedirs(backup_path, exist_ok=True)
        try:
            system = platform.system()
            if system == 'Windows':
                subprocess.Popen(['explorer', backup_path])
            elif system == 'Darwin':
                subprocess.Popen(['open', backup_path])
            else:
                subprocess.Popen(['xdg-open', backup_path])
            self.statusBar.showMessage(f"Opened backups folder: {backup_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open folder:\n{str(e)}")

    def open_car_folder(self):
        """Open the current car's folder in the system file explorer."""
        if not self.current_car:
            return
        
        import subprocess
        import platform
        
        # Get the car's folder path
        car_path = self.car_manager.get_car_path(self.current_car)
        
        if not os.path.exists(car_path):
            QMessageBox.warning(
                self,
                "Folder Not Found",
                f"The car's folder does not exist:\n{car_path}"
            )
            return
        
        try:
            system = platform.system()
            if system == 'Windows':
                subprocess.Popen(['explorer', car_path])
            elif system == 'Darwin':  # macOS
                subprocess.Popen(['open', car_path])
            else:  # Linux and others
                subprocess.Popen(['xdg-open', car_path])
            self.statusBar.showMessage(f"Opened folder: {car_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open folder:\n{str(e)}")
            
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
                    show_toast(self, "✅  data.acd renamed — your changes will be used in-game.", kind='success')
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Failed to rename data.acd. You may need to rename it manually."
                    )
        
    def edit_ui_metadata(self):
        """Open UI metadata editor"""
        if not self.current_car:
            return
        
        car_path = self.car_manager.get_car_path(self.current_car)
        
        # Open UI editor dialog
        editor = UIEditorDialog(self.current_car, car_path, self)
        result = editor.exec_()
        
        if result == QDialog.Accepted:
            self.statusBar.showMessage(f"UI metadata updated for {self.current_car}")
            # Refresh car info to show updated name
            self.on_car_selected(self.car_list.currentItem(), None)
    
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
