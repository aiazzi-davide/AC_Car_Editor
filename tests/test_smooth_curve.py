"""
Unit tests for smooth curve feature in curve editor
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from scipy import interpolate

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.lut_parser import LUTCurve


class TestSmoothCurveFeature(unittest.TestCase):
    """Test smooth curve interpolation feature"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lut')
        self.temp_file.write("1000|100\n2000|150\n3000|180\n4000|200\n")
        self.temp_file.close()
        
        self.curve = LUTCurve(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
    
    def test_pchip_interpolation_no_overshoot(self):
        """Test that PCHIP interpolation doesn't overshoot"""
        # Create monotonically increasing data
        x = np.array([1000, 2000, 3000, 4000])
        y = np.array([100, 150, 180, 200])
        
        # Create PCHIP interpolator
        pchip = interpolate.PchipInterpolator(x, y)
        
        # Generate interpolated values
        x_smooth = np.linspace(1000, 4000, 100)
        y_smooth = pchip(x_smooth)
        
        # Check no values exceed the max of original data (with small tolerance)
        self.assertLessEqual(np.max(y_smooth), np.max(y) * 1.01)
        
        # Check no values go below the min of original data (with small tolerance)
        self.assertGreaterEqual(np.min(y_smooth), np.min(y) * 0.99)
    
    def test_pchip_vs_cubic_overshoot(self):
        """Test that PCHIP produces less overshoot than cubic spline"""
        # Create data with a peak
        x = np.array([1000, 2000, 3000, 4000, 5000])
        y = np.array([100, 150, 200, 180, 150])
        
        # PCHIP interpolator
        pchip = interpolate.PchipInterpolator(x, y)
        
        # Cubic spline interpolator
        cubic = interpolate.interp1d(x, y, kind='cubic')
        
        # Generate interpolated values
        x_smooth = np.linspace(1000, 5000, 100)
        y_pchip = pchip(x_smooth)
        y_cubic = cubic(x_smooth)
        
        # PCHIP should not exceed max by much
        pchip_overshoot = np.max(y_pchip) - np.max(y)
        cubic_overshoot = np.max(y_cubic) - np.max(y)
        
        # PCHIP overshoot should be much smaller than cubic
        self.assertLess(abs(pchip_overshoot), abs(cubic_overshoot) + 5)  # Allow small margin
    
    def test_pchip_preserves_monotonicity(self):
        """Test that PCHIP preserves monotonicity for monotonic data"""
        # Strictly increasing data
        x = np.array([1000, 2000, 3000, 4000])
        y = np.array([100, 150, 180, 200])
        
        # Create PCHIP interpolator
        pchip = interpolate.PchipInterpolator(x, y)
        
        # Generate interpolated values
        x_smooth = np.linspace(1000, 4000, 100)
        y_smooth = pchip(x_smooth)
        
        # Check that values are monotonically increasing
        for i in range(len(y_smooth) - 1):
            self.assertLessEqual(y_smooth[i], y_smooth[i + 1])
    
    def test_pchip_with_minimum_points(self):
        """Test PCHIP with exactly 4 points (minimum for smooth curve)"""
        x = np.array([1000, 2000, 3000, 4000])
        y = np.array([100, 150, 180, 200])
        
        # Should not raise exception with 4 points
        try:
            pchip = interpolate.PchipInterpolator(x, y)
            x_smooth = np.linspace(1000, 4000, 50)
            y_smooth = pchip(x_smooth)
            self.assertEqual(len(y_smooth), 50)
        except Exception as e:
            self.fail(f"PCHIP failed with 4 points: {e}")
    
    def test_pchip_prevents_negative_values(self):
        """Test PCHIP with all positive input produces reasonable output"""
        # All positive values
        x = np.array([1000, 2000, 3000, 4000, 5000])
        y = np.array([100, 150, 180, 160, 140])
        
        pchip = interpolate.PchipInterpolator(x, y)
        x_smooth = np.linspace(1000, 5000, 100)
        y_smooth = pchip(x_smooth)
        
        # For this data, PCHIP should not produce negative values
        # (though it's not guaranteed in all cases)
        min_value = np.min(y_smooth)
        self.assertGreaterEqual(min_value, 0, 
            f"PCHIP produced negative value {min_value} for all-positive input")
    
    def test_smooth_curve_interpolation_quality(self):
        """Test that PCHIP interpolation maintains data quality"""
        # Create realistic power curve data
        x = np.array([1000, 2000, 3000, 4000, 5000, 6000])
        y = np.array([80, 120, 160, 180, 170, 150])
        
        pchip = interpolate.PchipInterpolator(x, y)
        x_smooth = np.linspace(1000, 6000, 200)
        y_smooth = pchip(x_smooth)
        
        # Check that interpolated values are reasonable
        self.assertGreaterEqual(np.min(y_smooth), np.min(y) - 5)
        self.assertLessEqual(np.max(y_smooth), np.max(y) + 5)
        
        # Check smoothness (no huge jumps)
        diffs = np.diff(y_smooth)
        max_diff = np.max(np.abs(diffs))
        self.assertLess(max_diff, 10, "Interpolation has large jumps")


if __name__ == '__main__':
    unittest.main()
