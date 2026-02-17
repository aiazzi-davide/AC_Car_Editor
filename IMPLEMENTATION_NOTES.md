# AC Car Editor - Implementation Notes

This document tracks the implemented features and provides guidance for future development.

## Current Implementation Status (Phase 6 Complete)

### Core Components (src/core/)

#### IniParser (ini_parser.py)
**Status**: Fully implemented and tested
**Functions**:
- `__init__(file_path)` - Initialize parser with file path
- `load()` - Load INI file from disk
- `save(backup=True)` - Save INI file with optional backup creation
- `get_value(section, key, default)` - Get value from INI file
- `set_value(section, key, value)` - Set value in INI file
- `get_section(section)` - Get all key-value pairs from section
- `get_sections()` - Get all section names
- `has_section(section)` - Check if section exists

**Key Features**:
- Case-sensitive key handling (`optionxform = str`)
- Automatic whitespace stripping
- Inline comment support (`;` and `#`)
- Backup file creation with `.bak` extension
- **Robust error handling**: Gracefully handles malformed INI files with unparseable lines (configparser.ParsingError)
- **Non-crashing behavior**: Application continues to run even if some INI files have parsing errors

#### LUTCurve (lut_parser.py)
**Status**: Fully implemented and tested
**Functions**:
- `__init__(file_path)` - Initialize LUT curve with optional file path
- `load()` - Load LUT file (X|Y format)
- `save(file_path, backup=True)` - Save LUT file with optional backup
- `add_point(x, y)` - Add a point to the curve
- `remove_point(index)` - Remove a point by index
- `update_point(index, x, y)` - Update a point's coordinates
- `sort_points()` - Sort points by X value
- `get_points()` - Get all points as list of tuples
- `interpolate(x)` - Interpolate Y value for given X (linear)
- `clear()` - Clear all points

**Key Features**:
- Parses pipe-delimited format (`X|Y`)
- Ignores comment lines starting with `#`
- Maintains points sorted by X value
- Linear interpolation support

#### CarFileManager (car_file_manager.py)
**Status**: Fully implemented and tested
**Functions**:
- `__init__(cars_path)` - Initialize with AC cars folder path
- `get_car_list()` - Get list of all car folders
- `get_car_path(car_name)` - Get full path to car folder
- `get_car_data_path(car_name)` - Get path to car's data folder
- `has_data_folder(car_name)` - Check if car has unpacked data folder
- `has_data_acd(car_name)` - Check if car has data.acd file
- `get_car_info(car_name)` - Get basic car information (reads ui_car.json)
- `create_backup(car_name, backup_dir)` - Create timestamped backup of car data
- `restore_backup(car_name, backup_path)` - Restore car data from backup
- `get_ini_file_path(car_name, ini_name)` - Get path to specific INI file
- `get_lut_file_path(car_name, lut_name)` - Get path to specific LUT file

**Key Features**:
- Handles AC's directory structure
- Distinguishes between data folder and data.acd
- Timestamped backups (YYYYMMDD_HHMMSS)
- Reads display name from ui_car.json

#### ConfigManager (config.py)
**Status**: Fully implemented
**Functions**:
- `__init__()` - Initialize configuration manager
- `get_ac_path()` - Get AC installation path
- `set_ac_path(path)` - Set AC installation path
- `get_cars_path()` - Get cars folder path
- `get_backup_path()` - Get backup folder path
- `save()` - Save configuration to config.json
- `load()` - Load configuration from config.json

**Key Features**:
- JSON-based configuration storage
- Default path support
- Automatic directory creation

#### ComponentLibrary (component_library.py)
**Status**: Fully implemented and tested
**Functions**:
- `__init__(library_path)` - Initialize component library
- `load()` - Load library from JSON file
- `save()` - Save library to JSON file
- `get_components(component_type)` - Get all components of a type
- `get_component(component_type, component_id)` - Get specific component
- `add_component(component_type, component)` - Add new component
- `update_component(component_type, component_id, component)` - Update component
- `delete_component(component_type, component_id)` - Delete component
- `search_components(component_type, query)` - Search by name/tags

**Key Features**:
- JSON-based storage (src/components/library.json)
- Component types: engine, suspension, differential, drivetrain, aero, tyres
- Tag-based organization
- Default library creation

### GUI Components (src/gui/)

