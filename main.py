"""
AC Car Editor - Main Entry Point
Assetto Corsa Car Modifier Application
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("AC Car Editor")
    app.setOrganizationName("AC Car Editor")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
