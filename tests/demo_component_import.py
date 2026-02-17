#!/usr/bin/env python3
"""
Test script to demonstrate component import functionality
Opens the component selector dialog for each component type
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication
from gui.component_selector_dialog import ComponentSelectorDialog


def main():
    app = QApplication(sys.argv)
    
    # Test engine component selector
    print("\n=== Testing Engine Component Selector ===")
    dialog = ComponentSelectorDialog('engine')
    dialog.setWindowTitle("Engine Component Selector - Demo")
    dialog.show()
    
    # Run the application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
