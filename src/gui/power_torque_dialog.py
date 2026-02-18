"""
Power/Torque Calculator Dialog for AC Car Editor.

Displays interactive power (HP) and torque (Nm) curves derived from
power.lut (which stores torque in Nm) and turbo parameters,
using matplotlib embedded in a PyQt5 dialog.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QFormLayout, QPushButton, QWidget
)
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from core.power_calculator import PowerTorqueCalculator


class PowerTorqueDialog(QDialog):
    """Dialog showing real-time power and torque curves."""

    def __init__(self, torque_points, turbo_configs=None, parent=None):
        """
        Args:
            torque_points: List of (RPM, Nm) from power.lut
            turbo_configs: List of turbo config dicts (max_boost, reference_rpm, gamma, wastegate)
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Power / Torque Calculator")
        self.setMinimumSize(900, 600)

        self.calculator = PowerTorqueCalculator(torque_points, turbo_configs)
        self.has_turbo = bool(turbo_configs)

        self._build_ui()
        self._update_chart()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # --- Chart ---
        self.figure = Figure(figsize=(9, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # --- Stats panel ---
        stats_layout = QHBoxLayout()

        if self.has_turbo:
            # NA stats
            na_grp = QGroupBox("Naturally Aspirated (base)")
            na_form = QFormLayout()
            self.lbl_na_peak_hp = QLabel()
            self.lbl_na_peak_tq = QLabel()
            na_form.addRow("Peak Power:", self.lbl_na_peak_hp)
            na_form.addRow("Peak Torque:", self.lbl_na_peak_tq)
            na_grp.setLayout(na_form)
            stats_layout.addWidget(na_grp)

            # Turbo stats
            turbo_grp = QGroupBox("With Turbo")
            turbo_form = QFormLayout()
            self.lbl_turbo_peak_hp = QLabel()
            self.lbl_turbo_peak_tq = QLabel()
            turbo_form.addRow("Peak Power:", self.lbl_turbo_peak_hp)
            turbo_form.addRow("Peak Torque:", self.lbl_turbo_peak_tq)
            turbo_grp.setLayout(turbo_form)
            stats_layout.addWidget(turbo_grp)
        else:
            na_grp = QGroupBox("Engine Stats")
            na_form = QFormLayout()
            self.lbl_na_peak_hp = QLabel()
            self.lbl_na_peak_tq = QLabel()
            na_form.addRow("Peak Power:", self.lbl_na_peak_hp)
            na_form.addRow("Peak Torque:", self.lbl_na_peak_tq)
            na_grp.setLayout(na_form)
            stats_layout.addWidget(na_grp)

        layout.addLayout(stats_layout)

        # --- Close button ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def _update_chart(self):
        data = self.calculator.compute_curves(rpm_step=50)

        self.figure.clear()
        rpm = data['rpm_values']
        if not rpm:
            return

        ax1 = self.figure.add_subplot(111)
        ax2 = ax1.twinx()

        # Base curves
        ax1.plot(rpm, data['base_hp'], 'b-', linewidth=1.5, label='Power (NA) [HP]')
        ax2.plot(rpm, data['base_torque'], 'r--', linewidth=1.5, label='Torque (NA) [Nm]')

        if self.has_turbo:
            ax1.plot(rpm, data['effective_hp'], 'b-', linewidth=2.5, alpha=0.8,
                     label='Power (Turbo) [HP]')
            ax2.plot(rpm, data['effective_torque'], 'r-', linewidth=2.5, alpha=0.8,
                     label='Torque (Turbo) [Nm]')

        ax1.set_xlabel('RPM')
        ax1.set_ylabel('Power [HP]', color='blue')
        ax2.set_ylabel('Torque [Nm]', color='red')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax2.tick_params(axis='y', labelcolor='red')

        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

        ax1.grid(True, alpha=0.3)
        title = "Power & Torque Curves"
        if self.has_turbo:
            title += "  (NA vs Turbo)"
        ax1.set_title(title)

        self.figure.tight_layout()
        self.canvas.draw()

        # Update stats labels
        pbhp = data['peak_base_hp']
        pbtq = data['peak_base_torque']
        self.lbl_na_peak_hp.setText(f"{pbhp[1]:.1f} HP @ {pbhp[0]:.0f} RPM")
        self.lbl_na_peak_tq.setText(f"{pbtq[1]:.1f} Nm @ {pbtq[0]:.0f} RPM")

        if self.has_turbo:
            pehp = data['peak_eff_hp']
            petq = data['peak_eff_torque']
            self.lbl_turbo_peak_hp.setText(f"{pehp[1]:.1f} HP @ {pehp[0]:.0f} RPM")
            self.lbl_turbo_peak_tq.setText(f"{petq[1]:.1f} Nm @ {petq[0]:.0f} RPM")
