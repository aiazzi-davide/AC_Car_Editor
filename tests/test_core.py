"""
Test suite for AC Car Editor core modules
"""

import unittest
import os
import sys
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.ini_parser import IniParser
from core.lut_parser import LUTCurve
from core.car_file_manager import CarFileManager
from core.component_library import ComponentLibrary


class TestIniParser(unittest.TestCase):
    """Test INI parser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = 'tests/test_data/test_car/data/engine.ini'
        
    def test_load_ini(self):
        """Test loading INI file"""
        parser = IniParser(self.test_file)
        self.assertTrue(parser.has_section('ENGINE_DATA'))
        
    def test_get_value(self):
        """Test getting values from INI"""
        parser = IniParser(self.test_file)
        minimum = parser.get_value('ENGINE_DATA', 'MINIMUM')
        self.assertEqual(minimum, '1000')
        
    def test_get_section(self):
        """Test getting entire section"""
        parser = IniParser(self.test_file)
        section = parser.get_section('ENGINE_DATA')
        self.assertIn('MINIMUM', section)
        self.assertIn('MAXIMUM', section)
    
    def test_inline_comments(self):
        """Test parsing values with inline comments"""
        import tempfile
        # Create a temporary INI file with inline comments
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write('[ENGINE_DATA]\n')
            f.write('MINIMUM=1000\t\t; minimum RPM\n')
            f.write('MAXIMUM=8200\t\t\t\t\t; maximum RPM\n')
            f.write('LIMITER=8500\t\t; engine rev limiter\n')
            temp_file = f.name
        
        try:
            parser = IniParser(temp_file)
            self.assertEqual(parser.get_value('ENGINE_DATA', 'MINIMUM'), '1000')
            self.assertEqual(parser.get_value('ENGINE_DATA', 'MAXIMUM'), '8200')
            self.assertEqual(parser.get_value('ENGINE_DATA', 'LIMITER'), '8500')
        finally:
            os.unlink(temp_file)

    def test_set_value_no_dirty_on_format_difference(self):
        """set_value must NOT mark dirty when only float formatting differs (e.g. '0.15' vs '0.1500')."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write('[ENGINE_DATA]\nINERTIA=0.15\nMINIMUM=800\n')
            temp_file = f.name
        try:
            parser = IniParser(temp_file)
            self.assertFalse(parser._dirty)
            # Re-write same values with different string format
            parser.set_value('ENGINE_DATA', 'INERTIA', '0.1500')
            parser.set_value('ENGINE_DATA', 'MINIMUM', '800')
            self.assertFalse(parser._dirty, "Should NOT be dirty — values are numerically identical")
            # Now change a value — must become dirty
            parser.set_value('ENGINE_DATA', 'INERTIA', '0.1600')
            self.assertTrue(parser._dirty, "Should be dirty after a real change")
        finally:
            os.unlink(temp_file)
    """Test LUT parser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = 'tests/test_data/test_car/data/power.lut'
        
    def test_load_lut(self):
        """Test loading LUT file"""
        curve = LUTCurve(self.test_file)
        self.assertGreater(len(curve), 0)
        
    def test_get_points(self):
        """Test getting points"""
        curve = LUTCurve(self.test_file)
        points = curve.get_points()
        self.assertEqual(len(points), 9)
        self.assertEqual(points[0], (1000.0, 100.0))
        
    def test_interpolate(self):
        """Test interpolation"""
        curve = LUTCurve(self.test_file)
        # Test exact point
        value = curve.interpolate(3000.0)
        self.assertEqual(value, 200.0)
        
        # Test interpolated point
        value = curve.interpolate(3500.0)
        self.assertGreater(value, 200.0)
        self.assertLess(value, 280.0)
        
    def test_add_point(self):
        """Test adding point"""
        curve = LUTCurve(self.test_file)
        initial_count = len(curve)
        curve.add_point(9000.0, 400.0)
        self.assertEqual(len(curve), initial_count + 1)
        
    def test_save_load(self):
        """Test save and load roundtrip"""
        curve = LUTCurve(self.test_file)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lut') as f:
            temp_file = f.name
        
        try:
            curve.save(temp_file, backup=False)
            
            # Load and compare
            curve2 = LUTCurve(temp_file)
            self.assertEqual(len(curve), len(curve2))
            self.assertEqual(curve.get_points(), curve2.get_points())
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_semicolon_comments(self):
        """Test that LUT parser skips lines starting with ;"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lut') as f:
            f.write("; This is a comment\n")
            f.write("0|0\n")
            f.write("; Another comment\n")
            f.write("100|50\n")
            temp_file = f.name
        try:
            curve = LUTCurve(temp_file)
            self.assertEqual(len(curve), 2)
            self.assertEqual(curve.get_points(), [(0.0, 0.0), (100.0, 50.0)])
        finally:
            os.remove(temp_file)

    def test_inline_semicolon_comments(self):
        """Test that LUT parser strips inline ; comments from values"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lut') as f:
            f.write("0|0\n")
            f.write("1000|85     ; This is an inline comment\n")
            f.write("2000|120\n")
            temp_file = f.name
        try:
            curve = LUTCurve(temp_file)
            self.assertEqual(len(curve), 3)
            self.assertEqual(curve.get_points()[1], (1000.0, 85.0))
        finally:
            os.remove(temp_file)

    def test_inline_hash_comments(self):
        """Test that LUT parser strips inline # comments from values"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lut') as f:
            f.write("0|10 # start point\n")
            f.write("500|75\n")
            temp_file = f.name
        try:
            curve = LUTCurve(temp_file)
            self.assertEqual(len(curve), 2)
            self.assertEqual(curve.get_points()[0], (0.0, 10.0))
        finally:
            os.remove(temp_file)

    def test_mixed_comments(self):
        """Test LUT parser with mixed comment styles (like real AC files)"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lut') as f:
            f.write("; Power curve\n")
            f.write("# RPM|HP\n")
            f.write("0|0\n")
            f.write("1500|105     ; low torque\n")
            f.write("3500|168     ; peak torque\n")
            f.write("6500|85      ; engine fading\n")
            temp_file = f.name
        try:
            curve = LUTCurve(temp_file)
            self.assertEqual(len(curve), 4)
            self.assertEqual(curve.get_points()[0], (0.0, 0.0))
            self.assertEqual(curve.get_points()[1], (1500.0, 105.0))
            self.assertEqual(curve.get_points()[2], (3500.0, 168.0))
            self.assertEqual(curve.get_points()[3], (6500.0, 85.0))
        finally:
            os.remove(temp_file)

    def test_load_real_power_lut_with_comments(self):
        """Test loading the example power.lut that has inline ; comments"""
        example_file = os.path.join(os.path.dirname(__file__), '..', 'examples', 'data', 'power.lut')
        if os.path.exists(example_file):
            curve = LUTCurve(example_file)
            self.assertGreater(len(curve), 0)
            # All points should have valid float values (comments stripped)
            for x, y in curve.get_points():
                self.assertIsInstance(x, float)
                self.assertIsInstance(y, float)


class TestCarFileManager(unittest.TestCase):
    """Test car file manager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_cars_path = 'tests/test_data'
        self.manager = CarFileManager(self.test_cars_path)
        
    def test_get_car_list(self):
        """Test getting car list"""
        cars = self.manager.get_car_list()
        self.assertIn('test_car', cars)
        
    def test_get_car_info(self):
        """Test getting car info"""
        info = self.manager.get_car_info('test_car')
        self.assertEqual(info['name'], 'test_car')
        self.assertTrue(info['has_data_folder'])
        self.assertEqual(info['display_name'], 'Test Car')
        self.assertEqual(info['brand'], 'Test Brand')
        
    def test_has_data_folder(self):
        """Test checking for data folder"""
        self.assertTrue(self.manager.has_data_folder('test_car'))