#### MainWindow (main_window.py)
**Status**: Fully implemented
**Functions**:
- `__init__()` - Initialize main window
- `init_ui()` - Set up user interface
- `create_menu_bar()` - Create menu bar with File/Tools/Help menus
- `create_car_list_panel()` - Create left panel with car list
- `create_car_info_panel()` - Create right panel with car info
- `load_cars()` - Load list of cars from AC directory
- `on_car_selected(current, previous)` - Handle car selection
- `set_ac_path()` - Dialog to set AC path
- `create_backup()` - Create backup of selected car
- `edit_car()` - Open car editor dialog
- `open_component_library()` - Placeholder for component library
- `show_about()` - Show about dialog

**Key Features**:
- Splitter layout with resizable panels
- Car list with refresh button
- Car info display (name, brand, data folder status)
- Edit and backup buttons (enabled only for cars with data folder)
- Status bar for feedback

#### CarEditorDialog (car_editor_dialog.py)
**Status**: Phase 6 complete - all major tabs implemented
**Functions**:
- `__init__(car_name, car_data_path, parent)` - Initialize editor dialog
- `init_parsers()` - Initialize all INI parsers (engine, suspension, drivetrain, car, aero)
- `init_ui()` - Set up tabbed interface
- `create_engine_tab()` - Create engine parameters tab
- `create_suspension_tab()` - Create suspension parameters tab
- `create_differential_tab()` - Create differential parameters tab
- `create_weight_tab()` - Create weight and balance tab
- `create_aero_tab()` - Create aerodynamics tab
- `load_data()` - Load all car data into UI fields
- `save_changes()` - Save all modified data to INI files
- `reset_values()` - Reset all fields to original values

**Implemented Tabs**:

1. **Engine Tab** (engine.ini)
   - Minimum RPM (ENGINE_DATA.MINIMUM)
   - Maximum RPM (ENGINE_DATA.MAXIMUM)
   - Limiter RPM (ENGINE_DATA.LIMITER)
   - Max Boost (TURBO_0.MAX_BOOST) - if turbo present
   - Wastegate (TURBO_0.WASTEGATE) - if turbo present

2. **Suspension Tab** (suspensions.ini)
   - Front:
     - Spring Rate (FRONT.SPRING_RATE) - N/m
     - Damper Fast Bump (FRONT.DAMPER_FAST_BUMP) - N/(m/s)
     - Damper Fast Rebound (FRONT.DAMPER_FAST_REBOUND) - N/(m/s)
     - Damper Slow Bump (FRONT.DAMPER_SLOW_BUMP) - N/(m/s)
     - Damper Slow Rebound (FRONT.DAMPER_SLOW_REBOUND) - N/(m/s)
     - Rod Length (FRONT.ROD_LENGTH) - m
   - Rear: (same parameters as front)

3. **Differential Tab** (drivetrain.ini)
   - Traction Type (TRACTION.TYPE) - display only (RWD/FWD/AWD)
   - Differential Type (DIFFERENTIAL.TYPE) - display only (LSD/SPOOL/etc)
   - Power (DIFFERENTIAL.POWER) - 0.0 to 1.0
   - Coast (DIFFERENTIAL.COAST) - 0.0 to 1.0
   - Preload (DIFFERENTIAL.PRELOAD) - Nm

4. **Weight Tab** (car.ini)
   - Total Mass (BASIC.TOTALMASS) - kg
   - Center of Gravity:
     - X (GRAPHICS.CG_LOCATION[0]) - lateral, m
     - Y (GRAPHICS.CG_LOCATION[1]) - vertical, m
     - Z (GRAPHICS.CG_LOCATION[2]) - longitudinal, m

5. **Aerodynamics Tab** (aero.ini)
   - Drag Coefficient (SETTINGS.DRAG_COEFF)
   - Front:
     - Lift Coefficient (FRONT.LIFTCOEFF) - negative = downforce
     - CL Gain (FRONT.CL_GAIN)
   - Rear:
     - Lift Coefficient (REAR.LIFTCOEFF) - negative = downforce
     - CL Gain (REAR.CL_GAIN)

**Key Features**:
- Modal dialog (800x600)
- Tabbed interface for organization
- QSpinBox/QDoubleSpinBox with appropriate units
- Save button creates backups for all modified files
- Reset button restores all original values
- Cancel button discards changes

## Testing Status

### Core Tests (tests/test_core.py)
- ✅ IniParser: 4 tests (load, get_value, get_section, inline_comments)
- ✅ LUTParser: 5 tests (load, get_points, add_point, interpolate, save_load)
- ✅ CarFileManager: 3 tests (get_car_list, has_data_folder, get_car_info)
- ✅ ComponentLibrary: 4 tests (create_default, get_components, add_component, search_components)

