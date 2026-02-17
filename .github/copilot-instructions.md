# AC Car Editor - AI Coding Agent Instructions

## Project Overview

Desktop PyQt5 application for modifying Assetto Corsa racing simulator car configurations. Parses and edits INI files (engine.ini, suspensions.ini) and LUT lookup tables (power curves, coast curves) in the game's data folders.

**Key constraint**: Only works with unpacked `data/` folders, not encrypted `data.acd` files yet.

## Architecture

### Three-Layer Structure

- **Core layer** (`src/core/`): File parsers, managers, configuration
- **GUI layer** (`src/gui/`): PyQt5 windows and dialogs
- **Entry point**: `main.py` bootstraps the app and configures sys.path

### Critical Components

**IniParser** (`src/core/ini_parser.py`)

- Uses configparser with `optionxform = str` to preserve case sensitivity (AC is case-sensitive)
- Always supports `backup=True` parameter in `save()` to create `.bak` files
- Strips whitespace from values automatically

**LUTCurve** (`src/core/lut_parser.py`)

- Parses AC's `X|Y` format (e.g., `1000|150.5` for RPM|kW curves)
- Maintains points as list of tuples: `List[Tuple[float, float]]`
- Ignores comment lines starting with `#`

**CarFileManager** (`src/core/car_file_manager.py`)

- Manages navigation of AC's `content/cars/[car_name]/data/` structure
- Key distinction: `has_data_folder()` vs `has_data_acd()` - only former is editable
- Handles backup operations with timestamps

**ConfigManager** (`src/core/config.py`)

- Stores AC path in `config.json` at project root
- Default path: `C:\Program Files (x86)\Steam\steamapps\common\assettocorsa`
- Cars always at `{ac_path}/content/cars/`

**ComponentLibrary** (`src/core/component_library.py`)

- JSON-based storage for reusable component configurations
- Schema: `{id, name, description, tags, data}` where `data` contains INI key-value pairs
- Full GUI manager implemented (`src/gui/component_library_dialog.py`)
- Component import functionality integrated into CarEditorDialog tabs

**ComponentSelectorDialog** (`src/gui/component_selector_dialog.py`)

- Dialog for selecting and applying components from library to cars
- Filters components by type (engine, suspension, differential, aero)
- Preview component details before applying
- Integrated via "Import from Library" buttons in CarEditorDialog tabs

## Critical Patterns

### Path Management Hack

Every GUI file uses this pattern to import from `src/`:

```python
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.ini_parser import IniParser
```

**Always replicate this in new GUI modules** - relative imports don't work due to PyQt5 execution model.

### Editor Dialog Pattern (CarEditorDialog)

1. Accept `car_name` and `car_data_path` in `__init__`
2. Store `original_values` dict for reset functionality
3. Initialize parsers in `init_parsers()` method
4. Create tab structure with dedicated `create_*_tab()` methods
5. Load data into widgets in `load_data()`
6. Save via `save_changes()` with **automatic backup** before writing
7. Provide `reset_values()` to restore from `original_values`

**Example spinbox setup** (always include units in suffix):

```python
self.limiter_rpm = QSpinBox()
self.limiter_rpm.setRange(0, 20000)
self.limiter_rpm.setSuffix(" RPM")  # User-visible unit label
```

### Backup Philosophy

**Never modify car files without backup.** Two approaches:

1. Parser-level: `parser.save(backup=True)` creates `.bak` alongside original
2. Manager-level: `CarFileManager.create_backup()` creates timestamped copies in `backups/` folder

Both should be used - parser backups for immediate undo, manager backups for long-term preservation.

### Component Import Pattern

Components from the library can be applied to cars via "Import from Library" buttons in each tab:

1. Button opens `ComponentSelectorDialog` filtered by component type
2. User selects component from list and previews details
3. On apply, corresponding `apply_*_component()` method maps component data to UI fields
4. Component data keys (e.g., `MINIMUM`, `TURBO_MAX_BOOST`) match INI parameter names
5. Only fields present in component data are updated - missing fields remain unchanged
6. Confirmation dialog shows which fields were updated

**Example implementation** (see `car_editor_dialog.py`):

```python
def import_engine_component(self):
    """Import engine component from library"""
    dialog = ComponentSelectorDialog('engine', self)
    if dialog.exec_() == QDialog.Accepted:
        component = dialog.get_selected_component()
        if component:
            self.apply_engine_component(component)

def apply_engine_component(self, component):
    """Apply engine component data to UI fields"""
    data = component.get('data', {})
    if 'MINIMUM' in data:
        self.minimum_rpm.setValue(int(data['MINIMUM']))
    # ... apply other fields
```

## File Format Specifics

### INI Files Structure

```ini
[SECTION_NAME]
KEY=value  ; inline comments supported
KEY2=123
```

- Sections like `[ENGINE_DATA]`, `[TURBO_0]`, `[SUSPENSION_FRONT]`
- Keys are case-sensitive: `MINIMUM` ≠ `minimum`
- Numeric values stored as strings, cast on use: `int(parser.get_value('ENGINE_DATA', 'MINIMUM'))`

### LUT Files Format

```
# Comment lines
1000|150.5
2000|180.3
3000|200.0
```

- Pipe-delimited: `X|Y`
- Used for curves: power.lut (RPM|kW), coast.lut (RPM|Nm), ctrl.lut, turbo.lut
- Must be sorted by X values for game interpolation

