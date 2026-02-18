"""
Car Editor Dialog - Main editor window for modifying car parameters.
Based on real Assetto Corsa file formats (engine.ini, suspensions.ini,
drivetrain.ini, car.ini, aero.ini, brakes.ini).
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QMessageBox, QWidget, QGroupBox,
    QFormLayout, QLabel, QDoubleSpinBox,
    QSpinBox, QComboBox, QCheckBox, QScrollArea
)
from PyQt5.QtCore import Qt

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.ini_parser import IniParser
from core.lut_parser import LUTCurve
from gui.curve_editor_dialog import CurveEditorDialog
from gui.component_selector_dialog import ComponentSelectorDialog


def _tip(widget, text):
    """Attach a tooltip to a widget and return it."""
    widget.setToolTip(text)
    return widget


class CarEditorDialog(QDialog):
    """Dialog for editing car parameters based on real AC file formats."""

    def __init__(self, car_name, car_data_path, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.car_name = car_name
        self.car_data_path = car_data_path
        self.original_values = {}

        self.engine_ini = None
        self.suspension_ini = None
        self.drivetrain_ini = None
        self.car_ini = None
        self.aero_ini = None
        self.brakes_ini = None

        # Count turbo units present in engine.ini (TURBO_0, TURBO_1, ...)
        self.turbo_count = 0
        # Count wing sections in aero.ini (WING_0, WING_1, ...)
        self.wing_count = 0

        self.init_parsers()
        self.init_ui()
        self.load_data()

    # ------------------------------------------------------------------ parsers

    def init_parsers(self):
        """Load all relevant INI files from the car data folder."""
        for attr, filename in [
            ('engine_ini',     'engine.ini'),
            ('suspension_ini', 'suspensions.ini'),
            ('drivetrain_ini', 'drivetrain.ini'),
            ('car_ini',        'car.ini'),
            ('aero_ini',       'aero.ini'),
            ('brakes_ini',     'brakes.ini'),
        ]:
            path = os.path.join(self.car_data_path, filename)
            if os.path.exists(path):
                try:
                    setattr(self, attr, IniParser(path))
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")

        if self.engine_ini:
            i = 0
            while self.engine_ini.has_section(f'TURBO_{i}'):
                i += 1
            self.turbo_count = i

        if self.aero_ini:
            i = 0
            while self.aero_ini.has_section(f'WING_{i}'):
                i += 1
            self.wing_count = i

    # ------------------------------------------------------------------ UI init

    def _make_scroll(self, widget):
        """Wrap widget in a scroll area (no horizontal scroll)."""
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return scroll

    def init_ui(self):
        """Build the tab widget and button bar."""
        self.setWindowTitle(f"Edit Car: {self.car_name}")
        self.setGeometry(150, 100, 920, 720)
        self.setModal(True)

        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        self.tabs.addTab(self._make_scroll(self.create_engine_tab()),      "Engine")
        self.tabs.addTab(self._make_scroll(self.create_suspension_tab()),  "Suspension")
        self.tabs.addTab(self._make_scroll(self.create_drivetrain_tab()),  "Drivetrain")
        self.tabs.addTab(self._make_scroll(self.create_weight_tab()),      "Weight & Fuel")
        self.tabs.addTab(self._make_scroll(self.create_aero_tab()),        "Aerodynamics")
        self.tabs.addTab(self._make_scroll(self.create_brakes_tab()),      "Brakes")

        layout.addWidget(self.tabs)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_changes)
        btn_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_values)
        btn_layout.addWidget(self.reset_btn)

        btn_layout.addStretch()

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)

    # ------------------------------------------------------------------ Engine tab

    def create_engine_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # --- Basic engine data ---
        basic_grp = QGroupBox("Engine Data  (engine.ini › ENGINE_DATA)")
        basic_form = QFormLayout()

        self.minimum_rpm = _tip(QSpinBox(), "Idle RPM — minimum engine speed the simulation allows. "
                                "Typical: 600–1200 RPM.  (MINIMUM)")
        self.minimum_rpm.setRange(0, 5000)
        self.minimum_rpm.setSuffix(" RPM")
        basic_form.addRow("Idle RPM:", self.minimum_rpm)

        self.limiter_rpm = _tip(QSpinBox(), "Rev limiter — hard cut RPM ceiling. The game cuts fuel/ignition above this. "
                                "Typical NA: 6000–9000, turbo: 5500–7500.  (LIMITER)")
        self.limiter_rpm.setRange(1000, 25000)
        self.limiter_rpm.setSuffix(" RPM")
        basic_form.addRow("Rev Limiter:", self.limiter_rpm)

        self.limiter_hz = _tip(QSpinBox(),
                               "Limiter activation frequency in Hz.\n"
                               "Controls how quickly the limiter cycles on/off.\n"
                               "Typical: 20–50 Hz.  (LIMITER_HZ)")
        self.limiter_hz.setRange(1, 200)
        self.limiter_hz.setSuffix(" Hz")
        basic_form.addRow("Limiter Frequency:", self.limiter_hz)

        self.engine_inertia = _tip(QDoubleSpinBox(),
                                   "Engine rotational inertia in kg·m².\n"
                                   "Lower = throttle response feels snappier.\n"
                                   "Typical: 0.08–0.15 (4-cyl), 0.15–0.25 (6-cyl), 0.25–0.50 (V8+).  (INERTIA)")
        self.engine_inertia.setRange(0.01, 5.0)
        self.engine_inertia.setDecimals(4)
        self.engine_inertia.setSingleStep(0.01)
        basic_form.addRow("Engine Inertia:", self.engine_inertia)

        self.altitude_sensitivity = _tip(QDoubleSpinBox(),
                                         "Power loss fraction per 1000 m of altitude.\n"
                                         "Naturally aspirated: ~0.1 (10% per 1000 m).\n"
                                         "Turbocharged: 0.0–0.04 (turbo compensates).  (ALTITUDE_SENSITIVITY)")
        self.altitude_sensitivity.setRange(0.0, 1.0)
        self.altitude_sensitivity.setDecimals(3)
        self.altitude_sensitivity.setSingleStep(0.01)
        basic_form.addRow("Altitude Sensitivity:", self.altitude_sensitivity)

        self.default_turbo_adj = _tip(QDoubleSpinBox(),
                                      "Default turbo adjustment value if boost is cockpit-adjustable.\n"
                                      "Range 0.0–1.0.  Typical: 0.7 (70% of max boost).  (DEFAULT_TURBO_ADJUSTMENT)")
        self.default_turbo_adj.setRange(0.0, 1.0)
        self.default_turbo_adj.setDecimals(2)
        self.default_turbo_adj.setSingleStep(0.05)
        basic_form.addRow("Default Turbo Adj:", self.default_turbo_adj)

        basic_grp.setLayout(basic_form)
        layout.addWidget(basic_grp)

        # --- Coast / engine braking reference ---
        coast_grp = QGroupBox("Engine Braking Reference  (engine.ini › COAST_REF)")
        coast_form = QFormLayout()

        self.coast_ref_rpm = _tip(QSpinBox(),
                                  "RPM at which the engine drag torque is measured.\n"
                                  "Typically set equal to LIMITER.  (RPM)")
        self.coast_ref_rpm.setRange(0, 25000)
        self.coast_ref_rpm.setSuffix(" RPM")
        coast_form.addRow("Reference RPM:", self.coast_ref_rpm)

        self.coast_ref_torque = _tip(QDoubleSpinBox(),
                                     "Engine drag torque at reference RPM.\n"
                                     "Higher = stronger engine braking feel.\n"
                                     "Typical: 30–120 Nm.  (TORQUE)")
        self.coast_ref_torque.setRange(0, 500)
        self.coast_ref_torque.setDecimals(1)
        self.coast_ref_torque.setSuffix(" Nm")
        coast_form.addRow("Drag Torque:", self.coast_ref_torque)

        self.coast_non_linearity = _tip(QDoubleSpinBox(),
                                        "Non-linearity of the coast curve.\n"
                                        "0 = perfectly linear, 1 = very non-linear (sudden engine brake at low RPM).\n"
                                        "Typical: 0.  (NON_LINEARITY)")
        self.coast_non_linearity.setRange(0, 1.0)
        self.coast_non_linearity.setDecimals(3)
        self.coast_non_linearity.setSingleStep(0.01)
        coast_form.addRow("Non-Linearity:", self.coast_non_linearity)

        coast_grp.setLayout(coast_form)
        layout.addWidget(coast_grp)

        # --- Forced induction ---
        fi_grp = QGroupBox("Forced Induction  (engine.ini › TURBO_N)")
        fi_layout = QVBoxLayout()

        self.has_turbo_check = _tip(QCheckBox("Car has forced induction (turbo/supercharger)"),
                                    "When enabled the TURBO_0 (and optionally TURBO_1/2) sections will be saved.\n"
                                    "Uncheck for naturally aspirated engines.")
        self.has_turbo_check.stateChanged.connect(self._on_turbo_toggle)
        fi_layout.addWidget(self.has_turbo_check)

        count_row = QHBoxLayout()
        count_row.addWidget(QLabel("Number of turbo units:"))
        self.turbo_count_combo = _tip(QComboBox(),
                                      "1 = single turbo (TURBO_0)\n"
                                      "2 = twin turbo (TURBO_0 + TURBO_1)\n"
                                      "3 = triple turbo (TURBO_0–2)")
        self.turbo_count_combo.addItems(["1 — Single", "2 — Twin", "3 — Triple"])
        self.turbo_count_combo.setEnabled(False)
        self.turbo_count_combo.currentIndexChanged.connect(self._on_turbo_count_changed)
        count_row.addWidget(self.turbo_count_combo)
        count_row.addStretch()
        fi_layout.addLayout(count_row)

        self.turbo_0_widget = self._create_turbo_widget(0)
        self.turbo_0_widget.setVisible(False)
        fi_layout.addWidget(self.turbo_0_widget)

        self.turbo_1_widget = self._create_turbo_widget(1)
        self.turbo_1_widget.setVisible(False)
        fi_layout.addWidget(self.turbo_1_widget)

        self.turbo_2_widget = self._create_turbo_widget(2)
        self.turbo_2_widget.setVisible(False)
        fi_layout.addWidget(self.turbo_2_widget)

        fi_grp.setLayout(fi_layout)
        layout.addWidget(fi_grp)

        # --- Engine Damage ---
        dmg_grp = QGroupBox("Engine Damage  (engine.ini › DAMAGE)")
        dmg_form = QFormLayout()

        self.turbo_boost_threshold = _tip(QDoubleSpinBox(),
                                          "Boost pressure above which the engine takes damage.\n"
                                          "Set above MAX_BOOST to allow some overboost before damage.  (TURBO_BOOST_THRESHOLD)")
        self.turbo_boost_threshold.setRange(0, 10.0); self.turbo_boost_threshold.setDecimals(2); self.turbo_boost_threshold.setSingleStep(0.1); self.turbo_boost_threshold.setSuffix(" bar")
        dmg_form.addRow("Turbo Damage Threshold:", self.turbo_boost_threshold)

        self.turbo_damage_k = _tip(QDoubleSpinBox(),
                                    "Damage rate per second for each bar of boost over threshold.\n"
                                    "Higher = faster engine destruction.  (TURBO_DAMAGE_K)")
        self.turbo_damage_k.setRange(0, 100); self.turbo_damage_k.setDecimals(1); self.turbo_damage_k.setSingleStep(0.5)
        dmg_form.addRow("Turbo Damage Rate:", self.turbo_damage_k)

        self.rpm_threshold = _tip(QSpinBox(),
                                   "RPM above which the engine takes damage.\n"
                                   "Usually set above LIMITER by 200–500 RPM.  (RPM_THRESHOLD)")
        self.rpm_threshold.setRange(0, 30000); self.rpm_threshold.setSuffix(" RPM")
        dmg_form.addRow("RPM Damage Threshold:", self.rpm_threshold)

        self.rpm_damage_k = _tip(QDoubleSpinBox(),
                                  "Damage rate per second for each RPM over threshold.\n"
                                  "Typical: 1.  (RPM_DAMAGE_K)")
        self.rpm_damage_k.setRange(0, 100); self.rpm_damage_k.setDecimals(1); self.rpm_damage_k.setSingleStep(0.5)
        dmg_form.addRow("RPM Damage Rate:", self.rpm_damage_k)

        dmg_grp.setLayout(dmg_form)
        layout.addWidget(dmg_grp)

        # --- Library import ---
        import_btn = QPushButton("Import Engine from Library...")
        import_btn.clicked.connect(self.import_engine_component)
        import_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        layout.addWidget(import_btn)

        # --- Curves ---
        curve_grp = QGroupBox("Power & Coast Curves")
        curve_layout = QVBoxLayout()

        power_btn = QPushButton("Edit Power Curve (power.lut)  ·  RPM → HP")
        power_btn.clicked.connect(self.edit_power_curve)
        curve_layout.addWidget(power_btn)

        coast_btn = QPushButton("Edit Coast Curve (coast.lut)  ·  RPM → drag Nm")
        coast_btn.clicked.connect(self.edit_coast_curve)
        curve_layout.addWidget(coast_btn)

        curve_grp.setLayout(curve_layout)
        layout.addWidget(curve_grp)

        layout.addStretch()
        return widget

    def _create_turbo_widget(self, index):
        """Build a QGroupBox with all parameters for one TURBO_N section."""
        gb = QGroupBox(f"Turbo {index + 1}  (TURBO_{index})")
        form = QFormLayout()

        max_boost = _tip(QDoubleSpinBox(),
                         "Maximum boost pressure in bar.\n"
                         "Stock cars: 0.5–1.5 bar.  Race/tuned: 1.5–3.0+ bar.  (MAX_BOOST)")
        max_boost.setRange(0, 6.0); max_boost.setDecimals(3); max_boost.setSingleStep(0.05); max_boost.setSuffix(" bar")
        form.addRow("Max Boost:", max_boost)

        wastegate = _tip(QDoubleSpinBox(),
                         "Wastegate opening pressure.\n"
                         "Should equal MAX_BOOST for stock maps.\n"
                         "Higher than MAX_BOOST = boost creep simulation.  (WASTEGATE)")
        wastegate.setRange(0, 6.0); wastegate.setDecimals(3); wastegate.setSingleStep(0.05); wastegate.setSuffix(" bar")
        form.addRow("Wastegate:", wastegate)

        display_max = _tip(QDoubleSpinBox(),
                           "Value shown in the cockpit boost gauge.\n"
                           "Usually matches MAX_BOOST.  (DISPLAY_MAX_BOOST)")
        display_max.setRange(0, 6.0); display_max.setDecimals(3); display_max.setSingleStep(0.05); display_max.setSuffix(" bar")
        form.addRow("Display Max Boost:", display_max)

        lag_up = _tip(QDoubleSpinBox(),
                      "Spool-up lag factor (0–1). Closer to 1.0 = slower spool.\n"
                      "Fast turbo: 0.950–0.975.  Laggy: 0.980–0.995.  (LAG_UP)")
        lag_up.setRange(0.5, 1.0); lag_up.setDecimals(4); lag_up.setSingleStep(0.001)
        form.addRow("Spool-Up Lag:", lag_up)

        lag_dn = _tip(QDoubleSpinBox(),
                      "Spool-down lag factor. Closer to 1.0 = boost bleeds off slowly.\n"
                      "Typical: 0.975–0.990.  (LAG_DN)")
        lag_dn.setRange(0.5, 1.0); lag_dn.setDecimals(4); lag_dn.setSingleStep(0.001)
        form.addRow("Spool-Down Lag:", lag_dn)

        ref_rpm = _tip(QSpinBox(),
                       "RPM at which full boost is produced.\n"
                       "Lower = less turbo lag.  Typical: 2500–4500 RPM.  (REFERENCE_RPM)")
        ref_rpm.setRange(0, 12000); ref_rpm.setSuffix(" RPM")
        form.addRow("Full Boost RPM:", ref_rpm)

        gamma = _tip(QDoubleSpinBox(),
                     "Boost curve shape exponent.\n"
                     "Higher = sharper onset above REFERENCE_RPM.\n"
                     "Typical: 1.5–3.0.  (GAMMA)")
        gamma.setRange(0.5, 8.0); gamma.setDecimals(2); gamma.setSingleStep(0.1)
        form.addRow("Boost Curve Gamma:", gamma)

        cockpit_adj = _tip(QCheckBox("Cockpit Adjustable"),
                           "Allow boost adjustment from in-car controls.  (COCKPIT_ADJUSTABLE)")
        form.addRow("", cockpit_adj)

        gb.setLayout(form)

        setattr(self, f'turbo_{index}_max_boost',       max_boost)
        setattr(self, f'turbo_{index}_wastegate',       wastegate)
        setattr(self, f'turbo_{index}_display_max',     display_max)
        setattr(self, f'turbo_{index}_lag_up',          lag_up)
        setattr(self, f'turbo_{index}_lag_dn',          lag_dn)
        setattr(self, f'turbo_{index}_ref_rpm',         ref_rpm)
        setattr(self, f'turbo_{index}_gamma',           gamma)
        setattr(self, f'turbo_{index}_cockpit_adj',     cockpit_adj)
        return gb

    def _on_turbo_toggle(self, state):
        enabled = (state == Qt.Checked)
        self.turbo_count_combo.setEnabled(enabled)
        self.turbo_0_widget.setVisible(enabled)
        if enabled:
            self._on_turbo_count_changed(self.turbo_count_combo.currentIndex())
        else:
            self.turbo_1_widget.setVisible(False)
            self.turbo_2_widget.setVisible(False)

    def _on_turbo_count_changed(self, index):
        if not self.has_turbo_check.isChecked():
            return
        self.turbo_1_widget.setVisible(index >= 1)
        self.turbo_2_widget.setVisible(index >= 2)

    # ------------------------------------------------------------------ Suspension tab

    def create_suspension_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # --- ARB ---
        arb_grp = QGroupBox("Anti-Roll Bars  (suspensions.ini › ARB)")
        arb_form = QFormLayout()

        self.arb_front = _tip(QDoubleSpinBox(),
                              "Front ARB stiffness in Nm/rad.\n"
                              "Higher = less body roll but more understeer tendency.\n"
                              "Street: 5 000–50 000 · Race: up to 200 000+  (FRONT)")
        self.arb_front.setRange(0, 500000); self.arb_front.setDecimals(0); self.arb_front.setSuffix(" Nm/rad")
        arb_form.addRow("Front ARB:", self.arb_front)

        self.arb_rear = _tip(QDoubleSpinBox(),
                             "Rear ARB stiffness in Nm/rad.\n"
                             "Higher = less roll but more oversteer tendency.  (REAR)")
        self.arb_rear.setRange(0, 500000); self.arb_rear.setDecimals(0); self.arb_rear.setSuffix(" Nm/rad")
        arb_form.addRow("Rear ARB:", self.arb_rear)

        arb_grp.setLayout(arb_form)
        layout.addWidget(arb_grp)

        # --- Front & Rear axle groups ---
        for axle_label, prefix, section in [("Front Suspension", "front", "FRONT"),
                                             ("Rear Suspension",  "rear",  "REAR")]:
            grp = QGroupBox(f"{axle_label}  (suspensions.ini › {section})")
            form = QFormLayout()

            spring = _tip(QDoubleSpinBox(),
                          "Wheel spring rate (N/m).\n"
                          "Use wheel rate, NOT coil spring rate.\n"
                          "Street: 15 000–80 000 · Race: 80 000–300 000+  (SPRING_RATE)")
            spring.setRange(0, 600000); spring.setDecimals(0); spring.setSuffix(" N/m")
            form.addRow("Spring Rate:", spring)
            setattr(self, f'{prefix}_spring_rate', spring)

            prog = _tip(QDoubleSpinBox(),
                        "Progressive spring rate increase per metre of compression.\n"
                        "0 = linear spring.  (PROGRESSIVE_SPRING_RATE)")
            prog.setRange(0, 2000000); prog.setDecimals(0); prog.setSuffix(" N/m/m")
            form.addRow("Progressive Spring:", prog)
            setattr(self, f'{prefix}_progressive_spring', prog)

            damp_bump = _tip(QDoubleSpinBox(),
                             "Slow bump damping — controls body motion over smooth roads.\n"
                             "Typical street: 1 500–4 000 Ns/m.  (DAMP_BUMP)")
            damp_bump.setRange(0, 60000); damp_bump.setDecimals(0); damp_bump.setSuffix(" Ns/m")
            form.addRow("Slow Bump:", damp_bump)
            setattr(self, f'{prefix}_damp_bump', damp_bump)

            damp_fast_bump = _tip(QDoubleSpinBox(),
                                  "Fast bump damping — controls wheel motion over sharp bumps.\n"
                                  "Usually 2–3× slow bump.  (DAMP_FAST_BUMP)")
            damp_fast_bump.setRange(0, 60000); damp_fast_bump.setDecimals(0); damp_fast_bump.setSuffix(" Ns/m")
            form.addRow("Fast Bump:", damp_fast_bump)
            setattr(self, f'{prefix}_damp_fast_bump', damp_fast_bump)

            damp_rebound = _tip(QDoubleSpinBox(),
                                "Slow rebound damping — controls body recovery after compression.\n"
                                "Typically 1.2–2× slow bump.  (DAMP_REBOUND)")
            damp_rebound.setRange(0, 60000); damp_rebound.setDecimals(0); damp_rebound.setSuffix(" Ns/m")
            form.addRow("Slow Rebound:", damp_rebound)
            setattr(self, f'{prefix}_damp_rebound', damp_rebound)

            damp_fast_rebound = _tip(QDoubleSpinBox(),
                                     "Fast rebound damping — controls wheel return speed after a bump.\n"
                                     "Usually higher than fast bump.  (DAMP_FAST_REBOUND)")
            damp_fast_rebound.setRange(0, 60000); damp_fast_rebound.setDecimals(0); damp_fast_rebound.setSuffix(" Ns/m")
            form.addRow("Fast Rebound:", damp_fast_rebound)
            setattr(self, f'{prefix}_damp_fast_rebound', damp_fast_rebound)

            rod = _tip(QDoubleSpinBox(),
                       "Push/pull-rod length offset in metres.\n"
                       "Positive = raises ride height · Negative = lowers it.  (ROD_LENGTH)")
            rod.setRange(-0.5, 0.5); rod.setDecimals(4); rod.setSingleStep(0.001); rod.setSuffix(" m")
            form.addRow("Rod Length:", rod)
            setattr(self, f'{prefix}_rod_length', rod)

            camber = _tip(QDoubleSpinBox(),
                          "Static camber in degrees.\n"
                          "Negative = top of tyre leans inward (most cars).\n"
                          "Street: −0.5 to −2.0°  ·  Race: −2.0 to −4.0°  (STATIC_CAMBER)")
            camber.setRange(-10.0, 5.0); camber.setDecimals(2); camber.setSingleStep(0.1); camber.setSuffix("°")
            form.addRow("Static Camber:", camber)
            setattr(self, f'{prefix}_static_camber', camber)

            toe = _tip(QDoubleSpinBox(),
                       "Toe angle in radians.\n"
                       "Positive = toe-out (front of tyre points outward).\n"
                       "Front typical: 0 to +0.001 · Rear: −0.001 to 0  (TOE_OUT)")
            toe.setRange(-0.1, 0.1); toe.setDecimals(5); toe.setSingleStep(0.0001)
            form.addRow("Toe Out:", toe)
            setattr(self, f'{prefix}_toe_out', toe)

            grp.setLayout(form)
            layout.addWidget(grp)

        import_btn = QPushButton("Import Suspension from Library...")
        import_btn.clicked.connect(self.import_suspension_component)
        import_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        layout.addWidget(import_btn)

        layout.addStretch()
        return widget

    # ------------------------------------------------------------------ Drivetrain tab

    def create_drivetrain_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # --- Traction ---
        traction_grp = QGroupBox("Traction Layout  (drivetrain.ini › TRACTION)")
        traction_form = QFormLayout()

        self.traction_type = _tip(QComboBox(), "Drive wheel configuration.\n"
                                            "AWD2 = advanced AWD with controller (drivetrain.ini VERSION=3).  (TYPE)")
        self.traction_type.addItems(["RWD", "FWD", "AWD", "AWD2"])
        traction_form.addRow("Drive Type:", self.traction_type)

        traction_grp.setLayout(traction_form)
        layout.addWidget(traction_grp)

        # --- Differential ---
        diff_grp = QGroupBox("Differential  (drivetrain.ini › DIFFERENTIAL)")
        diff_form = QFormLayout()

        self.diff_power = _tip(QDoubleSpinBox(),
                               "LSD locking factor under power.\n"
                               "0.0 = open diff · 1.0 = fully locked (spool).\n"
                               "Street: 0.05–0.20 · Race: 0.30–0.80  (POWER)")
        self.diff_power.setRange(0, 1.0); self.diff_power.setDecimals(3); self.diff_power.setSingleStep(0.05)
        diff_form.addRow("Lock on Power:", self.diff_power)

        self.diff_coast = _tip(QDoubleSpinBox(),
                               "LSD locking factor on engine braking.\n"
                               "Higher = more stable but less rotation on corner entry.  (COAST)")
        self.diff_coast.setRange(0, 1.0); self.diff_coast.setDecimals(3); self.diff_coast.setSingleStep(0.05)
        diff_form.addRow("Lock on Coast:", self.diff_coast)

        self.diff_preload = _tip(QDoubleSpinBox(),
                                 "LSD preload torque — keeps diff partially locked even at zero throttle.\n"
                                 "Street: 0–20 Nm · Race: 30–150 Nm  (PRELOAD)")
        self.diff_preload.setRange(0, 500); self.diff_preload.setDecimals(1); self.diff_preload.setSuffix(" Nm")
        diff_form.addRow("Preload:", self.diff_preload)

        diff_grp.setLayout(diff_form)
        layout.addWidget(diff_grp)

        # --- Gearbox ---
        gbox_grp = QGroupBox("Gearbox  (drivetrain.ini › GEARS / GEARBOX)")
        gbox_form = QFormLayout()

        self.gear_count = _tip(QSpinBox(), "Number of forward gears.  (GEARS > COUNT)")
        self.gear_count.setRange(1, 10)
        gbox_form.addRow("Gear Count:", self.gear_count)

        self.final_ratio = _tip(QDoubleSpinBox(),
                                "Final drive ratio.\n"
                                "Higher = more acceleration, lower top speed.  (GEARS > FINAL)")
        self.final_ratio.setRange(1.0, 12.0); self.final_ratio.setDecimals(3); self.final_ratio.setSingleStep(0.05)
        gbox_form.addRow("Final Ratio:", self.final_ratio)

        self.gearbox_up_time = _tip(QSpinBox(),
                                    "Upshift time in milliseconds.\n"
                                    "0 = instantaneous (sequential gearbox).\n"
                                    "H-pattern manual: 200–400 ms  (GEARBOX > CHANGE_UP_TIME)")
        self.gearbox_up_time.setRange(0, 1000); self.gearbox_up_time.setSuffix(" ms")
        gbox_form.addRow("Upshift Time:", self.gearbox_up_time)

        self.gearbox_dn_time = _tip(QSpinBox(),
                                    "Downshift time in milliseconds.\n"
                                    "Usually slightly longer than upshift.  (GEARBOX > CHANGE_DN_TIME)")
        self.gearbox_dn_time.setRange(0, 1000); self.gearbox_dn_time.setSuffix(" ms")
        gbox_form.addRow("Downshift Time:", self.gearbox_dn_time)

        self.gearbox_inertia = _tip(QDoubleSpinBox(),
                                    "Gearbox rotational inertia — affects transmission feel.  (GEARBOX > INERTIA)")
        self.gearbox_inertia.setRange(0, 1.0); self.gearbox_inertia.setDecimals(4); self.gearbox_inertia.setSingleStep(0.001)
        gbox_form.addRow("Gearbox Inertia:", self.gearbox_inertia)

        gbox_grp.setLayout(gbox_form)
        layout.addWidget(gbox_grp)

        # --- Clutch ---
        clutch_grp = QGroupBox("Clutch  (drivetrain.ini › CLUTCH)")
        clutch_form = QFormLayout()

        self.clutch_max_torque = _tip(QDoubleSpinBox(),
                                      "Maximum clutch torque capacity.\n"
                                      "Should exceed engine peak torque to avoid slipping.  (MAX_TORQUE)")
        self.clutch_max_torque.setRange(0, 3000); self.clutch_max_torque.setDecimals(0); self.clutch_max_torque.setSuffix(" Nm")
        clutch_form.addRow("Max Clutch Torque:", self.clutch_max_torque)

        clutch_grp.setLayout(clutch_form)
        layout.addWidget(clutch_grp)

        import_btn = QPushButton("Import Differential from Library...")
        import_btn.clicked.connect(self.import_differential_component)
        import_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        layout.addWidget(import_btn)

        layout.addStretch()
        return widget

    # Keep legacy name for existing references
    def create_differential_tab(self):
        return self.create_drivetrain_tab()

    # ------------------------------------------------------------------ Weight & Fuel tab

    def create_weight_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # --- Mass & Inertia ---
        mass_grp = QGroupBox("Mass & Inertia  (car.ini › BASIC)")
        mass_form = QFormLayout()

        self.total_mass = _tip(QDoubleSpinBox(),
                               "Total vehicle mass including driver.\n"
                               "Street: 900–2000 kg · Race: 600–1000 kg  (TOTALMASS)")
        self.total_mass.setRange(100, 10000); self.total_mass.setDecimals(0); self.total_mass.setSuffix(" kg")
        mass_form.addRow("Total Mass:", self.total_mass)

        self.inertia_x = _tip(QDoubleSpinBox(),
                              "Roll inertia (rotation around longitudinal axis) in t·m².\n"
                              "Affects body lean in direction changes.  (INERTIA[0])")
        self.inertia_x.setRange(0, 50); self.inertia_x.setDecimals(3); self.inertia_x.setSingleStep(0.1); self.inertia_x.setSuffix(" t·m²")
        mass_form.addRow("Roll Inertia:", self.inertia_x)

        self.inertia_y = _tip(QDoubleSpinBox(),
                              "Pitch inertia (rotation around lateral axis) in t·m².\n"
                              "Affects pitch under braking/acceleration.  (INERTIA[1])")
        self.inertia_y.setRange(0, 50); self.inertia_y.setDecimals(3); self.inertia_y.setSingleStep(0.1); self.inertia_y.setSuffix(" t·m²")
        mass_form.addRow("Pitch Inertia:", self.inertia_y)

        self.inertia_z = _tip(QDoubleSpinBox(),
                              "Yaw inertia (rotation around vertical axis) in t·m².\n"
                              "Most important for handling: higher = more stable but slower rotation.  (INERTIA[2])")
        self.inertia_z.setRange(0, 100); self.inertia_z.setDecimals(3); self.inertia_z.setSingleStep(0.1); self.inertia_z.setSuffix(" t·m²")
        mass_form.addRow("Yaw Inertia:", self.inertia_z)

        mass_grp.setLayout(mass_form)
        layout.addWidget(mass_grp)

        # --- Balance & wheelbase ---
        bal_grp = QGroupBox("Weight Distribution & Wheelbase  (suspensions.ini › BASIC)")
        bal_form = QFormLayout()

        self.cg_location = _tip(QDoubleSpinBox(),
                                "Front axle weight distribution as a fraction (0.0–1.0).\n"
                                "0.578 = 57.8% front.  FR cars: 0.47–0.52 · FF: 0.58–0.65.  (CG_LOCATION)")
        self.cg_location.setRange(0.0, 1.0); self.cg_location.setDecimals(4); self.cg_location.setSingleStep(0.01)
        bal_form.addRow("Front Weight Fraction:", self.cg_location)

        self.wheelbase = _tip(QDoubleSpinBox(),
                              "Distance between front and rear axle centres in metres.  (WHEELBASE)")
        self.wheelbase.setRange(1.0, 5.0); self.wheelbase.setDecimals(4); self.wheelbase.setSingleStep(0.01); self.wheelbase.setSuffix(" m")
        bal_form.addRow("Wheelbase:", self.wheelbase)

        bal_grp.setLayout(bal_form)
        layout.addWidget(bal_grp)

        # --- Steering ---
        steer_grp = QGroupBox("Steering  (car.ini › CONTROLS)")
        steer_form = QFormLayout()

        self.steer_lock = _tip(QDoubleSpinBox(),
                               "Steering wheel lock-to-lock angle in degrees.\n"
                               "Street: 400–900° · Race: 200–360°  (STEER_LOCK)")
        self.steer_lock.setRange(90, 1080); self.steer_lock.setDecimals(0); self.steer_lock.setSuffix("°")
        steer_form.addRow("Steering Lock:", self.steer_lock)

        self.steer_ratio = _tip(QDoubleSpinBox(),
                                "Steering gear ratio.\n"
                                "Lower absolute value = more direct.  Negative = inverted side.\n"
                                "Street: 15–18 · Sport: 12–15 · Negative = reversed  (STEER_RATIO)")
        self.steer_ratio.setRange(-25, 25); self.steer_ratio.setDecimals(1); self.steer_ratio.setSingleStep(0.5)
        steer_form.addRow("Steering Ratio:", self.steer_ratio)

        steer_grp.setLayout(steer_form)
        layout.addWidget(steer_grp)

        # --- Fuel ---
        fuel_grp = QGroupBox("Fuel  (car.ini › FUEL)")
        fuel_form = QFormLayout()

        self.fuel_start = _tip(QDoubleSpinBox(), "Default starting fuel load in litres.  (FUEL)")
        self.fuel_start.setRange(0, 300); self.fuel_start.setDecimals(1); self.fuel_start.setSuffix(" L")
        fuel_form.addRow("Starting Fuel:", self.fuel_start)

        self.fuel_max = _tip(QDoubleSpinBox(), "Maximum tank capacity in litres.  (MAX_FUEL)")
        self.fuel_max.setRange(0, 500); self.fuel_max.setDecimals(1); self.fuel_max.setSuffix(" L")
        fuel_form.addRow("Tank Capacity:", self.fuel_max)

        self.fuel_consumption = _tip(QDoubleSpinBox(),
                                     "Fuel consumption in litres per metre of travel.\n"
                                     "Efficient: 0.0003 · Typical: 0.0030 · Race heavy: 0.005+  (CONSUMPTION)")
        self.fuel_consumption.setRange(0, 0.1); self.fuel_consumption.setDecimals(6); self.fuel_consumption.setSingleStep(0.0001)
        fuel_form.addRow("Consumption (L/m):", self.fuel_consumption)

        fuel_grp.setLayout(fuel_form)
        layout.addWidget(fuel_grp)

        layout.addStretch()
        return widget

    # ------------------------------------------------------------------ Aero tab

    def create_aero_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info = QLabel("Assetto Corsa aerodynamics use WING_N sections (WING_0, WING_1…).\n"
                      "WING_0 is typically the car body.  CD = drag coefficient, "
                      "CL = lift (negative value = downforce).")
        info.setWordWrap(True)
        info.setStyleSheet("color: #555; font-style: italic; padding: 4px;")
        layout.addWidget(info)

        self.wing_widgets = []
        if self.wing_count == 0:
            layout.addWidget(QLabel("No aero.ini found or no WING_N sections detected."))
        else:
            for i in range(self.wing_count):
                w = self._create_wing_widget(i)
                self.wing_widgets.append(w)
                layout.addWidget(w)

        import_btn = QPushButton("Import Aero from Library...")
        import_btn.clicked.connect(self.import_aero_component)
        import_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        layout.addWidget(import_btn)

        layout.addStretch()
        return widget

    def _create_wing_widget(self, index):
        name = ''
        if self.aero_ini:
            name = self.aero_ini.get_value(f'WING_{index}', 'NAME', '')
        title = f"Wing {index}: {name}" if name else f"WING_{index}"
        gb = QGroupBox(f"{title}  (aero.ini › WING_{index})")
        form = QFormLayout()

        cd = _tip(QDoubleSpinBox(),
                  f"Drag coefficient for this wing element.\n"
                  f"Body: 0.3–1.0 · Small wings: 0.01–0.5 · Large wings: 0.5–3.0+  (CD)")
        cd.setRange(0, 20.0); cd.setDecimals(4); cd.setSingleStep(0.01)
        form.addRow("Drag (CD):", cd)
        setattr(self, f'wing_{index}_cd', cd)

        cl = _tip(QDoubleSpinBox(),
                  f"Lift coefficient.\n"
                  f"Negative = downforce (most ground-effect/wing elements).\n"
                  f"Positive = lift (road car body WING_0 at speed).  (CL)")
        cl.setRange(-10.0, 10.0); cl.setDecimals(4); cl.setSingleStep(0.01)
        form.addRow("Lift / Downforce (CL):", cl)
        setattr(self, f'wing_{index}_cl', cl)

        angle = _tip(QDoubleSpinBox(),
                     f"Wing angle of attack in degrees.\n"
                     f"Increasing angle raises downforce AND drag.  (ANGLE)")
        angle.setRange(-45, 45); angle.setSuffix("°"); angle.setDecimals(2); angle.setSingleStep(1.0)
        form.addRow("Angle:", angle)
        setattr(self, f'wing_{index}_angle', angle)

        gb.setLayout(form)
        return gb

    # ------------------------------------------------------------------ Brakes tab

    def create_brakes_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        brake_grp = QGroupBox("Brake System  (brakes.ini › DATA)")
        brake_form = QFormLayout()

        self.brake_max_torque = _tip(QDoubleSpinBox(),
                                     "Maximum brake torque per wheel in Nm.\n"
                                     "Street: 1 000–3 000 Nm · Race: 3 000–8 000+ Nm  (MAX_TORQUE)")
        self.brake_max_torque.setRange(0, 12000); self.brake_max_torque.setDecimals(0); self.brake_max_torque.setSuffix(" Nm")
        brake_form.addRow("Max Brake Torque:", self.brake_max_torque)

        self.brake_front_share = _tip(QDoubleSpinBox(),
                                      "Fraction of total braking force applied to the front axle.\n"
                                      "0.64 = 64% front.  Typical street: 0.58–0.70 · Race: 0.55–0.65  (FRONT_SHARE)")
        self.brake_front_share.setRange(0.3, 0.9); self.brake_front_share.setDecimals(3); self.brake_front_share.setSingleStep(0.01)
        brake_form.addRow("Front Brake Bias:", self.brake_front_share)

        self.brake_handbrake = _tip(QDoubleSpinBox(),
                                    "Handbrake torque applied to rear wheels.\n"
                                    "Higher = more aggressive e-brake / handbrake turns.  (HANDBRAKE_TORQUE)")
        self.brake_handbrake.setRange(0, 12000); self.brake_handbrake.setDecimals(0); self.brake_handbrake.setSuffix(" Nm")
        brake_form.addRow("Handbrake Torque:", self.brake_handbrake)

        self.brake_cockpit_adj = _tip(QCheckBox("Cockpit Brake Bias Adjustable"),
                                      "Allow driver to adjust front/rear brake balance from cockpit.  (COCKPIT_ADJUSTABLE)")
        brake_form.addRow("", self.brake_cockpit_adj)

        self.brake_adjust_step = _tip(QDoubleSpinBox(),
                                       "Step size for cockpit brake bias adjustment.\n"
                                       "How much the bias changes per click.  Typical: 0.5–1.0.  (ADJUST_STEP)")
        self.brake_adjust_step.setRange(0.1, 5.0); self.brake_adjust_step.setDecimals(1); self.brake_adjust_step.setSingleStep(0.1)
        brake_form.addRow("Bias Adjust Step:", self.brake_adjust_step)

        brake_grp.setLayout(brake_form)
        layout.addWidget(brake_grp)

        layout.addStretch()
        return widget

    # ------------------------------------------------------------------ Load data

    def load_data(self):
        self._load_engine_data()
        self._load_suspension_data()
        self._load_drivetrain_data()
        self._load_weight_data()
        self._load_aero_data()
        self._load_brakes_data()

    def _load_engine_data(self):
        if not self.engine_ini:
            return

        if self.engine_ini.has_section('ENGINE_DATA'):
            minimum  = int(self.engine_ini.get_value('ENGINE_DATA', 'MINIMUM',  '800'))
            limiter  = int(self.engine_ini.get_value('ENGINE_DATA', 'LIMITER',  '7000'))
            lim_hz   = int(float(self.engine_ini.get_value('ENGINE_DATA', 'LIMITER_HZ', '30')))
            inertia  = float(self.engine_ini.get_value('ENGINE_DATA', 'INERTIA',  '0.15'))
            alt_sens = float(self.engine_ini.get_value('ENGINE_DATA', 'ALTITUDE_SENSITIVITY', '0.1'))
            turbo_adj = float(self.engine_ini.get_value('ENGINE_DATA', 'DEFAULT_TURBO_ADJUSTMENT', '0.7'))

            self.minimum_rpm.setValue(minimum)
            self.limiter_rpm.setValue(limiter)
            self.limiter_hz.setValue(lim_hz)
            self.engine_inertia.setValue(inertia)
            self.altitude_sensitivity.setValue(alt_sens)
            self.default_turbo_adj.setValue(turbo_adj)
            self.original_values.update({'minimum': minimum, 'limiter': limiter, 'limiter_hz': lim_hz,
                                         'engine_inertia': inertia, 'altitude_sensitivity': alt_sens,
                                         'default_turbo_adj': turbo_adj})

        if self.engine_ini.has_section('COAST_REF'):
            c_rpm = int(self.engine_ini.get_value('COAST_REF', 'RPM',            '5000'))
            c_trq = float(self.engine_ini.get_value('COAST_REF', 'TORQUE',        '50'))
            c_nl  = float(self.engine_ini.get_value('COAST_REF', 'NON_LINEARITY', '0'))
            self.coast_ref_rpm.setValue(c_rpm)
            self.coast_ref_torque.setValue(c_trq)
            self.coast_non_linearity.setValue(c_nl)
            self.original_values.update({'coast_ref_rpm': c_rpm, 'coast_ref_torque': c_trq,
                                         'coast_non_linearity': c_nl})

        has_turbo = self.turbo_count > 0
        # Block signals to avoid partial state during setup
        self.has_turbo_check.blockSignals(True)
        self.has_turbo_check.setChecked(has_turbo)
        self.has_turbo_check.blockSignals(False)
        self.turbo_count_combo.setEnabled(has_turbo)
        if has_turbo:
            self.turbo_count_combo.setCurrentIndex(min(self.turbo_count - 1, 2))

        for i in range(min(self.turbo_count, 3)):
            sec = f'TURBO_{i}'
            if not self.engine_ini.has_section(sec):
                continue
            mb   = float(self.engine_ini.get_value(sec, 'MAX_BOOST',       '0.0'))
            wg   = float(self.engine_ini.get_value(sec, 'WASTEGATE',        '0.0'))
            dmb  = float(self.engine_ini.get_value(sec, 'DISPLAY_MAX_BOOST', str(mb)))
            lu   = float(self.engine_ini.get_value(sec, 'LAG_UP',           '0.990'))
            ld   = float(self.engine_ini.get_value(sec, 'LAG_DN',           '0.985'))
            rrpm = int(self.engine_ini.get_value(sec, 'REFERENCE_RPM',     '3000'))
            gam  = float(self.engine_ini.get_value(sec, 'GAMMA',            '2.5'))
            ca   = int(float(self.engine_ini.get_value(sec, 'COCKPIT_ADJUSTABLE', '0')))

            getattr(self, f'turbo_{i}_max_boost').setValue(mb)
            getattr(self, f'turbo_{i}_wastegate').setValue(wg)
            getattr(self, f'turbo_{i}_display_max').setValue(dmb)
            getattr(self, f'turbo_{i}_lag_up').setValue(lu)
            getattr(self, f'turbo_{i}_lag_dn').setValue(ld)
            getattr(self, f'turbo_{i}_ref_rpm').setValue(rrpm)
            getattr(self, f'turbo_{i}_gamma').setValue(gam)
            getattr(self, f'turbo_{i}_cockpit_adj').setChecked(bool(ca))
            self.original_values.update({
                f'turbo_{i}_max_boost': mb, f'turbo_{i}_wastegate': wg,
                f'turbo_{i}_display_max': dmb, f'turbo_{i}_lag_up': lu,
                f'turbo_{i}_lag_dn': ld, f'turbo_{i}_ref_rpm': rrpm,
                f'turbo_{i}_gamma': gam, f'turbo_{i}_cockpit_adj': bool(ca),
            })

        # Trigger visibility update after loading
        self._on_turbo_toggle(Qt.Checked if has_turbo else Qt.Unchecked)

        # Engine damage section
        if self.engine_ini.has_section('DAMAGE'):
            tbt = float(self.engine_ini.get_value('DAMAGE', 'TURBO_BOOST_THRESHOLD', '1.5'))
            tdk = float(self.engine_ini.get_value('DAMAGE', 'TURBO_DAMAGE_K', '5'))
            rth = int(float(self.engine_ini.get_value('DAMAGE', 'RPM_THRESHOLD', '8000')))
            rdk = float(self.engine_ini.get_value('DAMAGE', 'RPM_DAMAGE_K', '1'))
            self.turbo_boost_threshold.setValue(tbt)
            self.turbo_damage_k.setValue(tdk)
            self.rpm_threshold.setValue(rth)
            self.rpm_damage_k.setValue(rdk)
            self.original_values.update({'turbo_boost_threshold': tbt, 'turbo_damage_k': tdk,
                                         'rpm_threshold': rth, 'rpm_damage_k': rdk})

    def _load_suspension_data(self):
        if not self.suspension_ini:
            return

        if self.suspension_ini.has_section('ARB'):
            af = float(self.suspension_ini.get_value('ARB', 'FRONT', '20000'))
            ar = float(self.suspension_ini.get_value('ARB', 'REAR',  '10000'))
            self.arb_front.setValue(af)
            self.arb_rear.setValue(ar)
            self.original_values.update({'arb_front': af, 'arb_rear': ar})

        for axle, prefix in [('FRONT', 'front'), ('REAR', 'rear')]:
            if not self.suspension_ini.has_section(axle):
                continue
            spring   = float(self.suspension_ini.get_value(axle, 'SPRING_RATE',            '40000'))
            prog     = float(self.suspension_ini.get_value(axle, 'PROGRESSIVE_SPRING_RATE', '0'))
            db       = float(self.suspension_ini.get_value(axle, 'DAMP_BUMP',               '2500'))
            dfb      = float(self.suspension_ini.get_value(axle, 'DAMP_FAST_BUMP',          '3500'))
            dr       = float(self.suspension_ini.get_value(axle, 'DAMP_REBOUND',            '4000'))
            dfr      = float(self.suspension_ini.get_value(axle, 'DAMP_FAST_REBOUND',       '5500'))
            rod      = float(self.suspension_ini.get_value(axle, 'ROD_LENGTH',              '0.08'))
            camber   = float(self.suspension_ini.get_value(axle, 'STATIC_CAMBER',           '-1.5'))
            toe      = float(self.suspension_ini.get_value(axle, 'TOE_OUT',                 '0.0'))

            getattr(self, f'{prefix}_spring_rate').setValue(spring)
            getattr(self, f'{prefix}_progressive_spring').setValue(prog)
            getattr(self, f'{prefix}_damp_bump').setValue(db)
            getattr(self, f'{prefix}_damp_fast_bump').setValue(dfb)
            getattr(self, f'{prefix}_damp_rebound').setValue(dr)
            getattr(self, f'{prefix}_damp_fast_rebound').setValue(dfr)
            getattr(self, f'{prefix}_rod_length').setValue(rod)
            getattr(self, f'{prefix}_static_camber').setValue(camber)
            getattr(self, f'{prefix}_toe_out').setValue(toe)
            self.original_values.update({
                f'{prefix}_spring_rate': spring, f'{prefix}_progressive_spring': prog,
                f'{prefix}_damp_bump': db, f'{prefix}_damp_fast_bump': dfb,
                f'{prefix}_damp_rebound': dr, f'{prefix}_damp_fast_rebound': dfr,
                f'{prefix}_rod_length': rod, f'{prefix}_static_camber': camber,
                f'{prefix}_toe_out': toe,
            })

    def _load_drivetrain_data(self):
        if not self.drivetrain_ini:
            return

        if self.drivetrain_ini.has_section('TRACTION'):
            tt = self.drivetrain_ini.get_value('TRACTION', 'TYPE', 'RWD')
            idx = self.traction_type.findText(tt)
            if idx >= 0:
                self.traction_type.setCurrentIndex(idx)
            self.original_values['traction_type'] = tt

        if self.drivetrain_ini.has_section('DIFFERENTIAL'):
            dp  = float(self.drivetrain_ini.get_value('DIFFERENTIAL', 'POWER',   '0.1'))
            dc  = float(self.drivetrain_ini.get_value('DIFFERENTIAL', 'COAST',   '0.1'))
            dpl = float(self.drivetrain_ini.get_value('DIFFERENTIAL', 'PRELOAD', '2'))
            self.diff_power.setValue(dp)
            self.diff_coast.setValue(dc)
            self.diff_preload.setValue(dpl)
            self.original_values.update({'diff_power': dp, 'diff_coast': dc, 'diff_preload': dpl})

        if self.drivetrain_ini.has_section('GEARS'):
            gc    = int(self.drivetrain_ini.get_value('GEARS', 'COUNT', '6'))
            final = float(self.drivetrain_ini.get_value('GEARS', 'FINAL', '4.0'))
            self.gear_count.setValue(gc)
            self.final_ratio.setValue(final)
            self.original_values.update({'gear_count': gc, 'final_ratio': final})

        if self.drivetrain_ini.has_section('GEARBOX'):
            up   = int(self.drivetrain_ini.get_value('GEARBOX', 'CHANGE_UP_TIME', '250'))
            dn   = int(self.drivetrain_ini.get_value('GEARBOX', 'CHANGE_DN_TIME', '300'))
            gbi  = float(self.drivetrain_ini.get_value('GEARBOX', 'INERTIA',        '0.02'))
            self.gearbox_up_time.setValue(up)
            self.gearbox_dn_time.setValue(dn)
            self.gearbox_inertia.setValue(gbi)
            self.original_values.update({'gearbox_up_time': up, 'gearbox_dn_time': dn,
                                         'gearbox_inertia': gbi})

        if self.drivetrain_ini.has_section('CLUTCH'):
            ct = float(self.drivetrain_ini.get_value('CLUTCH', 'MAX_TORQUE', '400'))
            self.clutch_max_torque.setValue(ct)
            self.original_values['clutch_max_torque'] = ct

    def _load_weight_data(self):
        if self.car_ini:
            if self.car_ini.has_section('BASIC'):
                mass = float(self.car_ini.get_value('BASIC', 'TOTALMASS', '1350'))
                self.total_mass.setValue(mass)
                self.original_values['total_mass'] = mass
                inertia_str = self.car_ini.get_value('BASIC', 'INERTIA', '1.5,1.2,4.0')
                try:
                    parts = [float(x.strip()) for x in inertia_str.split(',')]
                    if len(parts) == 3:
                        self.inertia_x.setValue(parts[0])
                        self.inertia_y.setValue(parts[1])
                        self.inertia_z.setValue(parts[2])
                        self.original_values.update({'inertia_x': parts[0],
                                                     'inertia_y': parts[1],
                                                     'inertia_z': parts[2]})
                except (ValueError, AttributeError):
                    pass

            if self.car_ini.has_section('CONTROLS'):
                sl = float(self.car_ini.get_value('CONTROLS', 'STEER_LOCK',  '450'))
                sr = float(self.car_ini.get_value('CONTROLS', 'STEER_RATIO', '15.9'))
                self.steer_lock.setValue(sl)
                self.steer_ratio.setValue(sr)
                self.original_values.update({'steer_lock': sl, 'steer_ratio': sr})

            if self.car_ini.has_section('FUEL'):
                f   = float(self.car_ini.get_value('FUEL', 'FUEL',        '30'))
                mf  = float(self.car_ini.get_value('FUEL', 'MAX_FUEL',    '60'))
                con = float(self.car_ini.get_value('FUEL', 'CONSUMPTION', '0.003'))
                self.fuel_start.setValue(f)
                self.fuel_max.setValue(mf)
                self.fuel_consumption.setValue(con)
                self.original_values.update({'fuel_start': f, 'fuel_max': mf,
                                             'fuel_consumption': con})

        # CG_LOCATION and WHEELBASE live in suspensions.ini [BASIC]
        if self.suspension_ini and self.suspension_ini.has_section('BASIC'):
            cg = float(self.suspension_ini.get_value('BASIC', 'CG_LOCATION', '0.5'))
            wb = float(self.suspension_ini.get_value('BASIC', 'WHEELBASE',   '2.5'))
            self.cg_location.setValue(cg)
            self.wheelbase.setValue(wb)
            self.original_values.update({'cg_location': cg, 'wheelbase': wb})

    def _load_aero_data(self):
        if not self.aero_ini:
            return
        for i in range(self.wing_count):
            sec = f'WING_{i}'
            cd    = float(self.aero_ini.get_value(sec, 'CD',    '0.5'))
            cl    = float(self.aero_ini.get_value(sec, 'CL',    '0.0'))
            angle = float(self.aero_ini.get_value(sec, 'ANGLE', '0.0'))
            getattr(self, f'wing_{i}_cd').setValue(cd)
            getattr(self, f'wing_{i}_cl').setValue(cl)
            getattr(self, f'wing_{i}_angle').setValue(angle)
            self.original_values.update({f'wing_{i}_cd': cd, f'wing_{i}_cl': cl,
                                         f'wing_{i}_angle': angle})

    def _load_brakes_data(self):
        if not self.brakes_ini:
            return
        if self.brakes_ini.has_section('DATA'):
            mt  = float(self.brakes_ini.get_value('DATA', 'MAX_TORQUE',        '2000'))
            fs  = float(self.brakes_ini.get_value('DATA', 'FRONT_SHARE',       '0.60'))
            hb  = float(self.brakes_ini.get_value('DATA', 'HANDBRAKE_TORQUE',  '2500'))
            ca  = int(float(self.brakes_ini.get_value('DATA', 'COCKPIT_ADJUSTABLE', '0')))
            adj = float(self.brakes_ini.get_value('DATA', 'ADJUST_STEP',       '0.5'))
            self.brake_max_torque.setValue(mt)
            self.brake_front_share.setValue(fs)
            self.brake_handbrake.setValue(hb)
            self.brake_cockpit_adj.setChecked(bool(ca))
            self.brake_adjust_step.setValue(adj)
            self.original_values.update({'brake_max_torque': mt, 'brake_front_share': fs,
                                         'brake_handbrake': hb, 'brake_cockpit_adj': bool(ca),
                                         'brake_adjust_step': adj})

    # ------------------------------------------------------------------ Curve editors

    def edit_power_curve(self):
        path = os.path.join(self.car_data_path, 'power.lut')
        if not os.path.exists(path):
            if QMessageBox.question(self, "File Not Found",
                                    "power.lut not found. Create a new one?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return
        CurveEditorDialog(lut_file_path=path if os.path.exists(path) else None,
                          x_label="RPM", y_label="Power (HP)", parent=self).exec_()

    def edit_coast_curve(self):
        path = os.path.join(self.car_data_path, 'coast.lut')
        if not os.path.exists(path):
            if QMessageBox.question(self, "File Not Found",
                                    "coast.lut not found. Create a new one?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return
        CurveEditorDialog(lut_file_path=path if os.path.exists(path) else None,
                          x_label="RPM", y_label="Drag Torque (Nm)", parent=self).exec_()

    # ------------------------------------------------------------------ Component imports

    def import_engine_component(self):
        from PyQt5.QtWidgets import QDialog as _QD
        dialog = ComponentSelectorDialog('engine', self)
        if dialog.exec_() == _QD.Accepted:
            c = dialog.get_selected_component()
            if c:
                self.apply_engine_component(c)

    def apply_engine_component(self, component):
        data = component.get('data', {})
        applied = []
        if 'MINIMUM' in data:
            self.minimum_rpm.setValue(int(data['MINIMUM']));         applied.append('Idle RPM')
        if 'LIMITER' in data:
            self.limiter_rpm.setValue(int(data['LIMITER']));         applied.append('Rev Limiter')
        if 'INERTIA' in data:
            self.engine_inertia.setValue(float(data['INERTIA']));    applied.append('Engine Inertia')
        if 'TURBO_MAX_BOOST' in data:
            self.turbo_0_max_boost.setValue(float(data['TURBO_MAX_BOOST'])); applied.append('Turbo Max Boost')
        if 'TURBO_WASTEGATE' in data:
            self.turbo_0_wastegate.setValue(float(data['TURBO_WASTEGATE'])); applied.append('Turbo Wastegate')
        QMessageBox.information(self, "Component Applied",
                                f"Applied '{component.get('name', '?')}'\n\nUpdated:\n- " +
                                "\n- ".join(applied) + "\n\nRemember to save.")

    def import_suspension_component(self):
        from PyQt5.QtWidgets import QDialog as _QD
        dialog = ComponentSelectorDialog('suspension', self)
        if dialog.exec_() == _QD.Accepted:
            c = dialog.get_selected_component()
            if c:
                self.apply_suspension_component(c)

    def apply_suspension_component(self, component):
        data = component.get('data', {})
        applied = []
        mapping = {
            'FRONT_SPRING_RATE':        ('front_spring_rate',        float),
            'FRONT_DAMP_BUMP':          ('front_damp_bump',          float),
            'FRONT_DAMP_FAST_BUMP':     ('front_damp_fast_bump',     float),
            'FRONT_DAMP_REBOUND':       ('front_damp_rebound',       float),
            'FRONT_DAMP_FAST_REBOUND':  ('front_damp_fast_rebound',  float),
            'REAR_SPRING_RATE':         ('rear_spring_rate',         float),
            'REAR_DAMP_BUMP':           ('rear_damp_bump',           float),
            'REAR_DAMP_FAST_BUMP':      ('rear_damp_fast_bump',      float),
            'REAR_DAMP_REBOUND':        ('rear_damp_rebound',        float),
            'REAR_DAMP_FAST_REBOUND':   ('rear_damp_fast_rebound',   float),
        }
        for key, (attr, cast) in mapping.items():
            if key in data:
                getattr(self, attr).setValue(cast(data[key]))
                applied.append(key)
        QMessageBox.information(self, "Component Applied",
                                f"Applied '{component.get('name', '?')}'\n\nUpdated:\n- " +
                                "\n- ".join(applied) + "\n\nRemember to save.")

    def import_differential_component(self):
        from PyQt5.QtWidgets import QDialog as _QD
        dialog = ComponentSelectorDialog('differential', self)
        if dialog.exec_() == _QD.Accepted:
            c = dialog.get_selected_component()
            if c:
                self.apply_differential_component(c)

    def apply_differential_component(self, component):
        data = component.get('data', {})
        applied = []
        if 'POWER'   in data: self.diff_power.setValue(float(data['POWER']));        applied.append('Lock on Power')
        if 'COAST'   in data: self.diff_coast.setValue(float(data['COAST']));        applied.append('Lock on Coast')
        if 'PRELOAD' in data: self.diff_preload.setValue(float(data['PRELOAD']));    applied.append('Preload')
        QMessageBox.information(self, "Component Applied",
                                f"Applied '{component.get('name', '?')}'\n\nUpdated:\n- " +
                                "\n- ".join(applied) + "\n\nRemember to save.")

    def import_aero_component(self):
        from PyQt5.QtWidgets import QDialog as _QD
        dialog = ComponentSelectorDialog('aero', self)
        if dialog.exec_() == _QD.Accepted:
            c = dialog.get_selected_component()
            if c:
                self.apply_aero_component(c)

    def apply_aero_component(self, component):
        data = component.get('data', {})
        applied = []
        for i in range(self.wing_count):
            for key, attr in [(f'WING_{i}_CD', f'wing_{i}_cd'), (f'WING_{i}_CL', f'wing_{i}_cl')]:
                if key in data:
                    getattr(self, attr).setValue(float(data[key]))
                    applied.append(key)
        QMessageBox.information(self, "Component Applied",
                                f"Applied '{component.get('name', '?')}'\n\nUpdated:\n- " +
                                ("\n- ".join(applied) if applied else "None") + "\n\nRemember to save.")

    # ------------------------------------------------------------------ Save

    def save_changes(self):
        try:
            self._save_engine_data()
            self._save_suspension_data()   # saves suspension_ini (includes BASIC)
            self._save_drivetrain_data()
            self._save_weight_data()       # saves car_ini; suspension BASIC already saved above
            self._save_aero_data()
            self._save_brakes_data()
            QMessageBox.information(self, "Success",
                                    "Changes saved successfully!\n"
                                    "Backups created with .bak extension.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error Saving", f"Failed to save changes:\n{str(e)}")

    def _save_engine_data(self):
        if not self.engine_ini:
            return
        self.engine_ini.set_value('ENGINE_DATA', 'MINIMUM',              str(self.minimum_rpm.value()))
        self.engine_ini.set_value('ENGINE_DATA', 'LIMITER',              str(self.limiter_rpm.value()))
        self.engine_ini.set_value('ENGINE_DATA', 'LIMITER_HZ',          str(self.limiter_hz.value()))
        self.engine_ini.set_value('ENGINE_DATA', 'INERTIA',              f"{self.engine_inertia.value():.4f}")
        self.engine_ini.set_value('ENGINE_DATA', 'ALTITUDE_SENSITIVITY', f"{self.altitude_sensitivity.value():.3f}")
        self.engine_ini.set_value('ENGINE_DATA', 'DEFAULT_TURBO_ADJUSTMENT', f"{self.default_turbo_adj.value():.2f}")

        if self.engine_ini.has_section('COAST_REF'):
            self.engine_ini.set_value('COAST_REF', 'RPM',           str(self.coast_ref_rpm.value()))
            self.engine_ini.set_value('COAST_REF', 'TORQUE',        f"{self.coast_ref_torque.value():.1f}")
            self.engine_ini.set_value('COAST_REF', 'NON_LINEARITY', f"{self.coast_non_linearity.value():.3f}")

        num_turbos = (self.turbo_count_combo.currentIndex() + 1) if self.has_turbo_check.isChecked() else 0
        for i in range(num_turbos):
            sec = f'TURBO_{i}'
            self.engine_ini.set_value(sec, 'MAX_BOOST',       f"{getattr(self, f'turbo_{i}_max_boost').value():.3f}")
            self.engine_ini.set_value(sec, 'WASTEGATE',       f"{getattr(self, f'turbo_{i}_wastegate').value():.3f}")
            self.engine_ini.set_value(sec, 'DISPLAY_MAX_BOOST', f"{getattr(self, f'turbo_{i}_display_max').value():.3f}")
            self.engine_ini.set_value(sec, 'LAG_UP',          f"{getattr(self, f'turbo_{i}_lag_up').value():.4f}")
            self.engine_ini.set_value(sec, 'LAG_DN',          f"{getattr(self, f'turbo_{i}_lag_dn').value():.4f}")
            self.engine_ini.set_value(sec, 'REFERENCE_RPM',   str(getattr(self, f'turbo_{i}_ref_rpm').value()))
            self.engine_ini.set_value(sec, 'GAMMA',           f"{getattr(self, f'turbo_{i}_gamma').value():.2f}")
            self.engine_ini.set_value(sec, 'COCKPIT_ADJUSTABLE',
                                      '1' if getattr(self, f'turbo_{i}_cockpit_adj').isChecked() else '0')

        if self.engine_ini.has_section('DAMAGE'):
            self.engine_ini.set_value('DAMAGE', 'TURBO_BOOST_THRESHOLD', f"{self.turbo_boost_threshold.value():.2f}")
            self.engine_ini.set_value('DAMAGE', 'TURBO_DAMAGE_K',       f"{self.turbo_damage_k.value():.1f}")
            self.engine_ini.set_value('DAMAGE', 'RPM_THRESHOLD',        str(self.rpm_threshold.value()))
            self.engine_ini.set_value('DAMAGE', 'RPM_DAMAGE_K',         f"{self.rpm_damage_k.value():.1f}")

        self.engine_ini.save(backup=True)

    def _save_suspension_data(self):
        if not self.suspension_ini:
            return

        # Save BASIC section (shared with weight tab)
        if self.suspension_ini.has_section('BASIC'):
            self.suspension_ini.set_value('BASIC', 'CG_LOCATION', f"{self.cg_location.value():.4f}")
            self.suspension_ini.set_value('BASIC', 'WHEELBASE',   f"{self.wheelbase.value():.5f}")

        if self.suspension_ini.has_section('ARB'):
            self.suspension_ini.set_value('ARB', 'FRONT', str(int(self.arb_front.value())))
            self.suspension_ini.set_value('ARB', 'REAR',  str(int(self.arb_rear.value())))

        for axle, prefix in [('FRONT', 'front'), ('REAR', 'rear')]:
            if not self.suspension_ini.has_section(axle):
                continue
            self.suspension_ini.set_value(axle, 'SPRING_RATE',            str(int(getattr(self, f'{prefix}_spring_rate').value())))
            self.suspension_ini.set_value(axle, 'PROGRESSIVE_SPRING_RATE', str(int(getattr(self, f'{prefix}_progressive_spring').value())))
            self.suspension_ini.set_value(axle, 'DAMP_BUMP',              str(int(getattr(self, f'{prefix}_damp_bump').value())))
            self.suspension_ini.set_value(axle, 'DAMP_FAST_BUMP',         str(int(getattr(self, f'{prefix}_damp_fast_bump').value())))
            self.suspension_ini.set_value(axle, 'DAMP_REBOUND',           str(int(getattr(self, f'{prefix}_damp_rebound').value())))
            self.suspension_ini.set_value(axle, 'DAMP_FAST_REBOUND',      str(int(getattr(self, f'{prefix}_damp_fast_rebound').value())))
            self.suspension_ini.set_value(axle, 'ROD_LENGTH',             f"{getattr(self, f'{prefix}_rod_length').value():.4f}")
            self.suspension_ini.set_value(axle, 'STATIC_CAMBER',          f"{getattr(self, f'{prefix}_static_camber').value():.2f}")
            self.suspension_ini.set_value(axle, 'TOE_OUT',                f"{getattr(self, f'{prefix}_toe_out').value():.5f}")

        self.suspension_ini.save(backup=True)

    def _save_drivetrain_data(self):
        if not self.drivetrain_ini:
            return
        if self.drivetrain_ini.has_section('TRACTION'):
            self.drivetrain_ini.set_value('TRACTION', 'TYPE', self.traction_type.currentText())
        if self.drivetrain_ini.has_section('DIFFERENTIAL'):
            self.drivetrain_ini.set_value('DIFFERENTIAL', 'POWER',   f"{self.diff_power.value():.3f}")
            self.drivetrain_ini.set_value('DIFFERENTIAL', 'COAST',   f"{self.diff_coast.value():.3f}")
            self.drivetrain_ini.set_value('DIFFERENTIAL', 'PRELOAD', f"{self.diff_preload.value():.1f}")
        if self.drivetrain_ini.has_section('GEARS'):
            self.drivetrain_ini.set_value('GEARS', 'COUNT', str(self.gear_count.value()))
            self.drivetrain_ini.set_value('GEARS', 'FINAL', f"{self.final_ratio.value():.3f}")
        if self.drivetrain_ini.has_section('GEARBOX'):
            self.drivetrain_ini.set_value('GEARBOX', 'CHANGE_UP_TIME', str(self.gearbox_up_time.value()))
            self.drivetrain_ini.set_value('GEARBOX', 'CHANGE_DN_TIME', str(self.gearbox_dn_time.value()))
            self.drivetrain_ini.set_value('GEARBOX', 'INERTIA',        f"{self.gearbox_inertia.value():.4f}")
        if self.drivetrain_ini.has_section('CLUTCH'):
            self.drivetrain_ini.set_value('CLUTCH', 'MAX_TORQUE', str(int(self.clutch_max_torque.value())))
        self.drivetrain_ini.save(backup=True)

    def _save_weight_data(self):
        if not self.car_ini:
            return
        if self.car_ini.has_section('BASIC'):
            self.car_ini.set_value('BASIC', 'TOTALMASS', str(int(self.total_mass.value())))
            inertia_str = (f"{self.inertia_x.value():.2f},"
                           f"{self.inertia_y.value():.2f},"
                           f"{self.inertia_z.value():.2f}")
            self.car_ini.set_value('BASIC', 'INERTIA', inertia_str)
        if self.car_ini.has_section('CONTROLS'):
            self.car_ini.set_value('CONTROLS', 'STEER_LOCK',  str(int(self.steer_lock.value())))
            self.car_ini.set_value('CONTROLS', 'STEER_RATIO', f"{self.steer_ratio.value():.1f}")
        if self.car_ini.has_section('FUEL'):
            self.car_ini.set_value('FUEL', 'FUEL',        f"{self.fuel_start.value():.1f}")
            self.car_ini.set_value('FUEL', 'MAX_FUEL',    f"{self.fuel_max.value():.1f}")
            self.car_ini.set_value('FUEL', 'CONSUMPTION', f"{self.fuel_consumption.value():.6f}")
        self.car_ini.save(backup=True)
        # Note: suspension_ini BASIC (CG_LOCATION, WHEELBASE) is saved inside _save_suspension_data

    def _save_aero_data(self):
        if not self.aero_ini:
            return
        for i in range(self.wing_count):
            sec = f'WING_{i}'
            self.aero_ini.set_value(sec, 'CD',    f"{getattr(self, f'wing_{i}_cd').value():.4f}")
            self.aero_ini.set_value(sec, 'CL',    f"{getattr(self, f'wing_{i}_cl').value():.4f}")
            self.aero_ini.set_value(sec, 'ANGLE', f"{getattr(self, f'wing_{i}_angle').value():.2f}")
        self.aero_ini.save(backup=True)

    def _save_brakes_data(self):
        if not self.brakes_ini:
            return
        if self.brakes_ini.has_section('DATA'):
            self.brakes_ini.set_value('DATA', 'MAX_TORQUE',        str(int(self.brake_max_torque.value())))
            self.brakes_ini.set_value('DATA', 'FRONT_SHARE',       f"{self.brake_front_share.value():.3f}")
            self.brakes_ini.set_value('DATA', 'HANDBRAKE_TORQUE',  str(int(self.brake_handbrake.value())))
            self.brakes_ini.set_value('DATA', 'COCKPIT_ADJUSTABLE',
                                      '1' if self.brake_cockpit_adj.isChecked() else '0')
            self.brakes_ini.set_value('DATA', 'ADJUST_STEP', f"{self.brake_adjust_step.value():.1f}")
        self.brakes_ini.save(backup=True)

    # ------------------------------------------------------------------ Reset

    def reset_values(self):
        """Reload all fields from the original_values snapshot."""
        self._load_engine_data()
        self._load_suspension_data()
        self._load_drivetrain_data()
        self._load_weight_data()
        self._load_aero_data()
        self._load_brakes_data()
