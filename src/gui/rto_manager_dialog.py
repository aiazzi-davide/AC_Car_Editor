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
from core.ini_parser import IniParser


class RTOManagerDialog(QDialog):
    """Dialog for managing .rto (ratio) files"""
    
    def __init__(self, car_data_path, parent=None, engine_ini=None, tyres_ini=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.car_data_path = car_data_path
        self.final_rto_path = os.path.join(car_data_path, 'final.rto')
        self.ratios_rto_path = os.path.join(car_data_path, 'ratios.rto')
        self.setup_ini_path = os.path.join(car_data_path, 'setup.ini')
        
        self.final_parser = RTOParser(self.final_rto_path)
        self.ratios_parser = RTOParser(self.ratios_rto_path)
        
        # Store paths for speed calculation
        self.engine_ini_path = engine_ini if engine_ini else os.path.join(car_data_path, 'engine.ini')
        self.tyres_ini_path = tyres_ini if tyres_ini else os.path.join(car_data_path, 'tyres.ini')
        self.drivetrain_ini_path = os.path.join(car_data_path, 'drivetrain.ini')
        
        # Get tire radius and max RPM for speed calculation
        from core.speed_calculator import SpeedCalculator
        self.tire_radius = SpeedCalculator.get_tire_radius_from_ini(self.tyres_ini_path)
        self.max_rpm = SpeedCalculator.get_max_rpm_from_ini(self.engine_ini_path)
        
        # Get actual gear ratios from drivetrain.ini
        self.gear_ratios = self._read_gear_ratios_from_drivetrain()
        
        self.init_ui()
        self.load_data()
    
    def _read_gear_ratios_from_drivetrain(self):
        """Read gear ratios from drivetrain.ini [GEARS] section"""
        gear_ratios = {}
        
        if not os.path.exists(self.drivetrain_ini_path):
            return gear_ratios
        
        try:
            from core.ini_parser import IniParser
            parser = IniParser(self.drivetrain_ini_path)
            
            if parser.has_section('GEARS'):
                # Read gear count to know how many gears to read
                gear_count_str = parser.get_value('GEARS', 'COUNT', '6')
                gear_count = int(float(gear_count_str))
                
                # Read each gear ratio
                for i in range(1, gear_count + 1):
                    gear_key = f'GEAR_{i}'
                    ratio_str = parser.get_value('GEARS', gear_key, None)
                    if ratio_str:
                        gear_ratios[i] = float(ratio_str)
                
        except Exception as e:
            print(f"Error reading gear ratios from drivetrain.ini: {e}")
        
        return gear_ratios
    
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

        disclaimer_label = QLabel(
            "⚠️  When .rto files are present, Assetto Corsa uses them to override the gear ratios "
            "defined in drivetrain.ini. The values in drivetrain.ini are ignored for the affected "
            "ratios as long as the corresponding .rto file exists."
        )
        disclaimer_label.setWordWrap(True)
        disclaimer_label.setStyleSheet(
            "background-color: #FFF8E1; color: #5D4037; padding: 10px; border-radius: 5px;"
        )
        layout.addWidget(disclaimer_label)
        
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
        
        # Import from library button
        import_btn = QPushButton("📥 Import from Library...")
        import_btn.clicked.connect(self.import_final_from_library)
        import_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 6px;")
        layout.addWidget(import_btn)
        
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
        
        # Speed info label
        self.final_speed_info = QLabel()
        self.final_speed_info.setStyleSheet("color: #666; font-style: italic;")
        self.final_speed_info.setWordWrap(True)
        layout.addWidget(self.final_speed_info)
        
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
        
        # Import from library button
        import_btn = QPushButton("📥 Import from Library...")
        import_btn.clicked.connect(self.import_ratios_from_library)
        import_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 6px;")
        layout.addWidget(import_btn)
        
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
        
        # Speed info label
        self.ratios_speed_info = QLabel()
        self.ratios_speed_info.setStyleSheet("color: #666; font-style: italic;")
        self.ratios_speed_info.setWordWrap(True)
        layout.addWidget(self.ratios_speed_info)
        
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
        
        # Update speed info
        self._update_speed_info()
    
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
            final_had_ratios = len(self.final_parser.get_ratios()) > 0

            # Save final ratios
            if final_had_ratios:
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

            # After saving final.rto, check if setup.ini already references it
            if final_had_ratios and not self._setup_ini_references_final_rto():
                self._prompt_update_setup_ini()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving",
                f"Failed to save RTO files:\n{str(e)}"
            )

    def _setup_ini_references_final_rto(self) -> bool:
        """Return True if setup.ini already enables USE_GEARSET and points to final.rto."""
        if not os.path.exists(self.setup_ini_path):
            return False
        try:
            parser = IniParser(self.setup_ini_path)
            use_gearset = str(parser.get_value('GEARS', 'USE_GEARSET', '0')).strip()
            ratios = str(parser.get_value('FINAL_GEAR_RATIO', 'RATIOS', '')).strip().lower()
            return use_gearset == '1' and ratios == 'final.rto'
        except Exception:
            return False

    def _prompt_update_setup_ini(self):
        """Ask the user whether to update setup.ini to enable final.rto."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Update setup.ini?")
        msg.setIcon(QMessageBox.Question)
        msg.setText(
            "<b>final.rto has been saved, but Assetto Corsa won't use it yet.</b>"
        )
        msg.setInformativeText(
            "For the game to offer selectable final drive ratios, <b>setup.ini</b> must be "
            "configured as follows:<br><br>"
            "<tt>[GEARS]<br>USE_GEARSET=1</tt> — enables the gear setup menu in-game<br><br>"
            "<tt>[FINAL_GEAR_RATIO]<br>RATIOS=final.rto</tt> — points the game to the file "
            "you just saved<br><br>"
            "Would you like to update <b>setup.ini</b> automatically?"
        )
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        if msg.exec_() == QMessageBox.Yes:
            self._apply_setup_ini_update()

    def _apply_setup_ini_update(self):
        """Write USE_GEARSET=1 and [FINAL_GEAR_RATIO] RATIOS=final.rto to setup.ini."""
        try:
            parser = IniParser(self.setup_ini_path)
            parser.set_value('GEARS', 'USE_GEARSET', '1')
            parser.set_value('FINAL_GEAR_RATIO', 'RATIOS', 'final.rto')
            parser.save(backup=True)
            QMessageBox.information(
                self,
                "setup.ini Updated",
                "setup.ini has been updated:\n"
                "  [GEARS] USE_GEARSET=1\n"
                "  [FINAL_GEAR_RATIO] RATIOS=final.rto\n\n"
                "A backup was created as setup.ini.bak."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Updating setup.ini",
                f"Could not update setup.ini:\n{str(e)}"
            )
    
    def import_final_from_library(self):
        """Import final drive ratios from component library"""
        from gui.component_selector_dialog import ComponentSelectorDialog
        from PyQt5.QtWidgets import QDialog as _QD
        
        dialog = ComponentSelectorDialog('rto_final', self)
        if dialog.exec_() == _QD.Accepted:
            component = dialog.get_selected_component()
            if component and 'ratios' in component:
                # Clear current ratios and add from preset
                self.final_parser.set_ratios(component['ratios'])
                self.load_data()
                QMessageBox.information(
                    self,
                    "Preset Loaded",
                    f"Loaded '{component['name']}'\n"
                    f"{len(component['ratios'])} ratios imported.\n\n"
                    f"Remember to save changes."
                )
    
    def import_ratios_from_library(self):
        """Import gear ratios from component library"""
        from gui.component_selector_dialog import ComponentSelectorDialog
        from PyQt5.QtWidgets import QDialog as _QD
        
        dialog = ComponentSelectorDialog('rto_ratios', self)
        if dialog.exec_() == _QD.Accepted:
            component = dialog.get_selected_component()
            if component and 'ratios' in component:
                # Clear current ratios and add from preset
                self.ratios_parser.set_ratios(component['ratios'])
                self.load_data()
                QMessageBox.information(
                    self,
                    "Preset Loaded",
                    f"Loaded '{component['name']}'\n"
                    f"{len(component['ratios'])} ratios imported.\n\n"
                    f"Remember to save changes."
                )
    
    def _update_speed_info(self):
        """Update speed estimation info labels"""
        from core.speed_calculator import SpeedCalculator
        
        # Check if we have required data
        if not self.tire_radius or not self.max_rpm:
            missing = []
            if not self.tire_radius:
                missing.append("tire radius (tyres.ini)")
            if not self.max_rpm:
                missing.append("max RPM (engine.ini)")
            
            info_text = f"⚠️ Speed estimation unavailable - missing: {', '.join(missing)}"
            if hasattr(self, 'final_speed_info'):
                self.final_speed_info.setText(info_text)
            if hasattr(self, 'ratios_speed_info'):
                self.ratios_speed_info.setText(info_text)
            return
        
        # Update final ratios speed info using actual gear ratios from drivetrain.ini
        if hasattr(self, 'final_speed_info'):
            final_ratios = self.final_parser.get_ratios()
            if final_ratios and self.gear_ratios:
                speeds = []
                # Show speed for 1st gear and highest gear (or 6th if available)
                gear_nums = sorted(self.gear_ratios.keys())
                
                for final in final_ratios[:3]:  # Show first 3 final ratios
                    speed_parts = []
                    
                    # 1st gear speed
                    if 1 in self.gear_ratios:
                        speed_1st = SpeedCalculator.calculate_max_speed(
                            self.gear_ratios[1], final, self.max_rpm, self.tire_radius
                        )
                        speed_parts.append(f"1st: ~{speed_1st:.0f}")
                    
                    # Highest gear speed (6th if available, otherwise last gear)
                    if 6 in self.gear_ratios:
                        speed_6th = SpeedCalculator.calculate_max_speed(
                            self.gear_ratios[6], final, self.max_rpm, self.tire_radius
                        )
                        speed_parts.append(f"6th: ~{speed_6th:.0f}")
                    elif gear_nums:
                        last_gear = gear_nums[-1]
                        speed_last = SpeedCalculator.calculate_max_speed(
                            self.gear_ratios[last_gear], final, self.max_rpm, self.tire_radius
                        )
                        speed_parts.append(f"{last_gear}th: ~{speed_last:.0f}")
                    
                    if speed_parts:
                        speeds.append(f"{final:.2f} → {', '.join(speed_parts)} km/h")
                
                if speeds:
                    info_text = f"📊 Speed estimates (from drivetrain.ini): " + " | ".join(speeds)
                    if len(final_ratios) > 3:
                        info_text += f" (+{len(final_ratios)-3} more)"
                    self.final_speed_info.setText(info_text)
                else:
                    self.final_speed_info.setText("⚠️ No gear ratios found in drivetrain.ini")
            elif final_ratios:
                # Fallback to typical 1st gear if no actual gear ratios available
                typical_1st = 3.5
                speeds = []
                for final in final_ratios[:3]:
                    speed = SpeedCalculator.calculate_max_speed(
                        typical_1st, final, self.max_rpm, self.tire_radius
                    )
                    speeds.append(f"{final:.2f} → ~{speed:.0f} km/h (typical 1st)")
                
                info_text = f"📊 Speed estimates (no drivetrain.ini - using typical 1st gear {typical_1st}): " + " | ".join(speeds)
                if len(final_ratios) > 3:
                    info_text += f" (+{len(final_ratios)-3} more)"
                self.final_speed_info.setText(info_text)
        
        # Update gear ratios speed info  
        if hasattr(self, 'ratios_speed_info'):
            gear_ratios = self.ratios_parser.get_ratios()
            if gear_ratios:
                # Use a typical final ratio for estimation
                typical_final = 4.1
                speeds = []
                for i, gear in enumerate(gear_ratios[:3], 1):  # Show first 3
                    speed = SpeedCalculator.calculate_max_speed(
                        gear, typical_final, self.max_rpm, self.tire_radius
                    )
                    speeds.append(f"G{i}: ~{speed:.0f} km/h")
                
                info_text = f"📊 Speed estimates with final {typical_final}: " + " | ".join(speeds)
                if len(gear_ratios) > 3:
                    info_text += f" (+{len(gear_ratios)-3} more gears)"
                self.ratios_speed_info.setText(info_text)