**Total Core Tests**: 16 tests, all passing

### GUI Tests (tests/test_gui.py)
- ✅ Engine: 3 tests (load_engine_data, save_engine_data, load_turbo_data, save_turbo_data, backup_creation)
- ✅ Suspension: 2 tests (load_suspension_data, save_suspension_data)
- ✅ Differential: 2 tests (load_differential_data, save_differential_data)
- ✅ Weight: 2 tests (load_weight_data, save_weight_data)
- ✅ Aerodynamics: 2 tests (load_aero_data, save_aero_data)
- ✅ Error Handling: 1 test (malformed_ini_file)

**Total GUI Tests**: 14 tests, all passing

**Total Tests**: 30 tests, 100% passing

## Test Data Files

Located in `tests/test_data/test_car/data/`:
- ✅ engine.ini - Engine and turbo configuration
- ✅ suspensions.ini - Front and rear suspension settings
- ✅ drivetrain.ini - Traction type and differential settings
- ✅ car.ini - Basic car info, mass, center of gravity
- ✅ aero.ini - Drag and downforce settings
- ✅ power.lut - Power curve (RPM|kW)
- ✅ coast.lut - Coast curve (RPM|Nm)
- ✅ malformed_suspensions.ini - Test file with unparseable lines for error handling

## Implementation Patterns

### Adding a New Tab to CarEditorDialog

Follow this pattern (documented in copilot-instructions.md):

1. **Add parser initialization** in `init_parsers()` (with error handling):
```python
myfile_path = os.path.join(self.car_data_path, 'myfile.ini')
if os.path.exists(myfile_path):
    try:
        self.myfile_ini = IniParser(myfile_path)
    except Exception as e:
        print(f"Failed to load myfile.ini: {e}")
        self.myfile_ini = None
```

2. **Create tab method** `create_mytab_tab()`:
```python
def create_mytab_tab(self):
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    group = QGroupBox("Settings")
    group_layout = QFormLayout()
    
    self.my_spinbox = QDoubleSpinBox()
    self.my_spinbox.setRange(0, 1000)
    self.my_spinbox.setSuffix(" units")
    group_layout.addRow("Label:", self.my_spinbox)
    
    group.setLayout(group_layout)
    layout.addWidget(group)
    layout.addStretch()
    
    return widget
```

3. **Add tab to UI** in `init_ui()`:
```python
self.mytab_tab = self.create_mytab_tab()
self.tabs.addTab(self.mytab_tab, "My Tab")
```

4. **Load data** in `load_data()`:
```python
if self.myfile_ini and self.myfile_ini.has_section('SECTION'):
    value = self.myfile_ini.get_value('SECTION', 'KEY', '0')
    self.my_spinbox.setValue(float(value))
    self.original_values['my_value'] = float(value)
```

5. **Save data** in `save_changes()`:
```python
if self.myfile_ini:
    if self.myfile_ini.has_section('SECTION'):
        self.myfile_ini.set_value('SECTION', 'KEY', str(self.my_spinbox.value()))
    self.myfile_ini.save(backup=True)
```

6. **Reset data** in `reset_values()`:
```python
if 'my_value' in self.original_values:
    self.my_spinbox.setValue(self.original_values['my_value'])
```

### Important Conventions

1. **Always use sys.path.insert** in GUI files:
```python
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.ini_parser import IniParser
```

2. **Always create backups** when saving:
```python
parser.save(backup=True)  # Creates .bak file
```

3. **Always add units to spinboxes**:
```python
spinbox.setSuffix(" RPM")  # or " kg", " N/m", etc.
```

4. **Check section existence** before accessing:
```python
if parser.has_section('SECTION'):
    value = parser.get_value('SECTION', 'KEY', 'default')
```

## Next Steps (Phase 6.5 and Beyond)

### Priority 1: Visual Curve Editor for .lut Files
**Status**: Not yet implemented
**Plan** (from plan.md lines 67-80):
- Create CurveEditor widget with matplotlib/pyqtgraph
- Visualize .lut files graphically (power.lut, coast.lut, etc.)
- Drag-drop point editing on graph
- Add/remove points (click or manual form)
- Zoom and pan functionality
- Grid and axis labels (RPM vs kW, etc.)
- Numerical table view alongside graph
- Smooth curve interpolation (spline)
- Import/export curves
- Preset curves (linear, turbo lag, NA, etc.)
- Integration into Engine tab

**Files to Create**:
- `src/gui/curve_editor_widget.py` - Main curve editor widget
- `src/gui/curve_editor_dialog.py` - Standalone dialog for editing curves

