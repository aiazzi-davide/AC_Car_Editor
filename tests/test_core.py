"""
Test suite for AC Car Editor core modules
"""

import unittest
import os
import sys
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.ini_parser import IniParser
from core.lut_parser import LUTCurve
from core.car_file_manager import CarFileManager
from core.component_library import ComponentLibrary


class TestIniParser(unittest.TestCase):
    """Test INI parser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = 'tests/test_data/test_car/data/engine.ini'
        
    def test_load_ini(self):
        """Test loading INI file"""
        parser = IniParser(self.test_file)
        self.assertTrue(parser.has_section('ENGINE_DATA'))
        
    def test_get_value(self):
        """Test getting values from INI"""
        parser = IniParser(self.test_file)
        minimum = parser.get_value('ENGINE_DATA', 'MINIMUM')
        self.assertEqual(minimum, '1000')
        
    def test_get_section(self):
        """Test getting entire section"""
        parser = IniParser(self.test_file)
        section = parser.get_section('ENGINE_DATA')
        self.assertIn('MINIMUM', section)
        self.assertIn('MAXIMUM', section)
    
    def test_inline_comments(self):
        """Test parsing values with inline comments"""
        import tempfile
        # Create a temporary INI file with inline comments
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write('[ENGINE_DATA]\n')
            f.write('MINIMUM=1000\t\t; minimum RPM\n')
            f.write('MAXIMUM=8200\t\t\t\t\t; maximum RPM\n')
            f.write('LIMITER=8500\t\t; engine rev limiter\n')
            temp_file = f.name
        
        try:
            parser = IniParser(temp_file)
            self.assertEqual(parser.get_value('ENGINE_DATA', 'MINIMUM'), '1000')
            self.assertEqual(parser.get_value('ENGINE_DATA', 'MAXIMUM'), '8200')
            self.assertEqual(parser.get_value('ENGINE_DATA', 'LIMITER'), '8500')
        finally:
            os.unlink(temp_file)


class TestLUTParser(unittest.TestCase):
    """Test LUT parser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = 'tests/test_data/test_car/data/power.lut'
        
    def test_load_lut(self):
        """Test loading LUT file"""
        curve = LUTCurve(self.test_file)
        self.assertGreater(len(curve), 0)
        
    def test_get_points(self):
        """Test getting points"""
        curve = LUTCurve(self.test_file)
        points = curve.get_points()
        self.assertEqual(len(points), 9)
        self.assertEqual(points[0], (1000.0, 100.0))
        
    def test_interpolate(self):
        """Test interpolation"""
        curve = LUTCurve(self.test_file)
        # Test exact point
        value = curve.interpolate(3000.0)
        self.assertEqual(value, 200.0)
        
        # Test interpolated point
        value = curve.interpolate(3500.0)
        self.assertGreater(value, 200.0)
        self.assertLess(value, 280.0)
        
    def test_add_point(self):
        """Test adding point"""
        curve = LUTCurve(self.test_file)
        initial_count = len(curve)
        curve.add_point(9000.0, 400.0)
        self.assertEqual(len(curve), initial_count + 1)
        
    def test_save_load(self):
        """Test save and load roundtrip"""
        curve = LUTCurve(self.test_file)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lut') as f:
            temp_file = f.name
        
        try:
            curve.save(temp_file, backup=False)
            
            # Load and compare
            curve2 = LUTCurve(temp_file)
            self.assertEqual(len(curve), len(curve2))
            self.assertEqual(curve.get_points(), curve2.get_points())
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