class TestComponentLibrary(unittest.TestCase):
    """Test component library"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Use temp file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.library_path = os.path.join(self.temp_dir, 'test_library.json')
        self.library = ComponentLibrary(self.library_path)
        
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir)
        
    def test_create_default_library(self):
        """Test default library creation"""
        self.assertIn('engine', self.library.components)
        self.assertGreater(len(self.library.components['engine']), 0)
        
    def test_add_component(self):
        """Test adding component"""
        component = {
            'id': 'test_engine',
            'name': 'Test Engine',
            'description': 'Test',
            'tags': ['test'],
            'data': {}
        }
        result = self.library.add_component('engine', component)
        self.assertTrue(result)
        
        # Verify it was added
        found = self.library.get_component('engine', 'test_engine')
        self.assertIsNotNone(found)
        self.assertEqual(found['name'], 'Test Engine')
        
    def test_get_components(self):
        """Test getting components by type"""
        components = self.library.get_components('engine')
        self.assertIsInstance(components, list)
        self.assertGreater(len(components), 0)
        
    def test_search_components(self):
        """Test searching components"""
        # Search for 'street' which should match multiple engine components
        results = self.library.search_components('engine', 'street')
        self.assertGreater(len(results), 0)
        
        # Search for 'turbo' tag
        results = self.library.search_components('engine', 'turbo')
        self.assertGreater(len(results), 0)
    
    def test_export_import_component(self):
        """Test exporting and importing a single component"""
        import tempfile
        
        # Export a component
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            export_path = f.name
        
        try:
            # Export an engine component
            result = self.library.export_component('engine', 'engine_na_street', export_path)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(export_path))
            
            # Create a new library and import the component
            temp_lib_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            temp_lib_path = temp_lib_file.name
            temp_lib_file.close()
            new_library = ComponentLibrary(temp_lib_path)
            
            # Delete the existing engine components first to avoid conflicts
            new_library.components['engine'] = []
            
            result = new_library.import_component(export_path)
            self.assertTrue(result)
            
            # Verify the component was imported
            imported = new_library.get_component('engine', 'engine_na_street')
            self.assertIsNotNone(imported)
            self.assertEqual(imported['name'], 'Street NA Engine')
            
            # Test overwrite functionality
            result = new_library.import_component(export_path, overwrite=True)
            self.assertTrue(result)
            
            # Cleanup
            os.unlink(temp_lib_path)
        finally:
            if os.path.exists(export_path):
                os.unlink(export_path)
    
    def test_filter_by_tags(self):
        """Test filtering components by tags"""
        # Filter engine components by 'turbo' tag
        results = self.library.filter_by_tags('engine', ['turbo'])
        self.assertGreater(len(results), 0)
        
        # Verify all results have the turbo tag
        for component in results:
            self.assertIn('turbo', component.get('tags', []))
        
        # Filter suspension by 'race' tag
        results = self.library.filter_by_tags('suspension', ['race'])
        self.assertGreater(len(results), 0)


class TestRestoreBakFiles(unittest.TestCase):
    """Test restore_bak_files method on CarFileManager"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.data_path = os.path.join(self.temp_dir, 'data')
        os.makedirs(self.data_path)
        self.manager = CarFileManager(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def _write(self, name, content):
        path = os.path.join(self.data_path, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def test_restore_single_bak(self):
        """Restoring a .bak file overwrites the original with the backup content."""
        self._write('engine.ini', 'modified content')
        self._write('engine.ini.bak', 'original content')

        count = self.manager.restore_bak_files(self.data_path)

        self.assertEqual(count, 1)
        with open(os.path.join(self.data_path, 'engine.ini'), encoding='utf-8') as f:
            self.assertEqual(f.read(), 'original content')

    def test_restore_multiple_bak(self):
        """All .bak files in the folder are restored."""
        self._write('engine.ini', 'new engine')
        self._write('engine.ini.bak', 'old engine')
        self._write('suspensions.ini', 'new susp')
        self._write('suspensions.ini.bak', 'old susp')

        count = self.manager.restore_bak_files(self.data_path)

        self.assertEqual(count, 2)

    def test_restore_no_bak_returns_zero(self):
        """Returns 0 when no .bak files exist."""
        self._write('engine.ini', 'some content')

        count = self.manager.restore_bak_files(self.data_path)

        self.assertEqual(count, 0)

    def test_restore_nonexistent_path_returns_zero(self):
        """Returns 0 gracefully when data path does not exist."""
        count = self.manager.restore_bak_files('/nonexistent/path')
        self.assertEqual(count, 0)

    def test_bak_file_removed_after_restore(self):
        """The .bak file is removed after restoration."""
        self._write('engine.ini', 'modified')
        self._write('engine.ini.bak', 'backup')

        self.manager.restore_bak_files(self.data_path)

        self.assertFalse(os.path.exists(os.path.join(self.data_path, 'engine.ini.bak')))


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
