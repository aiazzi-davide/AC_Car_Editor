#!/usr/bin/env python3
"""
Simple test to verify Phase 7 UI changes
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """Test the main window with Phase 7 features"""
    print("Testing Phase 7 Features:")
    print("1. Search/Filter functionality")
    print("2. Preview image display")
    print("\nLaunching main window...")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # Check if search box exists
    if hasattr(window, 'search_box'):
        print("✓ Search box widget created")
    else:
        print("✗ Search box widget NOT found")
    
    # Check if preview label exists
    if hasattr(window, 'preview_label'):
        print("✓ Preview label widget created")
    else:
        print("✗ Preview label widget NOT found")
    
    # Check if filter methods exist
    if hasattr(window, 'filter_cars'):
        print("✓ filter_cars method exists")
    else:
        print("✗ filter_cars method NOT found")
    
    if hasattr(window, 'clear_filter'):
        print("✓ clear_filter method exists")
    else:
        print("✗ clear_filter method NOT found")
    
    print("\nWindow is ready. Close the window to exit.")
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
