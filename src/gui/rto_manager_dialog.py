"""
RTO Manager Dialog - Manage final.rto and ratios.rto files
"""

import os
import sys
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QPushButton, QListWidget, QLabel, QDoubleSpinBox,
    QMessageBox, QFormLayout, QGroupBox
)
from PyQt5.QtCore import Qt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.rto_parser import RTOParser


class RTOManagerDialog(QDialog):
    """Dialog for managing .rto (ratio) files"""
    
    def __init__(self, car_data_path, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.car_data_path = car_data_path
        self.final_rto_path = os.path.join(car_data_path, 'final.rto')
        self.ratios_rto_path = os.path.join(car_data_path, 'ratios.rto')
        
        self.final_parser = RTOParser(self.final_rto_path)
        self.ratios_parser = RTOParser(self.ratios_rto_path)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("RTO File Manager - Gear Ratio Options")
        self.setGeometry(200, 150, 700, 500)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel(
            "📊 Manage selectable gear ratios for in-game setup.\n"
            "These files define alternative ratios players can choose from in the setup menu."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background-color: #E3F2FD; padding: 10px; border-radius: 5px;")
        layout.addWidget(info_label)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Final ratios tab
        final_tab = self.create_final_tab()
        self.tabs.addTab(final_tab, "Final Drive Ratios (final.rto)")
        
        # Gear sets tab
        ratios_tab = self.create_ratios_tab()
        self.tabs.addTab(ratios_tab, "Alternative Gear Sets (ratios.rto)")
        
        layout.addWidget(self.tabs)
        
        # Button bar
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save All Changes")
        save_btn.clicked.connect(self.save_all)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        btn_layout.addWidget(save_btn)
        
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def create_final_tab(self):
        """Create the final drive ratios tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Description
        desc = QLabel(
            "Final drive ratio options. These multiply all gear ratios.\n"
            "Higher values = more acceleration, lower top speed."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # List and controls
        list_layout = QHBoxLayout()
        
        # List widget
        self.final_list = QListWidget()
        self.final_list.currentRowChanged.connect(self.on_final_selected)
        list_layout.addWidget(self.final_list)
        
        # Control buttons
        btn_layout = QVBoxLayout()
        
        add_btn = QPushButton("➕ Add")
        add_btn.clicked.connect(self.add_final_ratio)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.clicked.connect(self.edit_final_ratio)
        btn_layout.addWidget(edit_btn)
        
        remove_btn = QPushButton("❌ Remove")
        remove_btn.clicked.connect(self.remove_final_ratio)
        btn_layout.addWidget(remove_btn)
        
        btn_layout.addSpacing(20)
        
        sort_btn = QPushButton("🔄 Sort")
        sort_btn.clicked.connect(self.sort_final_ratios)
        btn_layout.addWidget(sort_btn)
        
        btn_layout.addStretch()
        
        list_layout.addLayout(btn_layout)
        layout.addLayout(list_layout)
        
        # Edit form
        edit_grp = QGroupBox("Edit Selected Ratio")
        edit_form = QFormLayout()
        
        self.final_edit_spin = QDoubleSpinBox()
        self.final_edit_spin.setRange(1.0, 10.0)
        self.final_edit_spin.setDecimals(2)
        self.final_edit_spin.setSingleStep(0.05)
        self.final_edit_spin.valueChanged.connect(self.update_final_ratio)
        edit_form.addRow("Ratio Value:", self.final_edit_spin)
        
        edit_grp.setLayout(edit_form)
        layout.addWidget(edit_grp)
        
        # File status
        self.final_status = QLabel()
        layout.addWidget(self.final_status)
        
        return widget
    
    def create_ratios_tab(self):
        """Create the alternative gear sets tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Description
        desc = QLabel(
            "Complete gear set alternatives (individual gear ratios).\n"
            "Each entry represents a full set of gear ratios."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # List and controls
        list_layout = QHBoxLayout()
        
        # List widget
        self.ratios_list = QListWidget()
        self.ratios_list.currentRowChanged.connect(self.on_ratios_selected)
        list_layout.addWidget(self.ratios_list)
        
        # Control buttons
        btn_layout = QVBoxLayout()
        
        add_btn = QPushButton("➕ Add")
        add_btn.clicked.connect(self.add_gear_ratio)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.clicked.connect(self.edit_gear_ratio)
        btn_layout.addWidget(edit_btn)
        
        remove_btn = QPushButton("❌ Remove")
        remove_btn.clicked.connect(self.remove_gear_ratio)
        btn_layout.addWidget(remove_btn)
        
        btn_layout.addSpacing(20)
        
        sort_btn = QPushButton("🔄 Sort")
        sort_btn.clicked.connect(self.sort_gear_ratios)
        btn_layout.addWidget(sort_btn)
        
        btn_layout.addStretch()
        
        list_layout.addLayout(btn_layout)
        layout.addLayout(list_layout)
        
        # Edit form
        edit_grp = QGroupBox("Edit Selected Ratio")
        edit_form = QFormLayout()
        
        self.ratios_edit_spin = QDoubleSpinBox()
        self.ratios_edit_spin.setRange(0.5, 10.0)
        self.ratios_edit_spin.setDecimals(3)
        self.ratios_edit_spin.setSingleStep(0.1)
        self.ratios_edit_spin.valueChanged.connect(self.update_gear_ratio)
        edit_form.addRow("Ratio Value:", self.ratios_edit_spin)
        
        edit_grp.setLayout(edit_form)
        layout.addWidget(edit_grp)
        
        # File status
        self.ratios_status = QLabel()
        layout.addWidget(self.ratios_status)
        
        return widget
    
    def load_data(self):
        """Load data from .rto files"""
        # Load final ratios
        self.final_list.clear()
        final_ratios = self.final_parser.get_ratios()
        for ratio in final_ratios:
            self.final_list.addItem(f"{ratio:.2f}")
        
        # Update status
        if os.path.exists(self.final_rto_path):
            self.final_status.setText(f"✅ File: {os.path.basename(self.final_rto_path)} ({len(final_ratios)} ratios)")
        else:
            self.final_status.setText(f"⚠️ File: {os.path.basename(self.final_rto_path)} (not found - will be created on save)")
        
        # Load gear ratios
        self.ratios_list.clear()
        gear_ratios = self.ratios_parser.get_ratios()
        for ratio in gear_ratios:
            self.ratios_list.addItem(f"{ratio:.3f}")
        
        # Update status
        if os.path.exists(self.ratios_rto_path):
            self.ratios_status.setText(f"✅ File: {os.path.basename(self.ratios_rto_path)} ({len(gear_ratios)} ratios)")
        else:
            self.ratios_status.setText(f"⚠️ File: {os.path.basename(self.ratios_rto_path)} (not found - will be created on save)")
    
    # Final ratios methods
    def on_final_selected(self, row):
        """Handle final ratio selection"""
        if row >= 0:
            ratios = self.final_parser.get_ratios()
            if row < len(ratios):
                self.final_edit_spin.blockSignals(True)
                self.final_edit_spin.setValue(ratios[row])
                self.final_edit_spin.blockSignals(False)
    
    def add_final_ratio(self):
        """Add a new final ratio"""
        self.final_parser.add_ratio(4.00)
        self.load_data()
        self.final_list.setCurrentRow(self.final_list.count() - 1)
    
    def edit_final_ratio(self):
        """Edit selected final ratio (via spinbox)"""
        row = self.final_list.currentRow()
        if row >= 0:
            self.final_edit_spin.setFocus()
            self.final_edit_spin.selectAll()
    
    def remove_final_ratio(self):
        """Remove selected final ratio"""
        row = self.final_list.currentRow()
        if row >= 0:
            self.final_parser.remove_ratio(row)
            self.load_data()
    
    def update_final_ratio(self, value):
        """Update final ratio from spinbox"""
        row = self.final_list.currentRow()
        if row >= 0:
            self.final_parser.update_ratio(row, value)
            self.final_list.item(row).setText(f"{value:.2f}")
    
    def sort_final_ratios(self):
        """Sort final ratios in descending order"""
        self.final_parser.sort_ratios(reverse=True)
        self.load_data()
    
    # Gear ratios methods
    def on_ratios_selected(self, row):
        """Handle gear ratio selection"""
        if row >= 0:
            ratios = self.ratios_parser.get_ratios()
            if row < len(ratios):
                self.ratios_edit_spin.blockSignals(True)
                self.ratios_edit_spin.setValue(ratios[row])
                self.ratios_edit_spin.blockSignals(False)
    
    def add_gear_ratio(self):
        """Add a new gear ratio"""
        self.ratios_parser.add_ratio(3.00)
        self.load_data()
        self.ratios_list.setCurrentRow(self.ratios_list.count() - 1)
    
    def edit_gear_ratio(self):
        """Edit selected gear ratio (via spinbox)"""
        row = self.ratios_list.currentRow()
        if row >= 0:
            self.ratios_edit_spin.setFocus()
            self.ratios_edit_spin.selectAll()
    
    def remove_gear_ratio(self):
        """Remove selected gear ratio"""
        row = self.ratios_list.currentRow()
        if row >= 0:
            self.ratios_parser.remove_ratio(row)
            self.load_data()
    
    def update_gear_ratio(self, value):
        """Update gear ratio from spinbox"""
        row = self.ratios_list.currentRow()
        if row >= 0:
            self.ratios_parser.update_ratio(row, value)
            self.ratios_list.item(row).setText(f"{value:.3f}")
    
    def sort_gear_ratios(self):
        """Sort gear ratios in descending order"""
        self.ratios_parser.sort_ratios(reverse=True)
        self.load_data()
    
    def save_all(self):
        """Save all changes"""
        try:
            # Save final ratios
            if len(self.final_parser.get_ratios()) > 0:
                self.final_parser.save(backup=True)
            
            # Save gear ratios
            if len(self.ratios_parser.get_ratios()) > 0:
                self.ratios_parser.save(backup=True)
            
            QMessageBox.information(
                self,
                "Success",
                "RTO files saved successfully!\n"
                "Backups created with .bak extension."
            )
            self.load_data()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving",
                f"Failed to save RTO files:\n{str(e)}"
            )
