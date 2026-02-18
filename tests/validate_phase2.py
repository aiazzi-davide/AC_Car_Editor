"""
Quick validation test for Phase 2 implementation
"""

import os
import sys

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    try:
        sys.path.insert(0, 'src')
        from core.car_file_manager import CarFileManager
        from gui.main_window import MainWindow
        print(f"{GREEN}✓{RESET} All imports successful")
        return True
    except Exception as e:
        print(f"{RED}✗{RESET} Import failed: {e}")
        return False

def test_file_structure():
    """Test if required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        ('tools/quickbms/quickbms.exe', 'quickBMS executable'),
        ('tools/assetto_corsa_acd.bms', 'quickBMS script'),
        ('examples/data.acd', 'Example data.acd file'),
        ('examples/data', 'Example data folder'),
    ]
    
    all_ok = True
    for path, description in required_files:
        if os.path.exists(path):
            print(f"{GREEN}✓{RESET} {description}: {path}")
        else:
            print(f"{RED}✗{RESET} Missing {description}: {path}")
            all_ok = False
    
    return all_ok

def test_manager_methods():
    """Test if CarFileManager has new methods"""
    print("\nTesting CarFileManager methods...")
    
    sys.path.insert(0, 'src')
    from core.car_file_manager import CarFileManager
    
    mgr = CarFileManager('examples')
    
    methods = [
        'unpack_data_acd',
        'delete_data_acd',
        '_find_quickbms_path',
        '_find_quickbms_script',
    ]
    
    all_ok = True
    for method in methods:
        if hasattr(mgr, method):
            print(f"{GREEN}✓{RESET} Method exists: {method}")
        else:
            print(f"{RED}✗{RESET} Missing method: {method}")
            all_ok = False
    
    return all_ok

def test_quickbms_detection():
    """Test if quickBMS can be found"""
    print("\nTesting quickBMS detection...")
    
    sys.path.insert(0, 'src')
    from core.car_file_manager import CarFileManager
    
    mgr = CarFileManager('examples')
    
    quickbms_exe = mgr._find_quickbms_path()
    quickbms_script = mgr._find_quickbms_script()
    
    if quickbms_exe:
        print(f"{GREEN}✓{RESET} quickBMS executable found: {quickbms_exe}")
    else:
        print(f"{RED}✗{RESET} quickBMS executable not found")
    
    if quickbms_script:
        print(f"{GREEN}✓{RESET} quickBMS script found: {quickbms_script}")
    else:
        print(f"{RED}✗{RESET} quickBMS script not found")
    
    return quickbms_exe is not None and quickbms_script is not None

def main():
    print("=" * 70)
    print(f"{YELLOW}AC Car Editor - Phase 2 Implementation Validation{RESET}")
    print("=" * 70)
    print()
    
    tests = [
        test_imports,
        test_file_structure,
        test_manager_methods,
        test_quickbms_detection,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"{RED}✗{RESET} Test failed with exception: {e}")
            results.append(False)
        print()
    
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{GREEN}All tests passed! ({passed}/{total}){RESET}")
        print(f"\n{GREEN}✓ Phase 2 implementation complete!{RESET}")
    else:
        print(f"{YELLOW}Some tests failed: {passed}/{total} passed{RESET}")
    
    print("=" * 70)
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
