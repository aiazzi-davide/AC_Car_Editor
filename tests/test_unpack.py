"""
Test script for data.acd unpacking functionality
"""

import os
import sys

# Add src to path
sys.path.insert(0, 'src')

from core.car_file_manager import CarFileManager

def test_quickbms_detection():
    """Test if quickBMS can be found"""
    print("Testing quickBMS detection...")
    
    mgr = CarFileManager('examples')
    
    quickbms_exe = mgr._find_quickbms_path()
    if quickbms_exe:
        print(f"✓ quickBMS found: {quickbms_exe}")
    else:
        print("✗ quickBMS not found")
    
    quickbms_script = mgr._find_quickbms_script()
    if quickbms_script:
        print(f"✓ quickBMS script found: {quickbms_script}")
    else:
        print("✗ quickBMS script not found")
    
    return quickbms_exe is not None and quickbms_script is not None

def test_car_detection():
    """Test car file detection"""
    print("\nTesting car file detection...")
    
    # Test with examples folder structure
    # The examples folder should have data.acd and data/ subfolder
    
    # Check if we can use examples as a car folder
    if os.path.exists('examples/data.acd'):
        print(f"✓ examples/data.acd exists")
    else:
        print("✗ examples/data.acd not found")
    
    if os.path.exists('examples/data'):
        print(f"✓ examples/data folder exists")
    else:
        print("✗ examples/data folder not found")

def test_delete_function():
    """Test delete_data_acd function"""
    print("\nTesting delete_data_acd function...")
    
    mgr = CarFileManager('test_cars')
    os.makedirs('test_cars/test_car', exist_ok=True)
    
    # Create a dummy data.acd file
    test_acd = 'test_cars/test_car/data.acd'
    with open(test_acd, 'w') as f:
        f.write('dummy')
    
    if os.path.exists(test_acd):
        print(f"✓ Created test data.acd")
    
    # Test deletion
    result = mgr.delete_data_acd('test_car')
    
    if result and not os.path.exists(test_acd):
        print("✓ delete_data_acd works correctly")
    else:
        print("✗ delete_data_acd failed")
    
    # Cleanup
    import shutil
    if os.path.exists('test_cars'):
        shutil.rmtree('test_cars')
        print("✓ Cleaned up test files")

if __name__ == '__main__':
    print("=" * 60)
    print("AC Car Editor - Unpack Functionality Test")
    print("=" * 60)
    
    test_quickbms_detection()
    test_car_detection()
    test_delete_function()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
