#!/usr/bin/env python3
"""
Test script to manually verify Component Library Dialog
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication
from gui.component_library_dialog import ComponentLibraryDialog


def main():
    app = QApplication(sys.argv)
    
    # Create and show the component library dialog
    dialog = ComponentLibraryDialog()
    dialog.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
