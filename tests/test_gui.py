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
        self.test_suspension_ini = os.path.join(self.test_data_dir, 'suspensions.ini')
        self.test_drivetrain_ini = os.path.join(self.test_data_dir, 'drivetrain.ini')
        self.test_car_ini = os.path.join(self.test_data_dir, 'car.ini')
        self.test_aero_ini = os.path.join(self.test_data_dir, 'aero.ini')
        
        # Create temporary copy for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_engine_ini = os.path.join(self.temp_dir, 'engine.ini')
        self.temp_suspension_ini = os.path.join(self.temp_dir, 'suspensions.ini')
        self.temp_drivetrain_ini = os.path.join(self.temp_dir, 'drivetrain.ini')
        self.temp_car_ini = os.path.join(self.temp_dir, 'car.ini')
        self.temp_aero_ini = os.path.join(self.temp_dir, 'aero.ini')
        
        shutil.copy2(self.test_engine_ini, self.temp_engine_ini)
        if os.path.exists(self.test_suspension_ini):
            shutil.copy2(self.test_suspension_ini, self.temp_suspension_ini)
        if os.path.exists(self.test_drivetrain_ini):
            shutil.copy2(self.test_drivetrain_ini, self.temp_drivetrain_ini)
        if os.path.exists(self.test_car_ini):
            shutil.copy2(self.test_car_ini, self.temp_car_ini)
        if os.path.exists(self.test_aero_ini):
            shutil.copy2(self.test_aero_ini, self.temp_aero_ini)
        
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
    
    def test_load_suspension_data(self):
        """Test loading suspension data from INI file"""
        parser = IniParser(self.test_suspension_ini)
        
        self.assertTrue(parser.has_section('FRONT'))
        self.assertTrue(parser.has_section('REAR'))
        self.assertEqual(parser.get_value('FRONT', 'SPRING_RATE'), '80000')
        self.assertEqual(parser.get_value('REAR', 'SPRING_RATE'), '85000')
    
    def test_save_suspension_data(self):
        """Test saving modified suspension data"""
        parser = IniParser(self.temp_suspension_ini)
        
        # Modify values
        parser.set_value('FRONT', 'SPRING_RATE', '90000')
        parser.set_value('REAR', 'SPRING_RATE', '95000')
        
        # Save without backup for testing
        parser.save(backup=False)
        
        # Reload and verify
        parser2 = IniParser(self.temp_suspension_ini)
        self.assertEqual(parser2.get_value('FRONT', 'SPRING_RATE'), '90000')
        self.assertEqual(parser2.get_value('REAR', 'SPRING_RATE'), '95000')
    
    def test_load_differential_data(self):
        """Test loading differential data from INI file"""
        parser = IniParser(self.test_drivetrain_ini)
        
        self.assertTrue(parser.has_section('DIFFERENTIAL'))
        self.assertEqual(parser.get_value('DIFFERENTIAL', 'TYPE'), 'LSD')
        self.assertEqual(parser.get_value('DIFFERENTIAL', 'POWER'), '0.25')
        self.assertEqual(parser.get_value('DIFFERENTIAL', 'COAST'), '0.15')
    
    def test_save_differential_data(self):
        """Test saving modified differential data"""
        parser = IniParser(self.temp_drivetrain_ini)
        
        # Modify values
        parser.set_value('DIFFERENTIAL', 'POWER', '0.35')
        parser.set_value('DIFFERENTIAL', 'COAST', '0.25')
        
        # Save without backup for testing
        parser.save(backup=False)
        
        # Reload and verify
        parser2 = IniParser(self.temp_drivetrain_ini)
        self.assertEqual(parser2.get_value('DIFFERENTIAL', 'POWER'), '0.35')
        self.assertEqual(parser2.get_value('DIFFERENTIAL', 'COAST'), '0.25')
    
    def test_load_weight_data(self):
        """Test loading weight data from INI file"""
        parser = IniParser(self.test_car_ini)
        
        self.assertTrue(parser.has_section('BASIC'))
        self.assertEqual(parser.get_value('BASIC', 'TOTALMASS'), '1350')
        self.assertEqual(parser.get_value('GRAPHICS', 'CG_LOCATION'), '0.0,0.35,0.0')
    
    def test_save_weight_data(self):
        """Test saving modified weight data"""
        parser = IniParser(self.temp_car_ini)
        
        # Modify values
        parser.set_value('BASIC', 'TOTALMASS', '1400')
        parser.set_value('GRAPHICS', 'CG_LOCATION', '0.0,0.40,0.0')
        
        # Save without backup for testing
        parser.save(backup=False)
        
        # Reload and verify
        parser2 = IniParser(self.temp_car_ini)
        self.assertEqual(parser2.get_value('BASIC', 'TOTALMASS'), '1400')
        self.assertEqual(parser2.get_value('GRAPHICS', 'CG_LOCATION'), '0.0,0.40,0.0')
    
    def test_load_aero_data(self):
        """Test loading aerodynamics data from INI file"""
        parser = IniParser(self.test_aero_ini)
        
        self.assertTrue(parser.has_section('SETTINGS'))
        self.assertTrue(parser.has_section('FRONT'))
        self.assertTrue(parser.has_section('REAR'))
        self.assertEqual(parser.get_value('SETTINGS', 'DRAG_COEFF'), '0.34')
        self.assertEqual(parser.get_value('FRONT', 'LIFTCOEFF'), '-0.15')
        self.assertEqual(parser.get_value('REAR', 'LIFTCOEFF'), '-0.45')
    
    def test_save_aero_data(self):
        """Test saving modified aerodynamics data"""
        parser = IniParser(self.temp_aero_ini)
        
        # Modify values
        parser.set_value('SETTINGS', 'DRAG_COEFF', '0.30')
        parser.set_value('FRONT', 'LIFTCOEFF', '-0.20')
        
        # Save without backup for testing
        parser.save(backup=False)
        
        # Reload and verify
        parser2 = IniParser(self.temp_aero_ini)
        self.assertEqual(parser2.get_value('SETTINGS', 'DRAG_COEFF'), '0.30')
        self.assertEqual(parser2.get_value('FRONT', 'LIFTCOEFF'), '-0.20')


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
