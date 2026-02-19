"""
Stage Tuning Dialog - One-click performance upgrades for AC cars
"""

import sys
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QMessageBox, QLabel, QTextEdit
)
from PyQt5.QtCore import Qt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.stage_tuner import StageTuner


class StageTuningDialog(QDialog):
    """Dialog for applying stage-based tuning to cars"""
    
    def __init__(self, car_name, car_data_path, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.car_name = car_name
        self.car_data_path = car_data_path
        self.tuner = StageTuner(car_data_path)
        
        self.init_ui()
        self.update_current_stage()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(f"Stage Tuning: {self.car_name}")
        self.setGeometry(200, 150, 600, 550)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Info section
        info_group = QGroupBox("Current Configuration")
        info_layout = QVBoxLayout()
        
        self.engine_type_label = QLabel()
        self.engine_type_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addWidget(self.engine_type_label)
        
        self.current_stage_label = QLabel()
        self.current_stage_label.setStyleSheet("font-size: 12px;")
        info_layout.addWidget(self.current_stage_label)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Stage 1
        stage1_group = QGroupBox()
        stage1_layout = QVBoxLayout()
        
        stage1_desc = self.tuner.get_stage_description(1)
        stage1_title = QLabel(stage1_desc['title'])
        stage1_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        stage1_layout.addWidget(stage1_title)
        
        stage1_text = QTextEdit()
        stage1_text.setPlainText(stage1_desc['description'])
        stage1_text.setReadOnly(True)
        stage1_text.setMaximumHeight(60)
        stage1_layout.addWidget(stage1_text)
        
        self.stage1_btn = QPushButton("Apply Stage 1")
        self.stage1_btn.clicked.connect(lambda: self.apply_stage(1))
        stage1_layout.addWidget(self.stage1_btn)
        
        stage1_group.setLayout(stage1_layout)
        layout.addWidget(stage1_group)
        
        # Stage 2
        stage2_group = QGroupBox()
        stage2_layout = QVBoxLayout()
        
        stage2_desc = self.tuner.get_stage_description(2)
        stage2_title = QLabel(stage2_desc['title'])
        stage2_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        stage2_layout.addWidget(stage2_title)
        
        stage2_text = QTextEdit()
        stage2_text.setPlainText(stage2_desc['description'])
        stage2_text.setReadOnly(True)
        stage2_text.setMaximumHeight(60)
        stage2_layout.addWidget(stage2_text)
        
        self.stage2_btn = QPushButton("Apply Stage 2")
        self.stage2_btn.clicked.connect(lambda: self.apply_stage(2))
        stage2_layout.addWidget(self.stage2_btn)
        
        stage2_group.setLayout(stage2_layout)
        layout.addWidget(stage2_group)
        
        # Stage 3
        stage3_group = QGroupBox()
        stage3_layout = QVBoxLayout()
        
        stage3_desc = self.tuner.get_stage_description(3)
        stage3_title = QLabel(stage3_desc['title'])
        stage3_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        stage3_layout.addWidget(stage3_title)
        
        stage3_text = QTextEdit()
        stage3_text.setPlainText(stage3_desc['description'])
        stage3_text.setReadOnly(True)
        stage3_text.setMaximumHeight(100)
        stage3_layout.addWidget(stage3_text)
        
        self.stage3_btn = QPushButton("Apply Stage 3")
        self.stage3_btn.clicked.connect(lambda: self.apply_stage(3))
        stage3_layout.addWidget(self.stage3_btn)
        
        stage3_group.setLayout(stage3_layout)
        layout.addWidget(stage3_group)
        
        # Reset button
        reset_layout = QHBoxLayout()
        self.reset_btn = QPushButton("Reset to Stock (Clear Stage Marker)")
        self.reset_btn.setToolTip("This only clears the stage marker, doesn't revert changes. Use backups to restore.")
        self.reset_btn.clicked.connect(self.reset_to_stock)
        reset_layout.addWidget(self.reset_btn)
        layout.addLayout(reset_layout)
        
        # Button bar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.close_btn)
        
        layout.addLayout(btn_layout)
    
    def update_current_stage(self):
        """Update the current stage display"""
        engine_type = "Turbocharged" if self.tuner.is_turbo else "Naturally Aspirated (NA)"
        self.engine_type_label.setText(f"Engine Type: {engine_type}")
        
        current_stage = self.tuner.get_current_stage()
        if current_stage == 0:
            self.current_stage_label.setText("Current Stage: Stock")
        else:
            self.current_stage_label.setText(f"Current Stage: Stage {current_stage}")
    
    def apply_stage(self, stage: int):
        """
        Apply stage tuning
        
        Args:
            stage: Stage number (1/2/3)
        """
        # Confirm with user
        stage_desc = self.tuner.get_stage_description(stage)
        reply = QMessageBox.question(
            self,
            f"Apply {stage_desc['title']}",
            f"This will apply the following modifications:\n\n{stage_desc['description']}\n\n"
            "Backups will be created automatically.\n\n"
            "Do you want to continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Apply stage
        success = False
        try:
            if stage == 1:
                success = self.tuner.apply_stage_1()
            elif stage == 2:
                success = self.tuner.apply_stage_2()
            elif stage == 3:
                success = self.tuner.apply_stage_3()
            
            if success:
                QMessageBox.information(
                    self,
                    "Success",
                    f"{stage_desc['title']} applied successfully!\n\n"
                    "Backups have been created for all modified files."
                )
                self.update_current_stage()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Failed to apply stage tuning. Check console for details."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error applying stage tuning: {e}"
            )
    
    def reset_to_stock(self):
        """Reset stage level to stock"""
        reply = QMessageBox.question(
            self,
            "Reset to Stock",
            "This will clear the stage marker from the car.\n\n"
            "Note: This does NOT revert the modifications made by stage tuning.\n"
            "To fully restore the car, use backups.\n\n"
            "Continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        if self.tuner.reset_to_stock():
            QMessageBox.information(
                self,
                "Success",
                "Stage marker cleared. Car marked as stock."
            )
            self.update_current_stage()
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Failed to reset stage marker."
            )
