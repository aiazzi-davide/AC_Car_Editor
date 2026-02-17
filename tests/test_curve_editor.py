"""
Test cases for the curve editor functionality (non-GUI tests)
"""

import unittest
import os
import sys
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.lut_parser import LUTCurve


class TestCurveEditorIntegration(unittest.TestCase):
    """Integration tests for curve editor (non-GUI)"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.lut')
        
        # Create a test LUT file
        curve = LUTCurve()
        curve.add_point(1000, 100)
        curve.add_point(2000, 200)
        curve.add_point(3000, 300)
        curve.save(self.test_file, backup=False)
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
        
    def test_load_curve_for_editing(self):
        """Test loading a curve for editing"""
        curve = LUTCurve(self.test_file)
        curve.load()
        
        points = curve.get_points()
        self.assertEqual(len(points), 3)
        self.assertEqual(points[0], (1000, 100))
        self.assertEqual(points[1], (2000, 200))
        self.assertEqual(points[2], (3000, 300))
        
    def test_modify_and_save_curve(self):
        """Test modifying a curve and saving with backup"""
        # Load
        curve = LUTCurve(self.test_file)
        curve.load()
        
        # Modify
        curve.add_point(4000, 400)
        curve.add_point(5000, 500)
        
        # Save with backup
        curve.save(self.test_file, backup=True)
        
        # Verify backup exists
        self.assertTrue(os.path.exists(self.test_file + '.bak'))
        
        # Verify modified file
        new_curve = LUTCurve(self.test_file)
        new_curve.load()
        points = new_curve.get_points()
        self.assertEqual(len(points), 5)
        self.assertEqual(points[3], (4000, 400))
        self.assertEqual(points[4], (5000, 500))
        
        # Verify backup has original data
        backup_curve = LUTCurve(self.test_file + '.bak')
        backup_curve.load()
        backup_points = backup_curve.get_points()
        self.assertEqual(len(backup_points), 3)
        
    def test_create_new_curve(self):
        """Test creating a new curve from scratch"""
        new_file = os.path.join(self.test_dir, 'new_curve.lut')
        
        curve = LUTCurve()
        
        # Add points in random order
        curve.add_point(3000, 300)
        curve.add_point(1000, 100)
        curve.add_point(2000, 200)
        
        # Save
        curve.save(new_file, backup=False)
        
        # Verify file exists
        self.assertTrue(os.path.exists(new_file))
        
        # Load and verify sorting
        loaded_curve = LUTCurve(new_file)
        loaded_curve.load()
        points = loaded_curve.get_points()
        
        self.assertEqual(len(points), 3)
        self.assertEqual(points[0], (1000, 100))
        self.assertEqual(points[1], (2000, 200))
        self.assertEqual(points[2], (3000, 300))
        
    def test_remove_point_from_curve(self):
        """Test removing a point from a curve"""
        curve = LUTCurve(self.test_file)
        curve.load()
        
        # Remove middle point
        curve.remove_point(1)
        
        points = curve.get_points()
        self.assertEqual(len(points), 2)
        self.assertEqual(points[0], (1000, 100))
        self.assertEqual(points[1], (3000, 300))
        
        # Save
        curve.save(self.test_file, backup=True)
        
        # Verify
        new_curve = LUTCurve(self.test_file)
        new_curve.load()
        self.assertEqual(len(new_curve.get_points()), 2)
        
    def test_update_point_in_curve(self):
        """Test updating a point in a curve"""
        curve = LUTCurve(self.test_file)
        curve.load()
        
        # Update middle point
        curve.update_point(1, 2500, 250)
        
        points = curve.get_points()
        self.assertEqual(len(points), 3)
        # After sorting
        self.assertEqual(points[0], (1000, 100))
        self.assertEqual(points[1], (2500, 250))
        self.assertEqual(points[2], (3000, 300))
        
    def test_export_import_workflow(self):
        """Test exporting and importing curves"""
        # Load original
        original_curve = LUTCurve(self.test_file)
        original_curve.load()
        
        # Export to new file
        export_file = os.path.join(self.test_dir, 'exported.lut')
        original_curve.save(export_file, backup=False)
        
        # Import from exported file
        imported_curve = LUTCurve(export_file)
        imported_curve.load()
        
        # Verify data matches
        original_points = original_curve.get_points()
        imported_points = imported_curve.get_points()
        self.assertEqual(original_points, imported_points)
        
    def test_preset_curve_creation(self):
        """Test creating curves with preset patterns"""
        # Linear preset
        linear_curve = LUTCurve()
        for i in range(0, 6):
            linear_curve.add_point(i * 1000, i * 100)
        
        points = linear_curve.get_points()
        self.assertEqual(len(points), 6)
        self.assertEqual(points[0], (0, 0))
        self.assertEqual(points[5], (5000, 500))
        
        # Turbo lag preset (exponential-ish growth)
        turbo_curve = LUTCurve()
        turbo_data = [
            (0, 0), (1000, 50), (2000, 80), (2500, 120), 
            (3000, 200), (4000, 300), (5000, 350), 
            (6000, 380), (7000, 390)
        ]
        for x, y in turbo_data:
            turbo_curve.add_point(x, y)
            
        points = turbo_curve.get_points()
        self.assertEqual(len(points), 9)
        self.assertEqual(points[0], (0, 0))
        self.assertEqual(points[-1], (7000, 390))


if __name__ == '__main__':
    unittest.main()
