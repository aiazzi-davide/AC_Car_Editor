"""
Test Component Library Dialog
"""

import sys
import os
import unittest
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import after path is set
from PyQt5.QtWidgets import QApplication
from src.gui.component_library_dialog import ComponentLibraryDialog, ComponentEditorDialog
from src.core.component_library import ComponentLibrary


class TestComponentLibraryDialog(unittest.TestCase):
    """Test component library dialog"""
    
    @classmethod
    def setUpClass(cls):
        """Set up QApplication for all tests"""
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary library for testing
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_lib_file = temp_file.name
        temp_file.close()
        self.library = ComponentLibrary(self.temp_lib_file)
        
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_lib_file):
            os.unlink(self.temp_lib_file)
    
    def test_dialog_creation(self):
        """Test that dialog can be created"""
        dialog = ComponentLibraryDialog()
        self.assertIsNotNone(dialog)
        self.assertIsNotNone(dialog.library)
        self.assertIsNotNone(dialog.component_list)
        self.assertIsNotNone(dialog.type_combo)
        
    def test_load_components(self):
        """Test loading components into list"""
        dialog = ComponentLibraryDialog()
        
        # Initially should have engine components loaded
        self.assertEqual(dialog.current_component_type, 'engine')
        self.assertGreater(dialog.component_list.count(), 0)
        
    def test_type_change(self):
        """Test changing component type"""
        dialog = ComponentLibraryDialog()
        
        # Change to suspension
        dialog.type_combo.setCurrentText('Suspension')
        self.assertEqual(dialog.current_component_type, 'suspension')
        self.assertGreater(dialog.component_list.count(), 0)
        
    def test_search_filter(self):
        """Test search functionality"""
        dialog = ComponentLibraryDialog()
        
        # Count initial items
        initial_count = dialog.component_list.count()
        
        # Search for 'turbo'
        dialog.search_box.setText('turbo')
        filtered_count = dialog.component_list.count()
        
        # Should have fewer items or same
        self.assertLessEqual(filtered_count, initial_count)
        
    def test_component_editor_dialog(self):
        """Test component editor dialog creation"""
        # Test creating new component
        dialog = ComponentEditorDialog('engine', None)
        self.assertIsNotNone(dialog)
        self.assertTrue(dialog.id_edit.isEnabled())
        
        # Test editing existing component
        component = {
            'id': 'test_engine',
            'name': 'Test Engine',
            'description': 'Test description',
            'tags': ['test', 'demo'],
            'data': {'MINIMUM': 1000, 'LIMITER': 8000}
        }
        dialog = ComponentEditorDialog('engine', component)
        self.assertIsNotNone(dialog)
        self.assertFalse(dialog.id_edit.isEnabled())  # ID should be disabled when editing
        self.assertEqual(dialog.name_edit.text(), 'Test Engine')


if __name__ == '__main__':
    unittest.main()