## Development Workflow

### Running the Application

```powershell
python main.py
```

First run prompts for AC installation path via File > Set AC Path menu.

### Running Tests

```powershell
python -m unittest tests.test_core
python tests/test_gui.py
```

Tests use fixtures in `tests/test_data/test_car/` - an example car structure with engine.ini, LUTs.

### Testing GUI Changes

Manual only. Pattern:

1. Run app: `python main.py`
2. Select test car from list (e.g., "ks_audi_r8_lms")
3. Click "Edit Car" button
4. Modify values in dialog
5. Verify changes saved to file and backup created

## Adding New Editor Tabs

Follow the engine tab pattern in `CarEditorDialog`:

1. **Create tab method**:

```python
def create_suspension_tab(self):
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Group related settings
    front_group = QGroupBox("Front Suspension")
    front_layout = QFormLayout()

    # Add spinboxes with appropriate ranges/units
    self.spring_rate = QDoubleSpinBox()
    self.spring_rate.setRange(0, 300000)
    self.spring_rate.setSuffix(" N/m")
    front_layout.addRow("Spring Rate:", self.spring_rate)

    front_group.setLayout(front_layout)
    layout.addWidget(front_group)
    layout.addStretch()
    return widget
```

2. **Initialize parser** in `init_parsers()`:

```python
susp_path = os.path.join(self.car_data_path, 'suspensions.ini')
if os.path.exists(susp_path):
    self.suspension_ini = IniParser(susp_path)
```

3. **Load data** in `load_data()`:

```python
if self.suspension_ini and self.suspension_ini.has_section('FRONT'):
    spring = self.suspension_ini.get_value('FRONT', 'SPRING_RATE', '80000')
    self.spring_rate.setValue(float(spring))
    self.original_values['spring_rate'] = float(spring)
```

4. **Save data** in `save_changes()`:

```python
if self.suspension_ini:
    self.suspension_ini.set_value('FRONT', 'SPRING_RATE', str(self.spring_rate.value()))
    self.suspension_ini.save(backup=True)
```

5. **Add to tabs** in `init_ui()`:

```python
self.suspension_tab = self.create_suspension_tab()
self.tabs.addTab(self.suspension_tab, "Suspension")
```

## Phased Development Plan

Refer to `plan.md` for full roadmap. Current status: **Phase 5 complete** (engine editor working).

**Next priorities** (Phase 6):

- Suspension tab (suspensions.ini: SPRING_RATE, DAMPER_FAST/SLOW, ROD_LENGTH)
- Differential tab (drivetrain.ini: POWER, COAST, PRELOAD for LSD/SPOOL sections)
- Weight tab (car.ini: TOTALMASS, CG_LOCATION)

**Phase 6.5** (major feature):

- Visual curve editor for .lut files using matplotlib
- Drag-drop point editing, add/remove points, interpolation
- See `plan.md` lines 55-67 for full requirements

## Common Pitfalls

1. **Don't hardcode AC path** - always use `ConfigManager.get_ac_path()` and `get_cars_path()`
2. **Check data folder exists** - use `CarFileManager.has_data_folder()` before editing
3. **Don't forget sys.path.insert** in new GUI files - imports will silently fail otherwise
4. **Always create backups** - use `save(backup=True)` on all parsers
5. **Strip whitespace** - IniParser does this automatically, but validate on LUT parsing
6. **Handle missing sections** - INI files may not have TURBO_0, use `parser.has_section()` first
7. **PyQt5 slot connections** - use `.clicked.connect()` not `.clicked.connect(method())`

## Testing Requirements

When adding features:

1. Add unit tests to `tests/test_core.py` for core functionality
2. Create test data in `tests/test_data/` if needed
3. Add integration tests to `tests/test_gui.py` for editor dialogs
4. Pattern: setUp creates temp copies, tearDown cleans up - never modify test fixtures directly

Example test structure:

```python
def test_save_with_backup(self):
    parser = IniParser(self.temp_file)
    parser.set_value('SECTION', 'KEY', 'new_value')
    parser.save(backup=True)

    self.assertTrue(os.path.exists(self.temp_file + '.bak'))
    backup = IniParser(self.temp_file + '.bak')
    self.assertEqual(backup.get_value('SECTION', 'KEY'), 'old_value')
```

## External References

- AC modding wiki: https://assetto-corsa.fandom.com/wiki/Data_Format
- INI file specs: Each car's data/\*.ini has different sections - inspect game files for schema
- LUT curves: No official docs - reverse-engineered from game behavior

## Examples Folder

The `examples/` folder contains real Assetto Corsa car data for testing and reference:

**Structure:**
```
examples/
├── data/              # Complete unpacked car data folder
│   ├── engine.ini
│   ├── suspensions.ini
│   ├── drivetrain.ini
│   ├── power.lut
│   ├── coast.lut
│   └── ... (all AC car files)
└── data.acd          # Original packed data.acd file
```

**Usage:**
- **Testing parsers**: Real-world INI and LUT files for validation
- **Reference data**: Example of correct AC file structure and values
- **Development**: Use as template when implementing new features
- **Unpacking tests**: data.acd file for testing unpacker functionality

**Important Notes:**
- Data is from a real AC car, representative of typical mod structure
- All file formats follow AC conventions (case-sensitive keys, specific sections)
- Use these files to understand expected ranges and parameter relationships
- When adding new parser features, test against these files first

