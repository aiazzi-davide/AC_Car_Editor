"""
Curve Editor Dialog for editing LUT files.

This dialog provides a standalone window for editing .lut curve files.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                              QFileDialog, QMessageBox, QGroupBox, QLabel,
                              QComboBox)
from PyQt5.QtCore import Qt

from core.lut_parser import LUTCurve
from gui.curve_editor_widget import CurveEditorWidget
from gui.toast import show_toast


class CurveEditorDialog(QDialog):
    """Dialog for editing LUT curve files."""
    
    # Preset curves
    PRESETS = {
        "Linear": [(0, 0), (1000, 100), (2000, 200), (3000, 300), (4000, 400), (5000, 500)],
        "Turbo (Lag)": [
            (0, 0), (1000, 50), (2000, 80), (2500, 120), (3000, 200),
            (4000, 300), (5000, 350), (6000, 380), (7000, 390)
        ],
        "NA (Linear Peak)": [
            (0, 0), (1000, 80), (2000, 150), (3000, 220), (4000, 280),
            (5000, 320), (6000, 340), (7000, 330), (8000, 300)
        ],
        "V-Shape (Coast)": [
            (0, -50), (2000, -120), (4000, -180), (6000, -150), (8000, -100)
        ]
    }
    
    def __init__(self, lut_file_path=None, x_label="X", y_label="Y", parent=None):
        """
        Initialize the curve editor dialog.
        
        Args:
            lut_file_path: Path to LUT file to edit (optional)
            x_label: Label for X axis
            y_label: Label for Y axis
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.lut_file_path = lut_file_path
        self.x_label = x_label
        self.y_label = y_label
        self.curve_modified = False
        
        self.init_ui()
        
        # Load file if provided
        if lut_file_path and os.path.exists(lut_file_path):
            self.load_file(lut_file_path)
        else:
            # Start with empty curve
            self.editor.load_curve(LUTCurve())
            
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Curve Editor")
        self.setGeometry(100, 100, 1000, 700)
        
        layout = QVBoxLayout(self)
        
        # Info panel
        info_group = QGroupBox("Curve Information")
        info_layout = QHBoxLayout()
        
        self.file_label = QLabel("No file loaded")
        info_layout.addWidget(self.file_label)
        
        info_layout.addStretch()
        
        # Preset selector
        info_layout.addWidget(QLabel("Load Preset:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("-- Select Preset --")
        for preset_name in self.PRESETS.keys():
            self.preset_combo.addItem(preset_name)
        self.preset_combo.currentTextChanged.connect(self.load_preset)
        info_layout.addWidget(self.preset_combo)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Curve editor widget
        self.editor = CurveEditorWidget(self)
        self.editor.set_axis_labels(self.x_label, self.y_label)
        self.editor.curve_changed.connect(self.on_curve_changed)
        layout.addWidget(self.editor)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        load_btn = QPushButton("Load File...")
        load_btn.clicked.connect(self.load_file_dialog)
        button_layout.addWidget(load_btn)
        
        # Removed "Import..." button as it has the same function as "Load File..."
        
        export_btn = QPushButton("Export...")
        export_btn.clicked.connect(self.export_curve)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_file)
        button_layout.addWidget(save_btn)
        
        save_as_btn = QPushButton("Save As...")
        save_as_btn.clicked.connect(self.save_file_as)
        button_layout.addWidget(save_as_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close_dialog)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def on_curve_changed(self):
        """Handle curve modifications."""
        self.curve_modified = True
        self.setWindowTitle("Curve Editor *")
        
    def load_file(self, file_path):
        """Load a LUT file."""
        try:
            curve = LUTCurve(file_path)
            curve.load()
            self.editor.load_curve(curve)
            self.lut_file_path = file_path
            self.file_label.setText(f"File: {os.path.basename(file_path)}")
            self.curve_modified = False
            self.setWindowTitle("Curve Editor")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")
            
    def load_file_dialog(self):
        """Show file dialog to load a LUT file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load LUT File", "", "LUT Files (*.lut);;All Files (*.*)"
        )
        
        if file_path:
            self.load_file(file_path)
            
    def save_file(self):
        """Save the curve to the current file."""
        if not self.lut_file_path:
            self.save_file_as()
            return
            
        try:
            curve = self.editor.get_curve()
            curve.save(self.lut_file_path, backup=True)
            self.curve_modified = False
            self.setWindowTitle("Curve Editor")
            show_toast(self, "✅  Curve saved! Backup created (.bak).", kind='success')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
            
    def save_file_as(self):
        """Save the curve to a new file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save LUT File", "", "LUT Files (*.lut);;All Files (*.*)"
        )
        
        if file_path:
            try:
                curve = self.editor.get_curve()
                curve.save(file_path, backup=True)
                self.lut_file_path = file_path
                self.file_label.setText(f"File: {os.path.basename(file_path)}")
                self.curve_modified = False
                self.setWindowTitle("Curve Editor")
                show_toast(self, "✅  Curve saved!", kind='success')
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
                
    def import_curve(self):
        """Import curve data from another LUT file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import LUT File", "", "LUT Files (*.lut);;All Files (*.*)"
        )
        
        if file_path:
            try:
                curve = LUTCurve(file_path)
                curve.load()
                self.editor.load_curve(curve)
                self.curve_modified = True
                self.setWindowTitle("Curve Editor *")
                show_toast(self, f"✅  Imported {len(curve.get_points())} points", kind='success')
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import file: {e}")
                
    def export_curve(self):
        """Export curve data to a new LUT file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export LUT File", "", "LUT Files (*.lut);;All Files (*.*)"
        )
        
        if file_path:
            try:
                curve = self.editor.get_curve()
                curve.save(file_path, backup=False)
                show_toast(self, "✅  Curve exported!", kind='success')
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export file: {e}")
                
    def load_preset(self, preset_name):
        """Load a preset curve."""
        if preset_name == "-- Select Preset --" or preset_name == "":
            return
            
        if preset_name in self.PRESETS:
            # Confirm if curve is modified
            if self.curve_modified:
                reply = QMessageBox.question(
                    self, "Confirm",
                    "Current curve has unsaved changes. Load preset anyway?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    self.preset_combo.setCurrentIndex(0)
                    return
                    
            # Create new curve with preset points
            curve = LUTCurve()
            for x, y in self.PRESETS[preset_name]:
                curve.add_point(x, y)
                
            self.editor.load_curve(curve)
            self.curve_modified = True
            self.setWindowTitle("Curve Editor *")
            
            # Reset combo box
            self.preset_combo.setCurrentIndex(0)
            
    def close_dialog(self):
        """Close the dialog."""
        if self.curve_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "The curve has unsaved changes. Close anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
                
        self.accept()
        
    def closeEvent(self, event):
        """Handle window close event."""
        if self.curve_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "The curve has unsaved changes. Close anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                event.ignore()
                return
                
        event.accept()
