"""
Setup Manager Dialog for AC Car Editor.

Allows users to view setup.ini parameters, save track-specific presets,
and load/delete saved presets.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QFormLayout, QPushButton, QTabWidget, QWidget,
    QDoubleSpinBox, QListWidget, QInputDialog, QMessageBox,
    QScrollArea, QSplitter
)
from PyQt5.QtCore import Qt

from core.setup_manager import SetupManager
from gui.theme import btn_accent
from gui.toast import show_toast


class SetupManagerDialog(QDialog):
    """Dialog for managing track-specific car setups."""

    def __init__(self, car_data_path, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Setup Manager")
        self.setMinimumSize(800, 600)

        self.manager = SetupManager(car_data_path)
        self.param_widgets = {}

        self._build_ui()
        self._refresh_preset_list()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        if not self.manager.has_setup_ini():
            layout.addWidget(QLabel("No setup.ini found for this car.\n"
                                    "Setup parameters are not available."))
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(self.reject)
            layout.addWidget(close_btn)
            return

        splitter = QSplitter(Qt.Horizontal)

        # --- Left: parameter tabs ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        left_layout.addWidget(QLabel("<b>Setup Parameters</b>  (setup.ini)"))

        self.param_tabs = QTabWidget()
        tabs = self.manager.get_tabs()
        for tab_name in tabs:
            params = self.manager.get_parameters_by_tab(tab_name)
            if not params:
                continue
            tab_widget = QWidget()
            form = QFormLayout(tab_widget)
            for p in params:
                spin = QDoubleSpinBox()
                spin.setRange(p['min'], p['max'])
                step = p['step']
                if step >= 1:
                    spin.setDecimals(0)
                elif step >= 0.1:
                    spin.setDecimals(1)
                else:
                    spin.setDecimals(2)
                spin.setSingleStep(step)
                # Default to midpoint
                mid = (p['min'] + p['max']) / 2.0
                spin.setValue(mid)
                if p['help']:
                    spin.setToolTip(p['help'])
                form.addRow(f"{p['name']}:", spin)
                self.param_widgets[p['section']] = spin

            scroll = QScrollArea()
            scroll.setWidget(tab_widget)
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.param_tabs.addTab(scroll, tab_name)

        left_layout.addWidget(self.param_tabs)
        splitter.addWidget(left_widget)

        # --- Right: preset management ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        right_layout.addWidget(QLabel("<b>Saved Presets</b>  (track setups)"))

        self.preset_list = QListWidget()
        right_layout.addWidget(self.preset_list)

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save Current...")
        save_btn.clicked.connect(self._on_save_preset)
        save_btn.setStyleSheet(btn_accent())
        btn_row.addWidget(save_btn)

        load_btn = QPushButton("Load Selected")
        load_btn.clicked.connect(self._on_load_preset)
        btn_row.addWidget(load_btn)

        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self._on_delete_preset)
        btn_row.addWidget(del_btn)
        right_layout.addLayout(btn_row)

        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

        # --- Close ---
        close_row = QHBoxLayout()
        close_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_row.addWidget(close_btn)
        layout.addLayout(close_row)

    def _refresh_preset_list(self):
        self.preset_list.clear()
        for name in self.manager.list_presets():
            self.preset_list.addItem(name)

    def _current_values(self):
        """Collect current widget values into a dict."""
        return {section: w.value() for section, w in self.param_widgets.items()}

    def _on_save_preset(self):
        name, ok = QInputDialog.getText(self, "Save Setup Preset",
                                        "Enter track / preset name:")
        if not ok or not name.strip():
            return
        name = name.strip()
        values = self._current_values()
        if self.manager.save_preset(name, values):
            show_toast(self, f"✅  Preset '{name}' saved.", kind='success')
            self._refresh_preset_list()
        else:
            QMessageBox.warning(self, "Error", f"Failed to save preset '{name}'.")

    def _on_load_preset(self):
        item = self.preset_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Select a preset to load.")
            return
        name = item.text()
        values = self.manager.load_preset(name)
        if values is None:
            QMessageBox.warning(self, "Error", f"Failed to load preset '{name}'.")
            return
        for section, val in values.items():
            widget = self.param_widgets.get(section)
            if widget:
                widget.setValue(val)
        show_toast(self, f"✅  Preset '{name}' applied.", kind='success')

    def _on_delete_preset(self):
        item = self.preset_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Select a preset to delete.")
            return
        name = item.text()
        reply = QMessageBox.question(self, "Delete Preset",
                                     f"Delete preset '{name}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.manager.delete_preset(name):
                self._refresh_preset_list()
