"""
Tests for car comparison functionality
"""

import sys
import os
import unittest
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.car_file_manager import CarFileManager
from src.core.ini_parser import IniParser


class TestCarComparison(unittest.TestCase):
    """Test car comparison feature"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temp directory structure
        self.temp_dir = tempfile.mkdtemp()
        self.cars_path = os.path.join(self.temp_dir, 'cars')
        os.makedirs(self.cars_path)
        
        # Create two test cars
        self.create_test_car('test_car_1', mass='1200', power='300', limiter='7500')
        self.create_test_car('test_car_2', mass='1400', power='400', limiter='8000')
        
        # Initialize manager
        self.manager = CarFileManager(self.cars_path)
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_test_car(self, car_name, mass='1200', power='300', limiter='7500'):
        """Create a test car with basic INI files"""
        car_path = os.path.join(self.cars_path, car_name)
        data_path = os.path.join(car_path, 'data')
        os.makedirs(data_path)
        
        # Create car.ini
        car_ini_path = os.path.join(data_path, 'car.ini')
        with open(car_ini_path, 'w') as f:
            f.write(f"""[BASIC]
SCREEN_NAME={car_name}
TOTALMASS={mass}
WEIGHTDISTRIBUTION=0.50
""")
        
        # Create engine.ini
        engine_ini_path = os.path.join(data_path, 'engine.ini')
        with open(engine_ini_path, 'w') as f:
            f.write(f"""[ENGINE_DATA]
LIMITER={limiter}
INERTIA=0.15
""")
        
        # Create power.lut
        power_lut_path = os.path.join(data_path, 'power.lut')
        with open(power_lut_path, 'w') as f:
            f.write(f"""# Power curve
1000|100
3000|{power}
7000|{power}
{limiter}|250
""")
        
        # Create suspensions.ini
        susp_ini_path = os.path.join(data_path, 'suspensions.ini')
        with open(susp_ini_path, 'w') as f:
            f.write("""[BASIC]
WHEELBASE=2.5

[FRONT]
TRACK=1.5

[REAR]
TRACK=1.5
""")
        
        # Create drivetrain.ini
        dt_ini_path = os.path.join(data_path, 'drivetrain.ini')
        with open(dt_ini_path, 'w') as f:
            f.write("""[TRACTION]
TYPE=RWD

[GEARS]
FINAL=3.5
""")
    
    def test_car_specs_extraction(self):
        """Test extracting car specifications"""
        # We can't directly test the GUI dialog, but we can test that
        # the necessary files exist and can be parsed
        car1_info = self.manager.get_car_info('test_car_1')
        self.assertTrue(car1_info['has_data_folder'])
        
        # Test that INI files exist
        car_ini = self.manager.get_ini_file_path('test_car_1', 'car.ini')
        self.assertTrue(os.path.exists(car_ini))
        
        engine_ini = self.manager.get_ini_file_path('test_car_1', 'engine.ini')
        self.assertTrue(os.path.exists(engine_ini))
        
        # Test parsing
        car_parser = IniParser(car_ini)
        self.assertEqual(car_parser.get_value('BASIC', 'TOTALMASS'), '1200')
        
        engine_parser = IniParser(engine_ini)
        self.assertEqual(engine_parser.get_value('ENGINE_DATA', 'LIMITER'), '7500')
    
    def test_multiple_cars_available(self):
        """Test that multiple cars are available for comparison"""
        cars = self.manager.get_car_list()
        self.assertGreaterEqual(len(cars), 2)
        self.assertIn('test_car_1', cars)
        self.assertIn('test_car_2', cars)
    
    def test_different_car_specs(self):
        """Test that cars have different specs"""
        car1_ini = self.manager.get_ini_file_path('test_car_1', 'car.ini')
        car2_ini = self.manager.get_ini_file_path('test_car_2', 'car.ini')
        
        car1_parser = IniParser(car1_ini)
        car2_parser = IniParser(car2_ini)
        
        # Different masses
        mass1 = car1_parser.get_value('BASIC', 'TOTALMASS')
        mass2 = car2_parser.get_value('BASIC', 'TOTALMASS')
        self.assertNotEqual(mass1, mass2)
    
    def test_power_lut_parsing(self):
        """Test parsing power.lut for comparison"""
        power_lut_path = os.path.join(
            self.manager.get_car_data_path('test_car_1'),
            'power.lut'
        )
        
        self.assertTrue(os.path.exists(power_lut_path))
        
        # Parse power values
        max_power = 0
        with open(power_lut_path, 'r') as f:
            for line in f:
                line = line.split('#')[0].strip()
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) == 2:
                        power = float(parts[1])
                        max_power = max(max_power, power)
        
        self.assertGreater(max_power, 0)


if __name__ == '__main__':
    unittest.main()