class TestCarFileManager(unittest.TestCase):
    """Test car file manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_cars_path = 'tests/test_data'
        self.manager = CarFileManager(self.test_cars_path)
        
    def test_get_car_list(self):
        """Test getting car list"""
        cars = self.manager.get_car_list()
        self.assertIn('test_car', cars)
        
    def test_get_car_info(self):
        """Test getting car info"""
        info = self.manager.get_car_info('test_car')
        self.assertEqual(info['name'], 'test_car')
        self.assertTrue(info['has_data_folder'])
        self.assertEqual(info['display_name'], 'Test Car')
        self.assertEqual(info['brand'], 'Test Brand')
        
    def test_has_data_folder(self):
        """Test checking for data folder"""
        self.assertTrue(self.manager.has_data_folder('test_car'))
    
    def test_is_acd_encrypted(self):
        """Test checking if ACD is encrypted"""
        # Test with existing unencrypted ACD (ZIP)
        acd_exists, is_encrypted = self.manager.is_acd_encrypted('test_car')
        self.assertTrue(acd_exists)
        self.assertFalse(is_encrypted)  # Should be unencrypted ZIP
    
    def test_unpack_data_acd(self):
        """Test unpacking data.acd file"""
        # Create a temp test environment
        temp_dir = tempfile.mkdtemp()
        try:
            # Create test car folder structure
            test_car_path = os.path.join(temp_dir, 'test_unpack_car')
            os.makedirs(test_car_path)
            
            # Copy the test data.acd
            src_acd = 'tests/test_data/test_car/data.acd'
            dst_acd = os.path.join(test_car_path, 'data.acd')
            shutil.copy(src_acd, dst_acd)
            
            # Create manager for temp directory
            temp_manager = CarFileManager(temp_dir)
            
            # Unpack the ACD
            result = temp_manager.unpack_data_acd('test_unpack_car', backup_existing=False)
            self.assertTrue(result)
            
            # Verify data folder was created
            self.assertTrue(temp_manager.has_data_folder('test_unpack_car'))
            
            # Verify files were extracted
            data_path = temp_manager.get_car_data_path('test_unpack_car')
            self.assertTrue(os.path.exists(os.path.join(data_path, 'test_unpack.txt')))
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_unpack_data_acd_with_delete(self):
        """Test unpacking data.acd file with deletion after unpacking"""
        # Create a temp test environment
        temp_dir = tempfile.mkdtemp()
        try:
            # Create test car folder structure
            test_car_path = os.path.join(temp_dir, 'test_unpack_car_delete')
            os.makedirs(test_car_path)
            
            # Copy the test data.acd
            src_acd = 'tests/test_data/test_car/data.acd'
            dst_acd = os.path.join(test_car_path, 'data.acd')
            shutil.copy(src_acd, dst_acd)
            
            # Create manager for temp directory
            temp_manager = CarFileManager(temp_dir)
            
            # Verify data.acd exists before unpacking
            self.assertTrue(os.path.exists(dst_acd))
            
            # Unpack the ACD with delete_acd=True
            result = temp_manager.unpack_data_acd('test_unpack_car_delete', 
                                                   backup_existing=False, 
                                                   delete_acd=True)
            self.assertTrue(result)
            
            # Verify data folder was created
            self.assertTrue(temp_manager.has_data_folder('test_unpack_car_delete'))
            
            # Verify files were extracted
            data_path = temp_manager.get_car_data_path('test_unpack_car_delete')
            self.assertTrue(os.path.exists(os.path.join(data_path, 'test_unpack.txt')))
            
            # Verify data.acd was deleted
            self.assertFalse(os.path.exists(dst_acd))
            
        finally:
            shutil.rmtree(temp_dir)


class TestComponentLibrary(unittest.TestCase):
    """Test component library"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Use temp file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.library_path = os.path.join(self.temp_dir, 'test_library.json')
        self.library = ComponentLibrary(self.library_path)
        
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir)
        
    def test_create_default_library(self):
        """Test default library creation"""
        self.assertIn('engine', self.library.components)
        self.assertGreater(len(self.library.components['engine']), 0)
        
    def test_add_component(self):
        """Test adding component"""
        component = {
            'id': 'test_engine',
            'name': 'Test Engine',
            'description': 'Test',
            'tags': ['test'],
            'data': {}
        }
        result = self.library.add_component('engine', component)
        self.assertTrue(result)
        
        # Verify it was added
        found = self.library.get_component('engine', 'test_engine')
        self.assertIsNotNone(found)
        self.assertEqual(found['name'], 'Test Engine')
        
    def test_get_components(self):
        """Test getting components by type"""
        components = self.library.get_components('engine')
        self.assertIsInstance(components, list)
        self.assertGreater(len(components), 0)
        
    def test_search_components(self):
        """Test searching components"""
        results = self.library.search_components('engine', 'default')
        self.assertGreater(len(results), 0)


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
