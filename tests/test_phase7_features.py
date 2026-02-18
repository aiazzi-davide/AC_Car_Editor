"""
Tests for PowerTorqueCalculator and SetupManager.
"""

import unittest
import os
import sys
import tempfile
import shutil
import json
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.power_calculator import PowerTorqueCalculator
from core.setup_manager import SetupManager


class TestPowerTorqueCalculator(unittest.TestCase):
    """Test power/torque calculator."""

    def setUp(self):
        self.power_points = [
            (1000, 100),
            (2000, 150),
            (3000, 200),
            (4000, 280),
            (5000, 350),
            (6000, 400),
            (7000, 420),
            (8000, 430),
            (8500, 425),
        ]
        self.turbo_config = [{
            'max_boost': 1.5,
            'wastegate': 1.2,
            'reference_rpm': 3000,
            'gamma': 2.5,
        }]

    def test_hp_to_torque(self):
        """Test HP to Nm conversion."""
        # At 5252 RPM, 100 HP ≈ 100 lb·ft ≈ 135.58 Nm
        # Formula: Torque = HP * 745.7 / (RPM * 2π/60)
        torque = PowerTorqueCalculator.hp_to_torque_nm(100, 5252)
        # HP * 745.7 / (5252 * 2*pi/60) = 74570 / (5252 * 0.10472)
        expected = 100 * 745.7 / (5252 * 2 * math.pi / 60)
        self.assertAlmostEqual(torque, expected, places=1)

    def test_hp_to_torque_zero_rpm(self):
        """Torque at zero RPM should be 0."""
        self.assertEqual(PowerTorqueCalculator.hp_to_torque_nm(100, 0), 0.0)

    def test_interpolation_exact_point(self):
        """Interpolation at an exact curve point should return that value."""
        calc = PowerTorqueCalculator(self.power_points)
        self.assertEqual(calc.interpolate_power(3000), 200.0)

    def test_interpolation_between_points(self):
        """Interpolation between two points should give intermediate value."""
        calc = PowerTorqueCalculator(self.power_points)
        val = calc.interpolate_power(3500)
        self.assertGreater(val, 200)
        self.assertLess(val, 280)

    def test_interpolation_before_first_point(self):
        """Before first point, should return first Y value."""
        calc = PowerTorqueCalculator(self.power_points)
        self.assertEqual(calc.interpolate_power(500), 100.0)

    def test_interpolation_after_last_point(self):
        """After last point, should return last Y value."""
        calc = PowerTorqueCalculator(self.power_points)
        self.assertEqual(calc.interpolate_power(10000), 425.0)

    def test_boost_no_turbo(self):
        """Without turbo configs, boost should be 0."""
        calc = PowerTorqueCalculator(self.power_points)
        self.assertEqual(calc.boost_at_rpm(5000), 0.0)

    def test_boost_at_reference_rpm(self):
        """At reference RPM, boost should equal max_boost."""
        calc = PowerTorqueCalculator(self.power_points, self.turbo_config)
        boost = calc.boost_at_rpm(3000)
        self.assertAlmostEqual(boost, 1.5, places=3)

    def test_boost_above_reference_rpm(self):
        """Above reference RPM, boost is clamped to max_boost."""
        calc = PowerTorqueCalculator(self.power_points, self.turbo_config)
        boost = calc.boost_at_rpm(8000)
        self.assertAlmostEqual(boost, 1.5, places=3)

    def test_boost_below_reference_rpm(self):
        """Below reference RPM, boost should be less than max_boost."""
        calc = PowerTorqueCalculator(self.power_points, self.turbo_config)
        boost = calc.boost_at_rpm(1500)
        self.assertGreater(boost, 0.0)
        self.assertLess(boost, 1.5)

    def test_boost_at_zero_rpm(self):
        """At 0 RPM, boost should be 0."""
        calc = PowerTorqueCalculator(self.power_points, self.turbo_config)
        self.assertEqual(calc.boost_at_rpm(0), 0.0)

    def test_effective_power_with_turbo(self):
        """Effective power should be base × (1 + boost)."""
        calc = PowerTorqueCalculator(self.power_points, self.turbo_config)
        # At 3000 RPM: base=200, boost=1.5 → effective = 200 * 2.5 = 500
        eff = calc.effective_power(3000)
        self.assertAlmostEqual(eff, 200 * (1 + 1.5), places=1)

    def test_effective_power_no_turbo(self):
        """Without turbo, effective equals base."""
        calc = PowerTorqueCalculator(self.power_points)
        self.assertEqual(calc.effective_power(3000), 200.0)

    def test_compute_curves_structure(self):
        """compute_curves should return all expected keys."""
        calc = PowerTorqueCalculator(self.power_points, self.turbo_config)
        result = calc.compute_curves()
        expected_keys = ['rpm_values', 'base_hp', 'base_torque',
                         'effective_hp', 'effective_torque', 'boost_curve',
                         'peak_base_hp', 'peak_base_torque',
                         'peak_eff_hp', 'peak_eff_torque']
        for key in expected_keys:
            self.assertIn(key, result)

    def test_compute_curves_lengths_match(self):
        """All curve arrays should have the same length."""
        calc = PowerTorqueCalculator(self.power_points, self.turbo_config)
        result = calc.compute_curves()
        n = len(result['rpm_values'])
        self.assertEqual(len(result['base_hp']), n)
        self.assertEqual(len(result['base_torque']), n)
        self.assertEqual(len(result['effective_hp']), n)
        self.assertEqual(len(result['effective_torque']), n)
        self.assertEqual(len(result['boost_curve']), n)

    def test_peak_values(self):
        """Peak values should be correctly identified."""
        calc = PowerTorqueCalculator(self.power_points)
        result = calc.compute_curves(rpm_step=100)
        peak_hp_rpm, peak_hp = result['peak_base_hp']
        # The peak HP in our data is 430 at 8000 RPM
        self.assertAlmostEqual(peak_hp, 430.0, places=0)
        self.assertAlmostEqual(peak_hp_rpm, 8000, delta=100)

    def test_empty_points(self):
        """Empty power points should return empty result."""
        calc = PowerTorqueCalculator([])
        result = calc.compute_curves()
        self.assertEqual(len(result['rpm_values']), 0)

    def test_multi_turbo(self):
        """Multiple turbos should add their boost contributions."""
        twin_turbo = [
            {'max_boost': 0.8, 'reference_rpm': 3000, 'gamma': 2.0, 'wastegate': 0.8},
            {'max_boost': 0.7, 'reference_rpm': 4000, 'gamma': 2.0, 'wastegate': 0.7},
        ]
        calc = PowerTorqueCalculator(self.power_points, twin_turbo)
        boost = calc.boost_at_rpm(5000)
        # Both turbos at full boost: 0.8 + 0.7 = 1.5
        self.assertAlmostEqual(boost, 1.5, places=3)


