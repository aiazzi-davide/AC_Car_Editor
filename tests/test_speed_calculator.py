"""
Tests for Speed Calculator
"""

import unittest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.speed_calculator import SpeedCalculator


class TestSpeedCalculator(unittest.TestCase):
    """Test speed calculation for gear ratios"""
    
    def setUp(self):
        """Create temporary directory for test files"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_calculate_max_speed_basic(self):
        """Test basic speed calculation"""
        # Test with typical values: 1st gear
        # Gear: 3.5, Final: 4.1, RPM: 7000, Radius: 0.33m
        speed = SpeedCalculator.calculate_max_speed(3.5, 4.1, 7000, 0.33)
        
        # Expected: (7000 / (3.5 * 4.1)) * (2 * pi * 0.33) * 60 / 1000
        # = 487.8 rpm_wheel * 2.073 m_circumference * 0.06 = ~60.6 km/h
        self.assertAlmostEqual(speed, 60.6, delta=1.0)
    
    def test_calculate_max_speed_high_gear(self):
        """Test speed calculation for high gear"""
        # 6th gear: 0.8, Final: 4.1, RPM: 7000, Radius: 0.33m
        speed = SpeedCalculator.calculate_max_speed(0.8, 4.1, 7000, 0.33)
        
        # Expected: much higher speed
        self.assertGreater(speed, 250)
        self.assertLess(speed, 280)
    
    def test_calculate_max_speed_zero_gear(self):
        """Test speed calculation with zero gear ratio"""
        speed = SpeedCalculator.calculate_max_speed(0, 4.1, 7000, 0.33)
        self.assertEqual(speed, 0.0)
    
    def test_calculate_max_speed_zero_final(self):
        """Test speed calculation with zero final ratio"""
        speed = SpeedCalculator.calculate_max_speed(3.5, 0, 7000, 0.33)
        self.assertEqual(speed, 0.0)
    
    def test_calculate_max_speed_reverse(self):
        """Test speed calculation for reverse gear (negative ratio)"""
        # Reverse: -3.5, Final: 4.1, RPM: 7000, Radius: 0.33m
        speed = SpeedCalculator.calculate_max_speed(-3.5, 4.1, 7000, 0.33)
        
        # Should still calculate positive speed (abs used)
        self.assertGreater(speed, 50)
        self.assertLess(speed, 70)
    
    def test_get_tire_radius_from_ini(self):
        """Test reading tire radius from INI file"""
        # Create test tyres.ini
        tyres_ini = os.path.join(self.test_dir, 'tyres.ini')
        with open(tyres_ini, 'w') as f:
            f.write("[FRONT]\n")
            f.write("RADIUS=0.345\n")
        
        radius = SpeedCalculator.get_tire_radius_from_ini(tyres_ini, 0)
        self.assertAlmostEqual(radius, 0.345, places=3)
    
    def test_get_tire_radius_missing_file(self):
        """Test reading tire radius from non-existent file"""
        radius = SpeedCalculator.get_tire_radius_from_ini(
            os.path.join(self.test_dir, 'missing.ini')
        )
        self.assertIsNone(radius)
    
    def test_get_max_rpm_from_ini(self):
        """Test reading max RPM from INI file"""
        # Create test engine.ini
        engine_ini = os.path.join(self.test_dir, 'engine.ini')
        with open(engine_ini, 'w') as f:
            f.write("[ENGINE_DATA]\n")
            f.write("LIMITER=7500\n")
        
        max_rpm = SpeedCalculator.get_max_rpm_from_ini(engine_ini)
        self.assertEqual(max_rpm, 7500)
    
    def test_get_max_rpm_missing_file(self):
        """Test reading max RPM from non-existent file"""
        max_rpm = SpeedCalculator.get_max_rpm_from_ini(
            os.path.join(self.test_dir, 'missing.ini')
        )
        self.assertIsNone(max_rpm)
    
    def test_format_speed_normal(self):
        """Test speed formatting"""
        formatted = SpeedCalculator.format_speed(245.7)
        # Formatted rounds to nearest integer
        self.assertEqual(formatted, "246 km/h")
    
    def test_format_speed_zero(self):
        """Test formatting zero speed"""
        formatted = SpeedCalculator.format_speed(0)
        self.assertEqual(formatted, "N/A")
    
    def test_format_speed_negative(self):
        """Test formatting negative speed"""
        formatted = SpeedCalculator.format_speed(-10)
        self.assertEqual(formatted, "N/A")
    
    def test_realistic_car_speeds(self):
        """Test realistic car speed calculations"""
        # Typical sport car: 6-speed, 7000 RPM, 0.33m tire radius, 4.1 final
        max_rpm = 7000
        final = 4.1
        radius = 0.33
        
        gears = {
            1: 3.778,
            2: 2.050,
            3: 1.321,
            4: 0.970,
            5: 0.757,
            6: 0.625
        }
        
        speeds = {}
        for gear_num, gear_ratio in gears.items():
            speeds[gear_num] = SpeedCalculator.calculate_max_speed(
                gear_ratio, final, max_rpm, radius
            )
        
        # Check speeds are increasing
        self.assertLess(speeds[1], speeds[2])
        self.assertLess(speeds[2], speeds[3])
        self.assertLess(speeds[5], speeds[6])
        
        # Check reasonable values
        self.assertGreater(speeds[1], 45)  # 1st gear > 45 km/h
        self.assertLess(speeds[1], 65)    # 1st gear < 65 km/h
        self.assertGreater(speeds[6], 240)  # 6th gear > 240 km/h
        self.assertLess(speeds[6], 350)    # 6th gear < 350 km/h


if __name__ == '__main__':
    unittest.main()
