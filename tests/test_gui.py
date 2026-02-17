"""
Test suite for AC Car Editor GUI components
"""

import unittest
import os
import sys
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.ini_parser import IniParser


class TestCarEditorDialog(unittest.TestCase):
    """Test car editor dialog functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Get test data directory relative to this test file
        test_dir = os.path.dirname(__file__)
        self.test_data_dir = os.path.join(test_dir, 'test_data', 'test_car', 'data')
        self.test_engine_ini = os.path.join(self.test_data_dir, 'engine.ini')
        
        # Create temporary copy for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_engine_ini = os.path.join(self.temp_dir, 'engine.ini')
        shutil.copy2(self.test_engine_ini, self.temp_engine_ini)
        
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_load_engine_data(self):
        """Test loading engine data from INI file"""
        parser = IniParser(self.test_engine_ini)
        
        self.assertTrue(parser.has_section('ENGINE_DATA'))
        self.assertEqual(parser.get_value('ENGINE_DATA', 'MINIMUM'), '1000')
        self.assertEqual(parser.get_value('ENGINE_DATA', 'MAXIMUM'), '8500')
        self.assertEqual(parser.get_value('ENGINE_DATA', 'LIMITER'), '8500')
    
    def test_load_turbo_data(self):
        """Test loading turbo data from INI file"""
        parser = IniParser(self.test_engine_ini)
        
        self.assertTrue(parser.has_section('TURBO_0'))
        self.assertEqual(parser.get_value('TURBO_0', 'MAX_BOOST'), '1.5')
        self.assertEqual(parser.get_value('TURBO_0', 'WASTEGATE'), '1.2')
    
    def test_save_engine_data(self):
        """Test saving modified engine data"""
        parser = IniParser(self.temp_engine_ini)
        
        # Modify values
        parser.set_value('ENGINE_DATA', 'MINIMUM', '1200')
        parser.set_value('ENGINE_DATA', 'MAXIMUM', '9000')
        parser.set_value('ENGINE_DATA', 'LIMITER', '9500')
        
        # Save without backup for testing
        parser.save(backup=False)
        
        # Reload and verify
        parser2 = IniParser(self.temp_engine_ini)
        self.assertEqual(parser2.get_value('ENGINE_DATA', 'MINIMUM'), '1200')
        self.assertEqual(parser2.get_value('ENGINE_DATA', 'MAXIMUM'), '9000')
        self.assertEqual(parser2.get_value('ENGINE_DATA', 'LIMITER'), '9500')
    
    def test_save_turbo_data(self):
        """Test saving modified turbo data"""
        parser = IniParser(self.temp_engine_ini)
        
        # Modify values
        parser.set_value('TURBO_0', 'MAX_BOOST', '2.0')
        parser.set_value('TURBO_0', 'WASTEGATE', '1.8')
        
        # Save without backup for testing
        parser.save(backup=False)
        
        # Reload and verify
        parser2 = IniParser(self.temp_engine_ini)
        self.assertEqual(parser2.get_value('TURBO_0', 'MAX_BOOST'), '2.0')
        self.assertEqual(parser2.get_value('TURBO_0', 'WASTEGATE'), '1.8')
    
    def test_backup_creation(self):
        """Test that backup file is created when saving"""
        parser = IniParser(self.temp_engine_ini)
        
        # Modify a value
        parser.set_value('ENGINE_DATA', 'MINIMUM', '1100')
        
        # Save with backup
        parser.save(backup=True)
        
        # Check backup exists
        backup_path = self.temp_engine_ini + '.bak'
        self.assertTrue(os.path.exists(backup_path))
        
        # Verify backup contains original data
        backup_parser = IniParser(backup_path)
        self.assertEqual(backup_parser.get_value('ENGINE_DATA', 'MINIMUM'), '1000')


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
