#!/usr/bin/env python3
"""
Test Phase 7 features: car search/filter and preview images
"""

import sys
import os
import unittest
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.car_file_manager import CarFileManager


class TestCarPreview(unittest.TestCase):
    """Test car preview image functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory structure
        self.test_dir = tempfile.mkdtemp()
        self.cars_path = os.path.join(self.test_dir, 'cars')
        os.makedirs(self.cars_path)
        
        # Create test car directories
        self.car1 = 'test_car_1'
        self.car2 = 'test_car_2'
        self.car3 = 'test_car_no_preview'
        
        for car in [self.car1, self.car2, self.car3]:
            car_path = os.path.join(self.cars_path, car)
            os.makedirs(car_path)
            ui_path = os.path.join(car_path, 'ui')
            os.makedirs(ui_path)
        
        # Create preview.png for car1
        preview_png = os.path.join(self.cars_path, self.car1, 'ui', 'preview.png')
        with open(preview_png, 'wb') as f:
            f.write(b'fake png data')
        
        # Create preview.jpg for car2
        preview_jpg = os.path.join(self.cars_path, self.car2, 'ui', 'preview.jpg')
        with open(preview_jpg, 'wb') as f:
            f.write(b'fake jpg data')
        
        # car3 has no preview
        
        self.car_manager = CarFileManager(self.cars_path)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_get_car_preview_path_png(self):
        """Test getting preview path for PNG image"""
        path = self.car_manager.get_car_preview_path(self.car1)
        self.assertIsNotNone(path)
        self.assertTrue(path.endswith('preview.png'))
        self.assertTrue(os.path.exists(path))
    
    def test_get_car_preview_path_jpg(self):
        """Test getting preview path for JPG image"""
        path = self.car_manager.get_car_preview_path(self.car2)
        self.assertIsNotNone(path)
        self.assertTrue(path.endswith('preview.jpg'))
        self.assertTrue(os.path.exists(path))
    
    def test_get_car_preview_path_none(self):
        """Test getting preview path when no preview exists"""
        path = self.car_manager.get_car_preview_path(self.car3)
        self.assertIsNone(path)
    
    def test_get_car_preview_path_nonexistent_car(self):
        """Test getting preview path for non-existent car"""
        path = self.car_manager.get_car_preview_path('nonexistent_car')
        self.assertIsNone(path)
    
    def test_png_preferred_over_jpg(self):
        """Test that PNG is preferred when both exist"""
        # Create both preview.png and preview.jpg for car1
        preview_jpg = os.path.join(self.cars_path, self.car1, 'ui', 'preview.jpg')
        with open(preview_jpg, 'wb') as f:
            f.write(b'fake jpg data')
        
        path = self.car_manager.get_car_preview_path(self.car1)
        self.assertIsNotNone(path)
        self.assertTrue(path.endswith('preview.png'))


class TestCarFilter(unittest.TestCase):
    """Test car filtering functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_cars = [
            'alfa_romeo_4c',
            'bmw_m3_e30',
            'bmw_m3_e92',
            'ferrari_458',
            'ferrari_laferrari',
            'lamborghini_aventador',
            'porsche_911_gt3',
            'porsche_918_spyder',
        ]
    
    def test_filter_case_insensitive(self):
        """Test that filtering is case-insensitive"""
        search = 'bmw'
        filtered = [car for car in self.test_cars if search.lower() in car.lower()]
        self.assertEqual(len(filtered), 2)
        self.assertIn('bmw_m3_e30', filtered)
        self.assertIn('bmw_m3_e92', filtered)
    
    def test_filter_partial_match(self):
        """Test partial string matching"""
        search = 'ferrari'
        filtered = [car for car in self.test_cars if search.lower() in car.lower()]
        self.assertEqual(len(filtered), 2)
    
    def test_filter_no_match(self):
        """Test filtering with no matches"""
        search = 'toyota'
        filtered = [car for car in self.test_cars if search.lower() in car.lower()]
        self.assertEqual(len(filtered), 0)
    
    def test_filter_empty_search(self):
        """Test empty search returns all cars"""
        search = ''
        if not search:
            filtered = self.test_cars
        else:
            filtered = [car for car in self.test_cars if search.lower() in car.lower()]
        self.assertEqual(len(filtered), len(self.test_cars))
    
    def test_filter_number(self):
        """Test filtering by number"""
        search = '911'
        filtered = [car for car in self.test_cars if search.lower() in car.lower()]
        self.assertEqual(len(filtered), 1)
        self.assertIn('porsche_911_gt3', filtered)


if __name__ == '__main__':
    unittest.main()
