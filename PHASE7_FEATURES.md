# Phase 7 Features: UI Editor and Stage Tuning

This document describes the two new features added in Phase 7 completion.

## 1. UI Metadata Editor

### Purpose
Edit the `ui/ui_car.json` file that controls how the car appears in Assetto Corsa's car selection menu.

### Location
- **Main Window**: "Edit UI" button (appears when a car is selected)

### Features
The UI Editor allows you to modify:

#### Basic Information
- **Car Name**: Display name shown in AC car menu
- **Brand**: Car manufacturer (e.g., "Ferrari", "Porsche", "Audi")
- **Class**: Car category (street/race/drift/vintage/concept)
- **Country**: Country of origin (e.g., "Italy", "Germany", "Japan")
- **Year**: Year of production

#### Description
- Multi-line description with HTML support
- Use `<br>` tags for line breaks
- Shown in AC car selection menu

#### Tags
- Comma-separated list of tags
- Used for filtering and search
- Examples: "turbo", "fwd", "manual", "street"

#### Specifications
- **Power**: e.g., "180 bhp"
- **Torque**: e.g., "320 Nm"
- **Weight**: e.g., "1425 kg"
- **Top Speed**: e.g., "236 km/h"
- **0-100**: e.g., "7.8s 0-100"
- **Power/Weight**: e.g., "8.33 kg/hp"

#### Author Information
- **Author**: Mod creator name
- **Version**: Mod version (e.g., "1.0", "2.5 Beta")

### Technical Details
- Edits `ui/ui_car.json` file in car folder
- Automatic backup creation (`.bak` file)
- Creates ui/ folder if it doesn't exist
- Creates default ui_car.json if file doesn't exist

---

## 2. Stage Tuning System

### Purpose
Apply one-click performance upgrades to cars with different logic for naturally aspirated (NA) and turbocharged engines.

### Location
- **Car Editor Dialog**: "🚀 Stage Tuning" button in button bar (next to Setup Manager)

### How It Works

The system automatically detects if a car is:
- **NA (Naturally Aspirated)**: No `TURBO_0` section in engine.ini
- **Turbocharged**: Has `TURBO_0` section in engine.ini

Based on the engine type, different tuning logic is applied for each stage.

### Stage Progression

#### NA Cars (Naturally Aspirated)

**Stage 1 - ECU Remap**
- More aggressive engine mapping
- +8% increase to power curve
- Optimized for NA performance
- Files modified: `power.lut`, `engine.ini`

**Stage 2 - Turbo Conversion**
- Add complete turbo system
- Basic turbo configuration (0.35 bar boost)
- +5% base power increase
- Files modified: `engine.ini` (add TURBO_0 section), `power.lut`

**Stage 3 - Full Turbo Build**
- Enhanced turbo boost (+20% over Stage 2)
- +12% power curve increase
- -5% weight reduction
- -10% drag coefficient (improved aerodynamics)
- -15% engine inertia (faster revving)
- Files modified: `engine.ini`, `power.lut`, `car.ini`, `aero.ini`

#### Turbocharged Cars

**Stage 1 - ECU Remap**
- +15% turbo boost increase
- Safe power increase for daily driving
- Files modified: `engine.ini` (all TURBO_N sections)

**Stage 2 - Turbo Upgrade**
- +30% turbo boost increase
- More aggressive tuning
- Files modified: `engine.ini` (all TURBO_N sections)

**Stage 3 - Full Build**
- +50% turbo boost increase
- +500 RPM to limiter
- +10% power curve increase
- -5% weight reduction
- -15% drag coefficient
- +15% downforce on all wings
- +20% differential power (better power handling)
- -15% engine inertia
- Files modified: `engine.ini`, `power.lut`, `car.ini`, `aero.ini`, `drivetrain.ini`

### Stage Tracking

The system tracks the current stage level in `engine.ini`:
```ini
[HEADER]
STAGE_LEVEL=1
```

