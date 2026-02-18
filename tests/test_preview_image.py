"""
Tests for car preview image functionality
"""

import sys
import os
import unittest
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.car_file_manager import CarFileManager


class TestPreviewImage(unittest.TestCase):
    """Test car preview image feature"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temp directory structure
        self.temp_dir = tempfile.mkdtemp()
        self.cars_path = os.path.join(self.temp_dir, 'cars')
        os.makedirs(self.cars_path)
        
        # Create test car with preview
        self.car_with_preview = 'test_car_with_preview'
        car_path = os.path.join(self.cars_path, self.car_with_preview)
        ui_path = os.path.join(car_path, 'ui')
        os.makedirs(ui_path)
        
        # Create a simple preview.png
        preview_path = os.path.join(ui_path, 'preview.png')
        with open(preview_path, 'wb') as f:
            # Write minimal PNG header
            f.write(b'\x89PNG\r\n\x1a\n')
        
        # Create test car without preview
        self.car_no_preview = 'test_car_no_preview'
        car_path_no_preview = os.path.join(self.cars_path, self.car_no_preview)
        os.makedirs(car_path_no_preview)
        
        # Initialize manager
        self.manager = CarFileManager(self.cars_path)
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_get_car_preview_path_exists(self):
        """Test getting preview path when it exists"""
        preview_path = self.manager.get_car_preview_path(self.car_with_preview)
        self.assertIsNotNone(preview_path)
        self.assertTrue(os.path.exists(preview_path))
        self.assertTrue(preview_path.endswith('preview.png'))
    
    def test_get_car_preview_path_not_exists(self):
        """Test getting preview path when it doesn't exist"""
        preview_path = self.manager.get_car_preview_path(self.car_no_preview)
        self.assertIsNone(preview_path)
    
    def test_get_car_info_includes_preview(self):
        """Test that get_car_info includes preview_path"""
        info = self.manager.get_car_info(self.car_with_preview)
        self.assertIn('preview_path', info)
        self.assertIsNotNone(info['preview_path'])
        self.assertTrue(os.path.exists(info['preview_path']))
    
    def test_get_car_info_no_preview(self):
        """Test that get_car_info handles missing preview"""
        info = self.manager.get_car_info(self.car_no_preview)
        self.assertIn('preview_path', info)
        self.assertIsNone(info['preview_path'])
    
    def test_preview_jpg_support(self):
        """Test that .jpg previews are also supported"""
        car_name = 'test_car_jpg'
        car_path = os.path.join(self.cars_path, car_name)
        ui_path = os.path.join(car_path, 'ui')
        os.makedirs(ui_path)
        
        # Create preview.jpg
        preview_path = os.path.join(ui_path, 'preview.jpg')
        with open(preview_path, 'wb') as f:
            f.write(b'\xff\xd8\xff')  # JPEG header
        
        found_path = self.manager.get_car_preview_path(car_name)
        self.assertIsNotNone(found_path)
        self.assertTrue(found_path.endswith('preview.jpg'))


if __name__ == '__main__':
    unittest.main()