class TestSetupManager(unittest.TestCase):
    """Test setup manager."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.temp_dir, 'data')
        os.makedirs(self.data_dir)

        # Create a minimal setup.ini
        setup_content = (
            "[PRESSURE_LF]\n"
            "TAB=TYRES\n"
            "NAME=Pressure LF\n"
            "MIN=20\n"
            "MAX=40\n"
            "STEP=1\n"
            "HELP=HELP_LF_PRESSURE\n"
            "\n"
            "[PRESSURE_RF]\n"
            "TAB=TYRES\n"
            "NAME=Pressure RF\n"
            "MIN=20\n"
            "MAX=40\n"
            "STEP=1\n"
            "HELP=HELP_RF_PRESSURE\n"
            "\n"
            "[FUEL]\n"
            "TAB=GENERIC\n"
            "NAME=Fuel\n"
            "MIN=10\n"
            "MAX=61\n"
            "STEP=1\n"
            "HELP=HELP_FUEL\n"
        )
        with open(os.path.join(self.data_dir, 'setup.ini'), 'w') as f:
            f.write(setup_content)

        self.manager = SetupManager(self.data_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_has_setup_ini(self):
        """Should detect setup.ini."""
        self.assertTrue(self.manager.has_setup_ini())

    def test_no_setup_ini(self):
        """Should handle missing setup.ini."""
        empty_dir = os.path.join(self.temp_dir, 'empty')
        os.makedirs(empty_dir)
        mgr = SetupManager(empty_dir)
        self.assertFalse(mgr.has_setup_ini())
        self.assertEqual(len(mgr.get_parameters()), 0)

    def test_parameters_parsed(self):
        """Should parse parameters from setup.ini."""
        params = self.manager.get_parameters()
        self.assertEqual(len(params), 3)

    def test_get_tabs(self):
        """Should return correct tab names."""
        tabs = self.manager.get_tabs()
        self.assertIn('TYRES', tabs)
        self.assertIn('GENERIC', tabs)

    def test_get_parameters_by_tab(self):
        """Should filter parameters by tab."""
        tyre_params = self.manager.get_parameters_by_tab('TYRES')
        self.assertEqual(len(tyre_params), 2)
        generic_params = self.manager.get_parameters_by_tab('GENERIC')
        self.assertEqual(len(generic_params), 1)

    def test_parameter_values(self):
        """Should parse min/max/step correctly."""
        params = self.manager.get_parameters_by_tab('TYRES')
        p = params[0]
        self.assertEqual(p['min'], 20.0)
        self.assertEqual(p['max'], 40.0)
        self.assertEqual(p['step'], 1.0)

    def test_save_preset(self):
        """Should save a preset file."""
        values = {'PRESSURE_LF': 28.0, 'PRESSURE_RF': 28.0, 'FUEL': 40.0}
        result = self.manager.save_preset('monza', values)
        self.assertTrue(result)
        # File should exist
        path = os.path.join(self.temp_dir, 'setups', 'monza.json')
        self.assertTrue(os.path.exists(path))

    def test_load_preset(self):
        """Should load a saved preset."""
        values = {'PRESSURE_LF': 28.0, 'FUEL': 40.0}
        self.manager.save_preset('spa', values)
        loaded = self.manager.load_preset('spa')
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded['PRESSURE_LF'], 28.0)
        self.assertEqual(loaded['FUEL'], 40.0)

    def test_load_nonexistent_preset(self):
        """Should return None for missing preset."""
        result = self.manager.load_preset('nonexistent')
        self.assertIsNone(result)

    def test_list_presets(self):
        """Should list saved presets."""
        self.manager.save_preset('monza', {'FUEL': 40})
        self.manager.save_preset('spa', {'FUEL': 50})
        presets = self.manager.list_presets()
        self.assertIn('monza', presets)
        self.assertIn('spa', presets)
        self.assertEqual(len(presets), 2)

    def test_delete_preset(self):
        """Should delete a preset."""
        self.manager.save_preset('imola', {'FUEL': 30})
        self.assertTrue(self.manager.delete_preset('imola'))
        self.assertNotIn('imola', self.manager.list_presets())

    def test_delete_nonexistent_preset(self):
        """Should return False for missing preset."""
        self.assertFalse(self.manager.delete_preset('nonexistent'))


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
