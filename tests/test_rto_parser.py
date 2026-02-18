"""
Tests for RTO parser
"""

import unittest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.rto_parser import RTOParser


class TestRTOParser(unittest.TestCase):
    """Test RTO file parser"""
    
    def setUp(self):
        """Create temporary directory for test files"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.rto')
    
    def tearDown(self):
        """Clean up temporary directory"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_load_simple_rto(self):
        """Test loading a simple .rto file"""
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write("4.90|4.90\n")
            f.write("4.63|4.63\n")
            f.write("4.08|4.08\n")
        
        parser = RTOParser(self.test_file)
        ratios = parser.get_ratios()
        
        self.assertEqual(len(ratios), 3)
        self.assertAlmostEqual(ratios[0], 4.90, places=2)
        self.assertAlmostEqual(ratios[1], 4.63, places=2)
        self.assertAlmostEqual(ratios[2], 4.08, places=2)
    
    def test_load_with_comments(self):
        """Test loading .rto file with comments"""
        with open(self.test_file, 'w') as f:
            f.write("; Comment line\n")
            f.write("4.90|4.90\n")
            f.write("# Another comment\n")
            f.write("4.63|4.63\n")
        
        parser = RTOParser(self.test_file)
        ratios = parser.get_ratios()
        
        self.assertEqual(len(ratios), 2)
        self.assertAlmostEqual(ratios[0], 4.90, places=2)
        self.assertAlmostEqual(ratios[1], 4.63, places=2)
    
    def test_load_with_empty_lines(self):
        """Test loading .rto file with empty lines"""
        with open(self.test_file, 'w') as f:
            f.write("4.90|4.90\n")
            f.write("\n")
            f.write("4.63|4.63\n")
            f.write("\n\n")
            f.write("4.08|4.08\n")
        
        parser = RTOParser(self.test_file)
        ratios = parser.get_ratios()
        
        self.assertEqual(len(ratios), 3)
    
    def test_save_rto(self):
        """Test saving .rto file"""
        parser = RTOParser(self.test_file)
        parser.add_ratio(4.90)
        parser.add_ratio(4.63)
        parser.add_ratio(4.08)
        parser.save(backup=False)
        
        # Reload and verify
        parser2 = RTOParser(self.test_file)
        ratios = parser2.get_ratios()
        
        self.assertEqual(len(ratios), 3)
        self.assertAlmostEqual(ratios[0], 4.90, places=2)
        self.assertAlmostEqual(ratios[1], 4.63, places=2)
        self.assertAlmostEqual(ratios[2], 4.08, places=2)
    
    def test_save_with_backup(self):
        """Test that backup is created"""
        # Create initial file
        with open(self.test_file, 'w') as f:
            f.write("3.50|3.50\n")
        
        parser = RTOParser(self.test_file)
        parser.add_ratio(4.90)
        parser.save(backup=True)
        
        # Check backup exists
        backup_path = self.test_file + '.bak'
        self.assertTrue(os.path.exists(backup_path))
        
        # Verify backup contains original content
        with open(backup_path, 'r') as f:
            content = f.read()
            self.assertIn('3.50', content)
    
    def test_add_ratio(self):
        """Test adding a ratio"""
        parser = RTOParser(self.test_file)
        parser.add_ratio(4.90)
        parser.add_ratio(4.63)
        
        ratios = parser.get_ratios()
        self.assertEqual(len(ratios), 2)
        self.assertAlmostEqual(ratios[0], 4.90, places=2)
        self.assertAlmostEqual(ratios[1], 4.63, places=2)
    
    def test_remove_ratio(self):
        """Test removing a ratio"""
        parser = RTOParser(self.test_file)
        parser.add_ratio(4.90)
        parser.add_ratio(4.63)
        parser.add_ratio(4.08)
        
        parser.remove_ratio(1)  # Remove middle one
        
        ratios = parser.get_ratios()
        self.assertEqual(len(ratios), 2)
        self.assertAlmostEqual(ratios[0], 4.90, places=2)
        self.assertAlmostEqual(ratios[1], 4.08, places=2)
    
    def test_update_ratio(self):
        """Test updating a ratio"""
        parser = RTOParser(self.test_file)
        parser.add_ratio(4.90)
        parser.add_ratio(4.63)
        
        parser.update_ratio(1, 5.00)
        
        ratios = parser.get_ratios()
        self.assertAlmostEqual(ratios[1], 5.00, places=2)
    
    def test_sort_ratios(self):
        """Test sorting ratios"""
        parser = RTOParser(self.test_file)
        parser.add_ratio(4.08)
        parser.add_ratio(4.90)
        parser.add_ratio(4.63)
        
        parser.sort_ratios(reverse=True)  # Descending
        
        ratios = parser.get_ratios()
        self.assertAlmostEqual(ratios[0], 4.90, places=2)
        self.assertAlmostEqual(ratios[1], 4.63, places=2)
        self.assertAlmostEqual(ratios[2], 4.08, places=2)
    
    def test_nonexistent_file(self):
        """Test loading nonexistent file"""
        parser = RTOParser(self.test_file)
        ratios = parser.get_ratios()
        self.assertEqual(len(ratios), 0)
    
    def test_set_ratios(self):
        """Test setting ratios list"""
        parser = RTOParser(self.test_file)
        new_ratios = [4.90, 4.63, 4.08]
        parser.set_ratios(new_ratios)
        
        ratios = parser.get_ratios()
        self.assertEqual(len(ratios), 3)
        self.assertAlmostEqual(ratios[0], 4.90, places=2)


if __name__ == '__main__':
    unittest.main()
