"""
Tests for data.acd unpacking and deletion functionality
"""

import unittest
import os
import shutil
import tempfile
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.car_file_manager import CarFileManager


class TestDataAcdManagement(unittest.TestCase):
    """Test data.acd unpacking and deletion"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test cars
        self.test_dir = tempfile.mkdtemp()
        self.cars_path = os.path.join(self.test_dir, 'cars')
        os.makedirs(self.cars_path)
        
        # Create test car folder
        self.test_car = 'test_car'
        self.car_path = os.path.join(self.cars_path, self.test_car)
        os.makedirs(self.car_path)
        
        # Create car file manager
        self.manager = CarFileManager(self.cars_path)
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_has_data_acd(self):
        """Test checking if car has data.acd"""
        # Initially no data.acd
        self.assertFalse(self.manager.has_data_acd(self.test_car))
        
        # Create data.acd
        acd_path = os.path.join(self.car_path, 'data.acd')
        with open(acd_path, 'w') as f:
            f.write('test')
        
        # Now should have data.acd
        self.assertTrue(self.manager.has_data_acd(self.test_car))
    
    def test_delete_data_acd_success(self):
        """Test successful deletion of data.acd"""
        # Create data.acd
        acd_path = os.path.join(self.car_path, 'data.acd')
        with open(acd_path, 'w') as f:
            f.write('test')
        
        self.assertTrue(os.path.exists(acd_path))
        
        # Delete it
        result = self.manager.delete_data_acd(self.test_car)
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(acd_path))
    
    def test_delete_data_acd_not_exists(self):
        """Test deleting data.acd when it doesn't exist"""
        # Should return True even if file doesn't exist
        result = self.manager.delete_data_acd(self.test_car)
        self.assertTrue(result)
    
    def test_find_quickbms_path(self):
        """Test finding quickBMS executable"""
        path = self.manager._find_quickbms_path()
        
        # Should find the exe in tools folder
        if path:
            self.assertTrue(os.path.exists(path))
            self.assertTrue(path.endswith('.exe'))
    
    def test_find_quickbms_script(self):
        """Test finding quickBMS script"""
        script_path = self.manager._find_quickbms_script()
        
        # Should find the script in tools folder
        if script_path:
            self.assertTrue(os.path.exists(script_path))
            self.assertTrue(script_path.endswith('.bms'))
    
    def test_unpack_data_acd_no_file(self):
        """Test unpacking when data.acd doesn't exist"""
        result = self.manager.unpack_data_acd(self.test_car)
        self.assertFalse(result)
    
    def test_unpack_data_acd_data_exists(self):
        """Test unpacking when data folder already exists"""
        # Create data.acd
        acd_path = os.path.join(self.car_path, 'data.acd')
        with open(acd_path, 'w') as f:
            f.write('test')
        
        # Create data folder
        data_path = os.path.join(self.car_path, 'data')
        os.makedirs(data_path)
        
        # Should succeed and delete acd if requested
        result = self.manager.unpack_data_acd(self.test_car, delete_acd=True)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(acd_path))
    
    @patch('subprocess.run')
    @patch('sys.platform', 'win32')
    def test_unpack_data_acd_on_windows(self, mock_run):
        """Test unpacking on Windows with mocked subprocess"""
        # Create data.acd
        acd_path = os.path.join(self.car_path, 'data.acd')
        with open(acd_path, 'w') as f:
            f.write('test')
        
        # Mock successful subprocess run
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
        
        # Mock the path finding methods to return valid paths
        with patch.object(self.manager, '_find_quickbms_path', return_value='quickbms.exe'):
            with patch.object(self.manager, '_find_quickbms_script', return_value='script.bms'):
                result = self.manager.unpack_data_acd(self.test_car, delete_acd=False)
                
                # Should have called subprocess
                self.assertTrue(mock_run.called)
                
                # Check that data folder was created
                data_path = os.path.join(self.car_path, 'data')
                self.assertTrue(os.path.exists(data_path))


class TestDataAcdWithExamples(unittest.TestCase):
    """Test with real examples folder"""
    
    def setUp(self):
        """Set up test environment"""
        # Get examples folder path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.examples_path = os.path.join(project_root, 'examples')
        
        # Check if examples exist
        self.has_examples = os.path.exists(self.examples_path)
    
    def test_examples_structure(self):
        """Test that examples folder has expected structure"""
        if not self.has_examples:
            self.skipTest("Examples folder not found")
        
        # Should have data folder
        data_folder = os.path.join(self.examples_path, 'data')
        self.assertTrue(os.path.exists(data_folder))
        
        # Should have data.acd file
        data_acd = os.path.join(self.examples_path, 'data.acd')
        self.assertTrue(os.path.exists(data_acd))
        
        # Data folder should have engine.ini
        engine_ini = os.path.join(data_folder, 'engine.ini')
        self.assertTrue(os.path.exists(engine_ini))
    
    def test_examples_data_acd_size(self):
        """Test that data.acd has reasonable size"""
        if not self.has_examples:
            self.skipTest("Examples folder not found")
        
        data_acd = os.path.join(self.examples_path, 'data.acd')
        size = os.path.getsize(data_acd)
        
        # Should be at least 10KB (reasonable for AC car data)
        self.assertGreater(size, 10000)


if __name__ == '__main__':
    unittest.main()
