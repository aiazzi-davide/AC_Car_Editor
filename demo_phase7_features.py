"""
Demo script for UI Editor and Stage Tuning features
Run this to see how the new features work without launching the GUI
"""

import sys
import os
import tempfile
import shutil
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.ui_manager import UIManager
from core.stage_tuner import StageTuner


def demo_ui_editor():
    """Demonstrate UI Editor functionality"""
    print("\n" + "="*60)
    print("UI EDITOR DEMO")
    print("="*60)
    
    # Create a temporary car folder
    test_dir = tempfile.mkdtemp()
    car_path = os.path.join(test_dir, 'test_car')
    ui_path = os.path.join(car_path, 'ui')
    os.makedirs(ui_path)
    
    # Create sample ui_car.json
    sample_data = {
        'name': 'Original Car Name',
        'brand': 'Generic Brand',
        'class': 'street',
        'country': 'Italy',
        'description': 'Original description',
        'tags': ['street', 'manual'],
        'specs': {
            'bhp': '150 bhp',
            'torque': '200 Nm',
        },
        'year': 2010
    }
    
    with open(os.path.join(ui_path, 'ui_car.json'), 'w') as f:
        json.dump(sample_data, f)
    
    print("\n1. Original ui_car.json:")
    print(json.dumps(sample_data, indent=2))
    
    # Load and modify using UIManager
    manager = UIManager(car_path)
    print("\n2. Loading with UIManager...")
    print(f"   Current name: {manager.get_name()}")
    print(f"   Current brand: {manager.get_brand()}")
    
    # Make modifications
    print("\n3. Modifying metadata...")
    manager.set_name('Modified Car Name - Stage 1')
    manager.set_brand('Tuning Shop Inc.')
    manager.set_tags(['street', 'manual', 'stage1', 'tuned'])
    manager.set_specs({
        'bhp': '180 bhp',
        'torque': '240 Nm',
        'weight': '1300 kg'
    })
    
    print(f"   New name: {manager.get_name()}")
    print(f"   New brand: {manager.get_brand()}")
    print(f"   New tags: {manager.get_tags()}")
    
    # Save
    manager.save(backup=True)
    print("\n4. Saved to ui_car.json (backup created)")
    
    # Verify
    with open(os.path.join(ui_path, 'ui_car.json'), 'r') as f:
        saved_data = json.load(f)
    print("\n5. Saved ui_car.json:")
    print(json.dumps(saved_data, indent=2))
    
    # Cleanup
    shutil.rmtree(test_dir)
    print("\n✓ UI Editor demo completed!")


def demo_stage_tuning():
    """Demonstrate Stage Tuning functionality"""
    print("\n" + "="*60)
    print("STAGE TUNING DEMO")
    print("="*60)
    
    # Test NA car
    print("\n--- NA (Naturally Aspirated) Car ---")
    test_dir = tempfile.mkdtemp()
    data_path = os.path.join(test_dir, 'data')
    os.makedirs(data_path)
    
    # Create engine.ini for NA car
    with open(os.path.join(data_path, 'engine.ini'), 'w') as f:
        f.write("[ENGINE_DATA]\n")
        f.write("MINIMUM=1000\n")
        f.write("MAXIMUM=7000\n")
        f.write("LIMITER=7500\n")
        f.write("INERTIA=0.20\n")
    
    # Create power.lut
    with open(os.path.join(data_path, 'power.lut'), 'w') as f:
        f.write("1000|100\n")
        f.write("3000|200\n")
        f.write("5000|300\n")
        f.write("7000|280\n")
    
    # Create supporting files
    with open(os.path.join(data_path, 'car.ini'), 'w') as f:
        f.write("[BASIC]\nTOTALMASS=1400\n")
    
    with open(os.path.join(data_path, 'aero.ini'), 'w') as f:
        f.write("[HEADER]\nCD=0.35\n")
    
    tuner = StageTuner(data_path)
    print(f"\n1. Engine type: {'Turbo' if tuner.is_turbo else 'NA'}")
    print(f"   Current stage: {tuner.get_current_stage()}")
    
    # Show stage descriptions
    for stage in [1, 2, 3]:
        desc = tuner.get_stage_description(stage)
        print(f"\n{desc['title']}:")
        print(desc['description'])
    
    # Apply Stage 1
    print("\n2. Applying Stage 1...")
    tuner.apply_stage_1()
    print("   ✓ Stage 1 applied (power curve increased by 8%)")
    
    # Reload and check
    tuner = StageTuner(data_path)
    print(f"   Current stage: {tuner.get_current_stage()}")
    
    shutil.rmtree(test_dir)
    
    # Test Turbo car
    print("\n--- Turbocharged Car ---")
    test_dir = tempfile.mkdtemp()
    data_path = os.path.join(test_dir, 'data')
    os.makedirs(data_path)
    
    # Create engine.ini for turbo car
    with open(os.path.join(data_path, 'engine.ini'), 'w') as f:
        f.write("[ENGINE_DATA]\n")
        f.write("MINIMUM=1000\n")
        f.write("MAXIMUM=7000\n")
        f.write("LIMITER=7500\n")
        f.write("INERTIA=0.20\n")
        f.write("\n[TURBO_0]\n")
        f.write("MAX_BOOST=0.50\n")
        f.write("WASTEGATE=0.60\n")
    
    with open(os.path.join(data_path, 'power.lut'), 'w') as f:
        f.write("1000|100\n")
        f.write("3000|200\n")
        f.write("5000|300\n")
        f.write("7000|280\n")
    
    with open(os.path.join(data_path, 'car.ini'), 'w') as f:
        f.write("[BASIC]\nTOTALMASS=1400\n")
    
    with open(os.path.join(data_path, 'aero.ini'), 'w') as f:
        f.write("[HEADER]\nCD=0.35\n")
    
    tuner = StageTuner(data_path)
    print(f"\n1. Engine type: {'Turbo' if tuner.is_turbo else 'NA'}")
    print(f"   Current stage: {tuner.get_current_stage()}")
    print(f"   Initial boost: 0.50 bar")
    
    # Show stage descriptions
    for stage in [1, 2, 3]:
        desc = tuner.get_stage_description(stage)
        print(f"\n{desc['title']}:")
        print(desc['description'])
    
    # Apply Stage 1
    print("\n2. Applying Stage 1...")
    tuner.apply_stage_1()
    
    from core.ini_parser import IniParser
    engine = IniParser(os.path.join(data_path, 'engine.ini'))
    new_boost = float(engine.get_value('TURBO_0', 'MAX_BOOST'))
    print(f"   ✓ Stage 1 applied")
    print(f"   New boost: {new_boost:.3f} bar (15% increase)")
    
    # Apply Stage 2
    print("\n3. Applying Stage 2...")
    tuner.apply_stage_2()
    
    engine = IniParser(os.path.join(data_path, 'engine.ini'))
    new_boost = float(engine.get_value('TURBO_0', 'MAX_BOOST'))
    print(f"   ✓ Stage 2 applied")
    print(f"   New boost: {new_boost:.3f} bar (30% increase from original)")
    
    shutil.rmtree(test_dir)
    print("\n✓ Stage Tuning demo completed!")


if __name__ == '__main__':
    print("\nAC Car Editor - Phase 7 Features Demo")
    print("======================================")
    
    demo_ui_editor()
    demo_stage_tuning()
    
    print("\n" + "="*60)
    print("Demo completed successfully!")
    print("="*60)