- `0` = Stock
- `1` = Stage 1 applied
- `2` = Stage 2 applied
- `3` = Stage 3 applied

### Safety Features

1. **Automatic Backups**: All modified files get `.bak` backups
2. **Confirmation Dialogs**: User must confirm before applying each stage
3. **Clear Descriptions**: Each stage shows exactly what will be modified
4. **Reset Function**: Can clear stage marker (note: doesn't revert changes, use backups for full restoration)

### Usage Flow

1. Open car in Car Editor Dialog
2. Click "🚀 Stage Tuning" button
3. Dialog shows:
   - Current engine type (NA or Turbocharged)
   - Current stage level (Stock or 1/2/3)
   - Descriptions of all three stages
4. Click "Apply Stage X" button
5. Confirm the changes
6. Stage is applied with automatic backups
7. Dialog updates to show new stage level

### Technical Implementation

#### Core Classes
- **`StageTuner`** (`src/core/stage_tuner.py`): Core tuning logic
  - Detects NA vs Turbo
  - Applies stage-specific modifications
  - Tracks stage level
  
- **`StageTuningDialog`** (`src/gui/stage_tuning_dialog.py`): GUI dialog
  - Displays stage descriptions
  - Handles user confirmation
  - Updates on stage changes

#### Key Methods
- `_detect_turbo()`: Check for TURBO_0 section
- `apply_stage_1/2/3()`: Apply stage-specific logic
- `get_stage_description(stage)`: Get human-readable descriptions
- `reset_to_stock()`: Clear stage marker

#### Files Modified by Stage Tuning

| Stage | NA Cars | Turbo Cars |
|-------|---------|------------|
| 1 | power.lut, engine.ini | engine.ini |
| 2 | engine.ini, power.lut | engine.ini |
| 3 | engine.ini, power.lut, car.ini, aero.ini | engine.ini, power.lut, car.ini, aero.ini, drivetrain.ini |

---

## Testing

New test suite: `tests/test_ui_stage.py`

**UI Manager Tests** (7 tests):
- Load/modify/save ui_car.json
- Create default ui_car.json
- Handle tags and specs dictionaries
- Backup creation

**Stage Tuner Tests** (10 tests):
- Detect NA vs Turbo cars
- Apply Stage 1/2/3 for both NA and turbo
- Track stage level
- Reset to stock
- Verify modifications (power curve, boost, weight, aero)

**Total**: 121 passing tests (17 new tests added)

Run tests:
```bash
python -m unittest tests.test_ui_stage -v
```

---

## Usage Examples

### Edit UI Metadata
1. Select a car in main window
2. Click "Edit UI" button
3. Modify car name: "Audi A5 2.0 TFSI" → "Audi A5 Stage 2 Turbo"
4. Update specs: "180 bhp" → "220 bhp"
5. Add tags: "turbo, stage2"
6. Click "Save"
7. Car name updates in AC menu

### Apply Stage Tuning
1. Open car in editor
2. Click "🚀 Stage Tuning"
3. See current engine type and stage
4. Apply stages in order (1 → 2 → 3) for best results
5. Backups created automatically
6. Close and save car editor

### Recommended Workflow
1. Create backup first (main window "Create Backup" button)
2. Apply stage tuning
3. Edit UI metadata to reflect new stage
4. Test in-game
5. Restore from backup if needed

---

## Benefits

### UI Editor
- ✅ Change car names without text editors
- ✅ Update specs to match modifications
- ✅ Add custom tags for organization
- ✅ Professional presentation in AC menu
- ✅ Automatic backup safety

### Stage Tuning
- ✅ Quick performance upgrades (seconds vs manual editing)
- ✅ Intelligent NA vs Turbo logic
- ✅ Balanced modifications (no broken physics)
- ✅ Progressive tuning path (Stage 1 → 2 → 3)
- ✅ Complete modification logging
- ✅ All backups preserved
