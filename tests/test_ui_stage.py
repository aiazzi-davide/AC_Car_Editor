"""
Tests for UI Manager and Stage Tuning System
"""

import unittest
import os
import sys
import tempfile
import shutil
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.ui_manager import UIManager
from core.stage_tuner import StageTuner
from core.ini_parser import IniParser
from core.lut_parser import LUTCurve


class TestUIManager(unittest.TestCase):
    """Test UI Manager for ui_car.json handling"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.car_path = os.path.join(self.test_dir, 'test_car')
        self.ui_path = os.path.join(self.car_path, 'ui')
        os.makedirs(self.ui_path)
        
        # Create a sample ui_car.json
        self.sample_data = {
            'name': 'Test Car',
            'brand': 'Test Brand',
            'class': 'street',
            'country': 'Italy',
            'description': 'A test car',
            'tags': ['test', 'street'],
            'specs': {
                'bhp': '200 bhp',
                'torque': '300 Nm',
                'weight': '1400 kg',
            },
            'year': 2020,
            'author': 'Test Author',
            'version': '1.0'
        }
        
        with open(os.path.join(self.ui_path, 'ui_car.json'), 'w') as f:
            json.dump(self.sample_data, f)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_load_ui_car_json(self):
        """Test loading ui_car.json"""
        manager = UIManager(self.car_path)
        self.assertTrue(manager.has_ui_car_json())
        self.assertEqual(manager.get_name(), 'Test Car')
        self.assertEqual(manager.get_brand(), 'Test Brand')
        self.assertEqual(manager.get_country(), 'Italy')
        self.assertEqual(manager.get_year(), 2020)
    
    def test_modify_ui_car_json(self):
        """Test modifying ui_car.json"""
        manager = UIManager(self.car_path)
        manager.set_name('Modified Car')
        manager.set_brand('New Brand')
        manager.set_year(2025)
        
        self.assertEqual(manager.get_name(), 'Modified Car')
        self.assertEqual(manager.get_brand(), 'New Brand')
        self.assertEqual(manager.get_year(), 2025)
    
    def test_save_ui_car_json(self):
        """Test saving ui_car.json"""
        manager = UIManager(self.car_path)
        manager.set_name('Saved Car')
        manager.save(backup=True)
        
        # Verify backup was created
        backup_path = os.path.join(self.ui_path, 'ui_car.json.bak')
        self.assertTrue(os.path.exists(backup_path))
        
        # Reload and verify
        manager2 = UIManager(self.car_path)
        self.assertEqual(manager2.get_name(), 'Saved Car')
    
    def test_create_default_ui_car_json(self):
        """Test creating default ui_car.json"""
        new_car_path = os.path.join(self.test_dir, 'new_car')
        os.makedirs(os.path.join(new_car_path, 'ui'))
        
        manager = UIManager(new_car_path)
        manager.create_default_ui_car_json('new_car')
        manager.save(backup=False)
        
        self.assertTrue(os.path.exists(os.path.join(new_car_path, 'ui', 'ui_car.json')))
        self.assertEqual(manager.get_name(), 'new_car')
    
    def test_tags_handling(self):
        """Test tags list handling"""
        manager = UIManager(self.car_path)
        tags = ['turbo', 'awd', 'sport']
        manager.set_tags(tags)
        self.assertEqual(manager.get_tags(), tags)
    
    def test_specs_handling(self):
        """Test specs dictionary handling"""
        manager = UIManager(self.car_path)
        specs = {
            'bhp': '300 bhp',
            'torque': '400 Nm',
            'weight': '1200 kg',
        }
        manager.set_specs(specs)
        saved_specs = manager.get_specs()
        self.assertEqual(saved_specs['bhp'], '300 bhp')
        self.assertEqual(saved_specs['torque'], '400 Nm')


class TestStageTuner(unittest.TestCase):
    """Test Stage Tuning System"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.data_path = os.path.join(self.test_dir, 'data')
        os.makedirs(self.data_path)
        
        # Create basic engine.ini
        self.engine_ini_path = os.path.join(self.data_path, 'engine.ini')
        with open(self.engine_ini_path, 'w') as f:
            f.write("[ENGINE_DATA]\n")
            f.write("MINIMUM=1000\n")
            f.write("MAXIMUM=7000\n")
            f.write("LIMITER=7500\n")
            f.write("INERTIA=0.20\n")
        
        # Create power.lut
        self.power_lut_path = os.path.join(self.data_path, 'power.lut')
        with open(self.power_lut_path, 'w') as f:
            f.write("1000|100\n")
            f.write("3000|200\n")
            f.write("5000|300\n")
            f.write("7000|280\n")
        
        # Create car.ini
        self.car_ini_path = os.path.join(self.data_path, 'car.ini')
        with open(self.car_ini_path, 'w') as f:
            f.write("[BASIC]\n")
            f.write("TOTALMASS=1400\n")
        
        # Create aero.ini
        self.aero_ini_path = os.path.join(self.data_path, 'aero.ini')
        with open(self.aero_ini_path, 'w') as f:
            f.write("[HEADER]\n")
            f.write("CD=0.35\n")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_detect_na_car(self):
        """Test detection of NA (non-turbo) car"""
        tuner = StageTuner(self.data_path)
        self.assertFalse(tuner.is_turbo)
    
    def test_detect_turbo_car(self):
        """Test detection of turbo car"""
        # Add turbo section
        parser = IniParser(self.engine_ini_path)
        parser.set_value('TURBO_0', 'MAX_BOOST', '0.5')
        parser.save(backup=False)
        
        tuner = StageTuner(self.data_path)
        self.assertTrue(tuner.is_turbo)
    
    def test_stage_1_na(self):
        """Test Stage 1 application on NA car"""
        tuner = StageTuner(self.data_path)
        self.assertFalse(tuner.is_turbo)
        
        # Apply Stage 1
        result = tuner.apply_stage_1()
        self.assertTrue(result)
        
        # Verify power curve increased by 8%
        curve = LUTCurve(self.power_lut_path)
        # Original: 1000|100, should be ~1000|108
        self.assertAlmostEqual(curve.points[0][1], 108, delta=1)
        
        # Verify stage marker
        parser = IniParser(self.engine_ini_path)
        stage = parser.get_value('HEADER', 'STAGE_LEVEL', default='0')
        self.assertEqual(stage, '1')
    
    def test_stage_1_turbo(self):
        """Test Stage 1 application on turbo car"""
        # Add turbo section
        parser = IniParser(self.engine_ini_path)
        parser.set_value('TURBO_0', 'MAX_BOOST', '0.50')
        parser.save(backup=False)
        
        tuner = StageTuner(self.data_path)
        self.assertTrue(tuner.is_turbo)
        
        # Apply Stage 1
        result = tuner.apply_stage_1()
        self.assertTrue(result)
        
        # Verify boost increased by 15%
        parser = IniParser(self.engine_ini_path)
        new_boost = float(parser.get_value('TURBO_0', 'MAX_BOOST'))
        self.assertAlmostEqual(new_boost, 0.575, delta=0.01)  # 0.5 * 1.15 = 0.575
    
    def test_stage_2_na_adds_turbo(self):
        """Test Stage 2 on NA car adds turbo system"""
        tuner = StageTuner(self.data_path)
        self.assertFalse(tuner.is_turbo)
        
        # Apply Stage 2
        result = tuner.apply_stage_2()
        self.assertTrue(result)
        
        # Verify turbo was added
        parser = IniParser(self.engine_ini_path)
        self.assertTrue(parser.has_section('TURBO_0'))
        max_boost = parser.get_value('TURBO_0', 'MAX_BOOST')
        self.assertIsNotNone(max_boost)
    
    def test_stage_2_turbo_increases_boost(self):
        """Test Stage 2 on turbo car increases boost"""
        # Add turbo section
        parser = IniParser(self.engine_ini_path)
        parser.set_value('TURBO_0', 'MAX_BOOST', '0.50')
        parser.save(backup=False)
        
        tuner = StageTuner(self.data_path)
        self.assertTrue(tuner.is_turbo)
        
        # Apply Stage 2
        result = tuner.apply_stage_2()
        self.assertTrue(result)
        
        # Verify boost increased by 30%
        parser = IniParser(self.engine_ini_path)
        new_boost = float(parser.get_value('TURBO_0', 'MAX_BOOST'))
        self.assertAlmostEqual(new_boost, 0.65, delta=0.01)  # 0.5 * 1.30 = 0.65
    
    def test_stage_3_na_full_build(self):
        """Test Stage 3 on NA car (full build)"""
        tuner = StageTuner(self.data_path)
        
        # Apply Stage 3
        result = tuner.apply_stage_3()
        self.assertTrue(result)
        
        # Verify turbo added
        parser = IniParser(self.engine_ini_path)
        self.assertTrue(parser.has_section('TURBO_0'))
        
        # Verify weight reduction
        car_parser = IniParser(self.car_ini_path)
        new_mass = float(car_parser.get_value('BASIC', 'TOTALMASS'))
        self.assertAlmostEqual(new_mass, 1330, delta=5)  # 1400 * 0.95 = 1330
        
        # Verify aero improvement
        aero_parser = IniParser(self.aero_ini_path)
        new_cd = float(aero_parser.get_value('HEADER', 'CD'))
        self.assertAlmostEqual(new_cd, 0.315, delta=0.01)  # 0.35 * 0.90 = 0.315
    
    def test_stage_3_turbo_full_build(self):
        """Test Stage 3 on turbo car (full build)"""
        # Add turbo section
        parser = IniParser(self.engine_ini_path)
        parser.set_value('TURBO_0', 'MAX_BOOST', '0.50')
        parser.save(backup=False)
        
        tuner = StageTuner(self.data_path)
        
        # Apply Stage 3
        result = tuner.apply_stage_3()
        self.assertTrue(result)
        
        # Verify boost increased by 50%
        parser = IniParser(self.engine_ini_path)
        new_boost = float(parser.get_value('TURBO_0', 'MAX_BOOST'))
        self.assertAlmostEqual(new_boost, 0.75, delta=0.01)  # 0.5 * 1.50 = 0.75
        
        # Verify RPM limit increased
        new_limiter = int(float(parser.get_value('ENGINE_DATA', 'LIMITER')))
        self.assertEqual(new_limiter, 8000)  # 7500 + 500 = 8000
    
    def test_get_current_stage(self):
        """Test getting current stage level"""
        tuner = StageTuner(self.data_path)
        self.assertEqual(tuner.get_current_stage(), 0)
        
        # Apply Stage 1 and check
        tuner.apply_stage_1()
        tuner2 = StageTuner(self.data_path)
        self.assertEqual(tuner2.get_current_stage(), 1)
    
    def test_reset_to_stock(self):
        """Test resetting stage to stock"""
        tuner = StageTuner(self.data_path)
        tuner.apply_stage_1()
        
        # Reset
        result = tuner.reset_to_stock()
        self.assertTrue(result)
        
        # Verify stage cleared
        tuner2 = StageTuner(self.data_path)
        self.assertEqual(tuner2.get_current_stage(), 0)
    
    def test_stage_descriptions(self):
        """Test stage description retrieval"""
        tuner = StageTuner(self.data_path)
        
        desc1 = tuner.get_stage_description(1)
        self.assertIn('title', desc1)
        self.assertIn('description', desc1)
        
        # Check that NA descriptions differ from turbo descriptions
        # Add turbo and check again
        parser = IniParser(self.engine_ini_path)
        parser.set_value('TURBO_0', 'MAX_BOOST', '0.5')
        parser.save(backup=False)
        
        tuner_turbo = StageTuner(self.data_path)
        desc1_turbo = tuner_turbo.get_stage_description(1)
        
        # Descriptions should be different
        self.assertNotEqual(desc1['description'], desc1_turbo['description'])


if __name__ == '__main__':
    unittest.main()
