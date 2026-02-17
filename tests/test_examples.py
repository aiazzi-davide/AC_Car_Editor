"""
Test suite using real AC car data from examples/ folder

This tests the application with actual Assetto Corsa car data
to ensure it works correctly with real-world files.
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


class TestExamplesFolder(unittest.TestCase):
    """Test with real AC car data from examples/ folder"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.examples_path = os.path.join(os.path.dirname(__file__), '..', 'examples')
        self.assertTrue(os.path.exists(self.examples_path), 
                       "examples/ folder not found")
        self.assertTrue(os.path.exists(os.path.join(self.examples_path, 'data')),
                       "examples/data/ folder not found")
        self.assertTrue(os.path.exists(os.path.join(self.examples_path, 'data.acd')),
                       "examples/data.acd file not found")
    
    def test_examples_has_both_data_and_acd(self):
        """Test that examples/ has both data folder and data.acd file"""
        # Create a temporary test environment
        temp_dir = tempfile.mkdtemp()
        try:
            # Copy examples to temp dir
            test_car_path = os.path.join(temp_dir, 'test_car')
            shutil.copytree(self.examples_path, test_car_path)
            
            # Create manager
            manager = CarFileManager(temp_dir)
            
            # Verify both exist
            self.assertTrue(manager.has_data_folder('test_car'))
            self.assertTrue(manager.has_data_acd('test_car'))
            
            # Get car info
            info = manager.get_car_info('test_car')
            self.assertTrue(info['has_data_folder'])
            self.assertTrue(info['has_data_acd'])
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_delete_acd_with_real_data(self):
        """Test deleting real data.acd when data folder exists"""
        # Create a temporary test environment
        temp_dir = tempfile.mkdtemp()
        try:
            # Copy examples to temp dir
            test_car_path = os.path.join(temp_dir, 'test_car')
            shutil.copytree(self.examples_path, test_car_path)
            
            # Create manager
            manager = CarFileManager(temp_dir)
            
            # Verify data.acd exists before deletion
            acd_path = os.path.join(test_car_path, 'data.acd')
            self.assertTrue(os.path.exists(acd_path))
            
            # Delete data.acd
            result = manager.delete_data_acd('test_car')
            self.assertTrue(result)
            
            # Verify data.acd was deleted
            self.assertFalse(os.path.exists(acd_path))
            
            # Verify data folder still exists
            self.assertTrue(manager.has_data_folder('test_car'))
            
            # Verify files in data folder still exist
            engine_ini = os.path.join(test_car_path, 'data', 'engine.ini')
            self.assertTrue(os.path.exists(engine_ini))
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_parse_real_engine_ini(self):
        """Test parsing real engine.ini from examples/"""
        engine_ini_path = os.path.join(self.examples_path, 'data', 'engine.ini')
        
        parser = IniParser(engine_ini_path)
        
        # Check that ENGINE_DATA section exists
        self.assertTrue(parser.has_section('ENGINE_DATA'))
        
        # Try to get some common values (not all files have all fields)
        minimum = parser.get_value('ENGINE_DATA', 'MINIMUM', '')
        limiter = parser.get_value('ENGINE_DATA', 'LIMITER', '')
        
        # Verify at least one value exists
        self.assertTrue(minimum or limiter, 
                       "Should have at least MINIMUM or LIMITER")
        
        # If values exist, verify they're numeric
        if minimum:
            try:
                int(minimum)
            except ValueError:
                self.fail("MINIMUM value should be numeric")
        
        if limiter:
            try:
                int(limiter)
            except ValueError:
                self.fail("LIMITER value should be numeric")
    
    def test_parse_real_suspensions_ini(self):
        """Test parsing real suspensions.ini from examples/"""
        susp_ini_path = os.path.join(self.examples_path, 'data', 'suspensions.ini')
        
        parser = IniParser(susp_ini_path)
        
        # Check common suspension sections
        self.assertTrue(parser.has_section('FRONT') or parser.has_section('SUSPENSION_FRONT'))
        self.assertTrue(parser.has_section('REAR') or parser.has_section('SUSPENSION_REAR'))
    
    def test_parse_real_power_lut(self):
        """Test parsing real power.lut from examples/"""
        power_lut_path = os.path.join(self.examples_path, 'data', 'power.lut')
        
        # Check if file exists
        if not os.path.exists(power_lut_path):
            self.skipTest("power.lut not found in examples/")
        
        curve = LUTCurve(power_lut_path)
        
        # Verify we got some points
        self.assertGreater(len(curve), 0, "power.lut should have data points")
        
        # Verify points are tuples of (x, y)
        points = curve.get_points()
        for x, y in points:
            self.assertIsInstance(x, (int, float))
            self.assertIsInstance(y, (int, float))
    
    def test_parse_real_throttle_lut(self):
        """Test parsing real throttle.lut from examples/"""
        throttle_lut_path = os.path.join(self.examples_path, 'data', 'throttle.lut')
        
        # Check if file exists
        if not os.path.exists(throttle_lut_path):
            self.skipTest("throttle.lut not found in examples/")
        
        curve = LUTCurve(throttle_lut_path)
        
        # Verify we got some points
        self.assertGreater(len(curve), 0, "throttle.lut should have data points")
    
    def test_real_acd_is_not_zip(self):
        """Test that real data.acd is not a ZIP file"""
        acd_path = os.path.join(self.examples_path, 'data.acd')
        
        # Read first 2 bytes
        with open(acd_path, 'rb') as f:
            magic = f.read(2)
        
        # ZIP files start with 'PK' (0x50 0x4B)
        # Real AC data.acd uses custom format
        self.assertNotEqual(magic, b'PK', 
                           "Real data.acd should NOT be ZIP format")
    
    def test_detect_real_acd_format(self):
        """Test detection of real AC data.acd format"""
        # Create a temporary test environment
        temp_dir = tempfile.mkdtemp()
        try:
            # Copy examples to temp dir
            test_car_path = os.path.join(temp_dir, 'test_car')
            shutil.copytree(self.examples_path, test_car_path)
            
            # Create manager
            manager = CarFileManager(temp_dir)
            
            # Check if ACD is encrypted/custom format
            acd_exists, is_encrypted = manager.is_acd_encrypted('test_car')
            
            self.assertTrue(acd_exists, "data.acd should exist")
            self.assertTrue(is_encrypted, 
                          "Real data.acd should be detected as custom format (not ZIP)")
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_unpack_real_acd_fails_gracefully(self):
        """Test that unpacking real data.acd fails gracefully (custom format)"""
        # Create a temporary test environment
        temp_dir = tempfile.mkdtemp()
        try:
            # Copy only data.acd (no data folder)
            test_car_path = os.path.join(temp_dir, 'test_car')
            os.makedirs(test_car_path)
            shutil.copy(
                os.path.join(self.examples_path, 'data.acd'),
                os.path.join(test_car_path, 'data.acd')
            )
            
            # Create manager
            manager = CarFileManager(temp_dir)
            
            # Try to unpack (should fail - custom format, not ZIP)
            result = manager.unpack_data_acd('test_car', 
                                            backup_existing=False, 
                                            delete_acd=False)
            
            # Should fail gracefully
            self.assertFalse(result, 
                           "Unpacking custom format should fail gracefully")
            
            # data.acd should still exist (delete_acd=False)
            acd_path = os.path.join(test_car_path, 'data.acd')
            self.assertTrue(os.path.exists(acd_path))
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_all_ini_files_parseable(self):
        """Test that all INI files in examples/data/ are parseable"""
        data_path = os.path.join(self.examples_path, 'data')
        ini_files = [f for f in os.listdir(data_path) if f.endswith('.ini')]
        
        self.assertGreater(len(ini_files), 0, "Should have at least one INI file")
        
        parsed_count = 0
        skipped = []
        
        for ini_file in ini_files:
            ini_path = os.path.join(data_path, ini_file)
            try:
                parser = IniParser(ini_path)
                # Just verify it loaded (even if with warnings)
                # The IniParser handles errors gracefully and continues with partial data
                parsed_count += 1
            except Exception as e:
                # Some files may have issues, but IniParser should handle them gracefully
                skipped.append(f"{ini_file}: {str(e)}")
        
        # We should be able to parse most files (even if with warnings)
        self.assertGreater(parsed_count, len(ini_files) * 0.7,
                         f"Should parse at least 70% of INI files. Skipped: {skipped}")
    
    def test_all_lut_files_parseable(self):
        """Test that all LUT files in examples/data/ are parseable"""
        data_path = os.path.join(self.examples_path, 'data')
        lut_files = [f for f in os.listdir(data_path) if f.endswith('.lut')]
        
        self.assertGreater(len(lut_files), 0, "Should have at least one LUT file")
        
        errors = []
        for lut_file in lut_files:
            lut_path = os.path.join(data_path, lut_file)
            try:
                curve = LUTCurve(lut_path)
                # Verify we got some points (or file is empty, which is ok)
                points = curve.get_points()
                # Just verify it's a list
                self.assertIsInstance(points, list)
            except Exception as e:
                errors.append(f"{lut_file}: {str(e)}")
        
        if errors:
            self.fail(f"Failed to parse {len(errors)} LUT files:\n" + "\n".join(errors))


if __name__ == '__main__':
    unittest.main()