### Priority 2: Component Library GUI Manager
**Status**: Backend complete, GUI not implemented
**Plan**:
- Create ComponentLibraryDialog
- List view with filter by type
- Component details preview
- Add/edit/delete forms
- Apply component to car functionality
- Import/export components

**Files to Create**:
- `src/gui/component_library_dialog.py`

### Priority 3: Tire Settings Tab
**Status**: Not implemented
**Required**:
- Parse tyres.ini
- Display tire compounds
- Edit tire dimensions
- Edit thermal properties

### Priority 4: Advanced Features
- Car comparison (side-by-side)
- Undo/redo system
- Export/import configurations
- Search/filter cars by characteristics

## Known Limitations

1. **No data.acd support**: Only works with unpacked data folders
2. **No encryption handling**: Cannot handle encrypted car data
3. **Read-only fields**: Some fields like traction type and diff type are display-only
4. **No input validation**: Values can be set to unrealistic ranges
5. **No LUT editing in GUI**: LUT files can be parsed but not edited visually yet
6. **No sound editing**: Engine sound modification not supported

## File Locations

```
AC_Car_Editor/
├── main.py                          # Entry point
├── config.json                      # AC path configuration (auto-created)
├── IMPLEMENTATION_NOTES.md          # This file
├── README.md                        # User documentation
├── plan.md                          # Original development plan
├── requirements.txt                 # Python dependencies
├── .github/
│   └── copilot-instructions.md      # AI agent instructions
├── src/
│   ├── core/                        # Core logic (all implemented)
│   │   ├── config.py
│   │   ├── car_file_manager.py
│   │   ├── ini_parser.py
│   │   ├── lut_parser.py
│   │   └── component_library.py
│   ├── gui/                         # GUI components
│   │   ├── main_window.py           # Main window (implemented)
│   │   └── car_editor_dialog.py     # Car editor (Phase 6 complete)
│   └── components/
│       └── library.json             # Component library data (auto-created)
├── tests/
│   ├── test_core.py                 # Core tests (16 tests)
│   ├── test_gui.py                  # GUI tests (14 tests)
│   └── test_data/
│       └── test_car/data/           # Test car data files
└── backups/                         # Car backups (auto-created)
```

## Version History

- **v0.1.0** (Phase 1-5): Initial release with engine tab
- **v0.2.0** (Phase 6): Added suspension, differential, weight, and aerodynamics tabs
- **v0.2.1** (Phase 6 bugfix): Fixed crash when loading malformed INI files

## Contributors Notes

When continuing development:
1. Read this file first to understand what's implemented
2. Check copilot-instructions.md for coding patterns
3. Check plan.md for the overall roadmap
4. Always run tests after making changes: `python -m unittest discover tests -v`
5. Update this file when adding new features
6. Update README.md with user-facing changes

## Summary of Implemented Functions by Module

### src/core/ini_parser.py (IniParser class)
- `__init__`, `load`, `save`, `get_value`, `set_value`, `get_section`, `get_sections`, `has_section`

### src/core/lut_parser.py (LUTCurve class)
- `__init__`, `load`, `save`, `add_point`, `remove_point`, `update_point`, `sort_points`, `get_points`, `interpolate`, `clear`

### src/core/car_file_manager.py (CarFileManager class)
- `__init__`, `get_car_list`, `get_car_path`, `get_car_data_path`, `has_data_folder`, `has_data_acd`, `get_car_info`, `create_backup`, `restore_backup`, `get_ini_file_path`, `get_lut_file_path`

### src/core/config.py (ConfigManager class)
- `__init__`, `get_ac_path`, `set_ac_path`, `get_cars_path`, `get_backup_path`, `save`, `load`

### src/core/component_library.py (ComponentLibrary class)
- `__init__`, `load`, `save`, `get_components`, `get_component`, `add_component`, `update_component`, `delete_component`, `search_components`

### src/gui/main_window.py (MainWindow class)
- `__init__`, `init_ui`, `create_menu_bar`, `create_car_list_panel`, `create_car_info_panel`, `load_cars`, `on_car_selected`, `set_ac_path`, `create_backup`, `edit_car`, `open_component_library`, `show_about`

### src/gui/car_editor_dialog.py (CarEditorDialog class)
- `__init__`, `init_parsers`, `init_ui`, `create_engine_tab`, `create_suspension_tab`, `create_differential_tab`, `create_weight_tab`, `create_aero_tab`, `load_data`, `save_changes`, `reset_values`

**Total**: 63 implemented functions across 7 modules
