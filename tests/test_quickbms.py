"""
Unit tests for QuickBMS integration in CarFileManager
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.car_file_manager import CarFileManager
from core.config import ConfigManager


class TestQuickBMSIntegration(unittest.TestCase):
    """Test QuickBMS integration methods"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = CarFileManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_find_quickbms_with_config(self):
        """Test QuickBMS discovery from config"""
        # Create a mock config manager
        config_manager = Mock()
        config_manager.get_quickbms_path.return_value = '/path/to/quickbms.exe'
        
        # Create manager with config
        manager = CarFileManager(self.temp_dir, config_manager)
        
        # Mock os.path.exists to return True for our path
        with patch('os.path.exists', return_value=True):
            result = manager.find_quickbms()
            self.assertEqual(result, '/path/to/quickbms.exe')
    
    def test_find_quickbms_without_config(self):
        """Test QuickBMS discovery without config manager"""
        # Manager without config
        manager = CarFileManager(self.temp_dir, None)
        
        # Create a fake quickbms in tools directory
        tools_dir = os.path.join(self.temp_dir, 'tools')
        os.makedirs(tools_dir, exist_ok=True)
        quickbms_path = os.path.join(tools_dir, 'quickbms.exe' if os.name == 'nt' else 'quickbms')
        
        # Create empty file
        with open(quickbms_path, 'w') as f:
            f.write('')
        
        # Should find it in tools directory
        with patch('os.getcwd', return_value=self.temp_dir):
            result = manager.find_quickbms()
            self.assertIsNotNone(result)
            self.assertTrue(result.endswith('quickbms.exe' if os.name == 'nt' else 'quickbms'))
    
    def test_find_quickbms_not_found(self):
        """Test QuickBMS not found scenario"""
        manager = CarFileManager(self.temp_dir, None)
        
        # Empty directory, should not find anything
        with patch('os.getcwd', return_value=self.temp_dir):
            with patch('os.environ', {'PATH': ''}):
                result = manager.find_quickbms()
                self.assertIsNone(result)
    
    def test_find_acd_bms_script_found(self):
        """Test BMS script discovery"""
        manager = CarFileManager(self.temp_dir, None)
        
        # Create acd.bms in current directory
        bms_path = os.path.join(self.temp_dir, 'acd.bms')
        with open(bms_path, 'w') as f:
            f.write('# BMS script')
        
        with patch('os.getcwd', return_value=self.temp_dir):
            result = manager.find_acd_bms_script()
            self.assertEqual(result, bms_path)
    
    def test_find_acd_bms_script_not_found(self):
        """Test BMS script not found"""
        manager = CarFileManager(self.temp_dir, None)
        
        with patch('os.getcwd', return_value=self.temp_dir):
            result = manager.find_acd_bms_script()
            self.assertIsNone(result)
    
    @patch('subprocess.run')
    def test_unpack_with_quickbms_success(self, mock_run):
        """Test successful QuickBMS unpacking"""
        # Create test car with data.acd
        car_path = os.path.join(self.temp_dir, 'test_car')
        os.makedirs(car_path)
        acd_path = os.path.join(car_path, 'data.acd')
        with open(acd_path, 'wb') as f:
            f.write(b'fake acd data')
        
        # Mock successful subprocess run
        mock_run.return_value = Mock(returncode=0, stdout='', stderr='')
        
        # Mock finding QuickBMS and BMS script
        manager = CarFileManager(self.temp_dir, None)
        with patch.object(manager, 'find_quickbms', return_value='/fake/quickbms'):
            with patch.object(manager, 'find_acd_bms_script', return_value='/fake/acd.bms'):
                result = manager.unpack_data_acd_with_quickbms('test_car', 
                                                                backup_existing=False,
                                                                delete_acd=False)
                
                self.assertTrue(result)
                mock_run.assert_called_once()
                # Verify command structure
                call_args = mock_run.call_args[0][0]
                self.assertEqual(call_args[0], '/fake/quickbms')
                self.assertEqual(call_args[1], '-o')
                self.assertEqual(call_args[2], '/fake/acd.bms')
    
    @patch('subprocess.run')
    def test_unpack_with_quickbms_failure(self, mock_run):
        """Test failed QuickBMS unpacking"""
        # Create test car with data.acd
        car_path = os.path.join(self.temp_dir, 'test_car')
        os.makedirs(car_path)
        acd_path = os.path.join(car_path, 'data.acd')
        with open(acd_path, 'wb') as f:
            f.write(b'fake acd data')
        
        # Mock failed subprocess run
        mock_run.return_value = Mock(returncode=1, stdout='', stderr='Error')
        
        # Mock finding QuickBMS and BMS script
        manager = CarFileManager(self.temp_dir, None)
        with patch.object(manager, 'find_quickbms', return_value='/fake/quickbms'):
            with patch.object(manager, 'find_acd_bms_script', return_value='/fake/acd.bms'):
                result = manager.unpack_data_acd_with_quickbms('test_car',
                                                                backup_existing=False,
                                                                delete_acd=False)
                
                self.assertFalse(result)
    
    @patch('subprocess.run')
    def test_unpack_with_quickbms_timeout(self, mock_run):
        """Test QuickBMS timeout handling"""
        # Create test car with data.acd
        car_path = os.path.join(self.temp_dir, 'test_car')
        os.makedirs(car_path)
        acd_path = os.path.join(car_path, 'data.acd')
        with open(acd_path, 'wb') as f:
            f.write(b'fake acd data')
        
        # Mock timeout
        mock_run.side_effect = subprocess.TimeoutExpired('cmd', 60)
        
        # Mock finding QuickBMS and BMS script
        manager = CarFileManager(self.temp_dir, None)
        with patch.object(manager, 'find_quickbms', return_value='/fake/quickbms'):
            with patch.object(manager, 'find_acd_bms_script', return_value='/fake/acd.bms'):
                result = manager.unpack_data_acd_with_quickbms('test_car',
                                                                backup_existing=False,
                                                                delete_acd=False)
                
                self.assertFalse(result)
    
    def test_unpack_with_quickbms_not_found(self):
        """Test unpacking when QuickBMS not found"""
        # Create test car with data.acd
        car_path = os.path.join(self.temp_dir, 'test_car')
        os.makedirs(car_path)
        acd_path = os.path.join(car_path, 'data.acd')
        with open(acd_path, 'wb') as f:
            f.write(b'fake acd data')
        
        manager = CarFileManager(self.temp_dir, None)
        
        # Mock not finding QuickBMS
        with patch.object(manager, 'find_quickbms', return_value=None):
            result = manager.unpack_data_acd_with_quickbms('test_car',
                                                            backup_existing=False,
                                                            delete_acd=False)
            
            self.assertFalse(result)
    
    def test_unpack_with_quickbms_script_not_found(self):
        """Test unpacking when BMS script not found"""
        # Create test car with data.acd
        car_path = os.path.join(self.temp_dir, 'test_car')
        os.makedirs(car_path)
        acd_path = os.path.join(car_path, 'data.acd')
        with open(acd_path, 'wb') as f:
            f.write(b'fake acd data')
        
        manager = CarFileManager(self.temp_dir, None)
        
        # Mock finding QuickBMS but not BMS script
        with patch.object(manager, 'find_quickbms', return_value='/fake/quickbms'):
            with patch.object(manager, 'find_acd_bms_script', return_value=None):
                result = manager.unpack_data_acd_with_quickbms('test_car',
                                                                backup_existing=False,
                                                                delete_acd=False)
                
                self.assertFalse(result)
    
    @patch('subprocess.run')
    def test_unpack_with_quickbms_deletes_acd(self, mock_run):
        """Test that data.acd is deleted after successful unpacking"""
        # Create test car with data.acd
        car_path = os.path.join(self.temp_dir, 'test_car')
        os.makedirs(car_path)
        acd_path = os.path.join(car_path, 'data.acd')
        with open(acd_path, 'wb') as f:
            f.write(b'fake acd data')
        
        # Verify file exists
        self.assertTrue(os.path.exists(acd_path))
        
        # Mock successful subprocess run
        mock_run.return_value = Mock(returncode=0, stdout='', stderr='')
        
        # Mock finding QuickBMS and BMS script
        manager = CarFileManager(self.temp_dir, None)
        with patch.object(manager, 'find_quickbms', return_value='/fake/quickbms'):
            with patch.object(manager, 'find_acd_bms_script', return_value='/fake/acd.bms'):
                result = manager.unpack_data_acd_with_quickbms('test_car',
                                                                backup_existing=False,
                                                                delete_acd=True)
                
                self.assertTrue(result)
                # Verify data.acd was deleted
                self.assertFalse(os.path.exists(acd_path))


if __name__ == '__main__':
    unittest.main()
