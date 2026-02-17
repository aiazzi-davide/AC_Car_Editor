#!/usr/bin/env python3
"""
Test script for the curve editor
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication
from gui.curve_editor_dialog import CurveEditorDialog

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Test with power.lut
    power_lut = os.path.join(os.path.dirname(__file__), 'tests', 'test_data', 'test_car', 'data', 'power.lut')
    
    dialog = CurveEditorDialog(
        lut_file_path=power_lut,
        x_label="RPM",
        y_label="Power (kW)"
    )
    
    dialog.show()
    sys.exit(app.exec_())
