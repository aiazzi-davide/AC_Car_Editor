"""
Test Component Import functionality
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import QApplication
from src.gui.component_selector_dialog import ComponentSelectorDialog
from src.core.component_library import ComponentLibrary


class TestComponentImport(unittest.TestCase):
    """Test component import functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up QApplication for all tests"""
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])
    
    def test_component_selector_dialog_creation(self):
        """Test that ComponentSelectorDialog can be created"""
        dialog = ComponentSelectorDialog('engine')
        self.assertIsNotNone(dialog)
        self.assertEqual(dialog.component_type, 'engine')
        self.assertIsNotNone(dialog.component_list)
        
    def test_component_selector_loads_components(self):
        """Test that dialog loads components of correct type"""
        dialog = ComponentSelectorDialog('engine')
        
        # Should have engine components loaded
        self.assertGreater(dialog.component_list.count(), 0)
        
    def test_component_selector_for_each_type(self):
        """Test component selector for each component type"""
        types = ['engine', 'suspension', 'differential', 'aero']
        
        for comp_type in types:
            with self.subTest(component_type=comp_type):
                dialog = ComponentSelectorDialog(comp_type)
                self.assertEqual(dialog.component_type, comp_type)
                # Check that components are loaded
                self.assertGreater(dialog.component_list.count(), 0)
    
    def test_get_selected_component(self):
        """Test getting selected component"""
        dialog = ComponentSelectorDialog('engine')
        
        # Select first component
        dialog.component_list.setCurrentRow(0)
        
        # Get selected component
        component = dialog.get_selected_component()
        self.assertIsNotNone(component)
        self.assertIn('id', component)
        self.assertIn('name', component)
        self.assertIn('data', component)
    
    def test_component_data_structure(self):
        """Test that component data has correct structure"""
        library = ComponentLibrary()
        
        # Test engine component
        engines = library.get_components('engine')
        self.assertGreater(len(engines), 0)
        
        engine = engines[0]
        self.assertIn('id', engine)
        self.assertIn('name', engine)
        self.assertIn('data', engine)
        self.assertIn('tags', engine)
        
        # Engine data should have relevant keys
        data = engine['data']
        self.assertIsInstance(data, dict)
        # At least some basic engine parameters should be present
        has_rpm_data = any(key in data for key in ['MINIMUM', 'MAXIMUM', 'LIMITER'])
        self.assertTrue(has_rpm_data, "Engine component should have RPM data")


if __name__ == '__main__':
    unittest.main()
