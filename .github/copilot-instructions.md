# AC Car Editor - AI Coding Agent Instructions

## Quick Reference

**Desktop PyQt5 app** for modifying Assetto Corsa car configs. Edits INI files and LUT lookup tables in unpacked `data/` folders. Always renames `data.acd` → `data.acd.bak` (safe, recoverable).

**Full AC file format docs**: [assettocorsa_car_data_documentation.md](assettocorsa_car_data_documentation.md)  
**Development plan + phase status**: [plan.md](../plan.md)

## Architecture

- **Core** (`src/core/`): File parsers, managers, configuration
- **GUI** (`src/gui/`): PyQt5 windows and dialogs
- **Entry**: `main.py` bootstraps app + sys.path

### Key Classes

| Class              | File                   | Purpose                                                                                                |
| ------------------ | ---------------------- | ------------------------------------------------------------------------------------------------------ |
| `IniParser`        | `ini_parser.py`        | Parse/write `.ini` files (case-sensitive, numeric cast with `int(float(...))`)                         |
| `LUTCurve`         | `lut_parser.py`        | Parse/write `.lut` lookup tables (`X\|Y` format, ignore `#` comments)                                  |
| `CarFileManager`   | `car_file_manager.py`  | Navigate `content/cars/[car_name]/data/`, unpack via quickBMS, `delete_data_acd()` renames to `.bak`   |
| `ConfigManager`    | `config.py`            | Store AC path in `config.json` (default: `C:\Program Files (x86)\Steam\steamapps\common\assettocorsa`) |
| `ComponentLibrary` | `component_library.py` | JSON-based reusable components (schema: `{id, name, description, tags, data}`)                         |

### GUI Classes

| Class                     | File                           | Purpose                                                                              |
| ------------------------- | ------------------------------ | ------------------------------------------------------------------------------------ |
| `MainWindow`              | `main_window.py`               | Car list, edit dialog launcher                                                       |
| `CarEditorDialog`         | `car_editor_dialog.py`         | 6 tabs (Engine, Suspension, Drivetrain, Weight, Aero, Brakes), each in `QScrollArea` |
| `CurveEditorWidget`       | `curve_editor_widget.py`       | Matplotlib-based interactive LUT editor (drag points, add/remove, smooth via PCHIP)  |
| `ComponentSelectorDialog` | `component_selector_dialog.py` | "Import from Library" buttons in each tab                                            |
| `ComponentLibraryDialog`  | `component_library_dialog.py`  | Full CRUD component manager                                                          |

## Critical Patterns

### Path Imports

Every GUI file requires:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.ini_parser import IniParser
```

### Tab Structure Pattern

1. `create_*_tab()` — build widgets, use `_tip(widget, "description (INI_KEY)")` for tooltips
2. `_load_*_data()` — read from parsers → widgets, set `original_values`
3. `_save_*_data()` — write from widgets → parsers, call `parser.save(backup=True)`
4. `reset_values()` — re-run all `_load_*` methods (parsers retain disk values)

**Tooltip rule**: Always include INI key name: `_tip(w, "What it does (SOME_KEY)")`  
**Numeric parsing**: Always `int(float(parser.get_value(...)))` (AC stores `1.00`)

### Dynamic Widget Creation

- **Turbos**: Count `TURBO_N` sections → create widgets dynamically, store as `turbo_0_max_boost`, etc.
- **Aero**: Count `WING_N` sections → one `QGroupBox` per wing via `_create_wing_widget(index)`
- **Suspension details**: `CG_LOCATION` + `WHEELBASE` live in `suspensions.ini [BASIC]`, not `car.ini`

### Backup Strategy

- **Parser-level**: `parser.save(backup=True)` → `.bak` alongside original
- **Manager-level**: `CarFileManager.create_backup()` → timestamped in `backups/`

## Testing & Examples

- **Examples folder**: `examples/data/` (complete real AC car, 47 INI + 14 LUT files), `examples/data.acd` (original packed)
- **Test fixtures**: `tests/test_data/test_car/` — tests copy fixtures to temp files, never modify originals
- **Run app**: `python main.py`
- **Run tests**: `python -m unittest tests.test_core` or `python tests/test_gui.py`

## Documentation Maintenance

**CRITICAL**: Always update these files when making changes:

1. **[plan.md](../plan.md)** — Update phase status table when completing phases or adding features
2. **[README.md](../README.md)** — Update features list, installation steps, usage overview
3. **Comments in code** — Keep inline comments synced with actual behavior
4. **[copilot-instructions.md](copilot-instructions.md)** — Update architecture and patterns if new paradigms are introduced

- in general update every markdown involved with the modification you are doing.

Example: If you implement Phase 7 (Undo/Redo), mark it as ✅ in `plan.md`'s feature table and describe it in `README.md`.

- If temp scripts are needed, remember to delete them after use and do not commit them to the repo.
