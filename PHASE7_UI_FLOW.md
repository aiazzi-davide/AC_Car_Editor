# Phase 7 Features - UI Flow

## UI Metadata Editor Flow

```
Main Window
┌─────────────────────────────────────────────┐
│ Car List                 Car Information    │
│ ┌────────────┐          ┌────────────────┐ │
│ │ audi_a5    │          │ Audi A5 2.0    │ │
│ │ bmw_m3     │          │ [Preview Image]│ │
│ │ ferrari_458│          │                │ │
│ │            │          │ Brand: Audi    │ │
│ │            │          │ Has data: Yes  │ │
│ │            │          │                │ │
│ │            │          │ [Edit Car]     │ │
│ │            │          │ [Open Folder]  │ │
│ │            │          │ [Edit UI]  ←───┼─ NEW BUTTON
│ │            │          │ [Backup]       │ │
│ └────────────┘          └────────────────┘ │
└─────────────────────────────────────────────┘
                                 │
                                 │ Click "Edit UI"
                                 ▼
UI Editor Dialog
┌─────────────────────────────────────────────┐
│ Edit UI Metadata: audi_a5                   │
├─────────────────────────────────────────────┤
│ ┌─ Basic Information ──────────────────┐   │
│ │ Car Name:    [Audi A5 2.0 TFSI     ] │   │
│ │ Brand:       [Audi                  ] │   │
│ │ Class:       [street ▼]               │   │
│ │ Country:     [Germany               ] │   │
│ │ Year:        [2008]                   │   │
│ └──────────────────────────────────────┘   │
│                                             │
│ ┌─ Description ─────────────────────────┐  │
│ │ [Replica Audi A5 2.0 TFSI 180cv.    ]│  │
│ │ [FWD, Manuale 6 marce.               ]│  │
│ └──────────────────────────────────────┘  │
│                                             │
│ ┌─ Tags ───────────────────────────────┐  │
│ │ [fwd, manual, street, turbo         ]│  │
│ └──────────────────────────────────────┘  │
│                                             │
│ ┌─ Specifications ─────────────────────┐  │
│ │ Power:        [180 bhp              ] │  │
│ │ Torque:       [320 Nm               ] │  │
│ │ Weight:       [1425 kg              ] │  │
│ │ Top Speed:    [236 km/h             ] │  │
│ │ 0-100:        [7.8s 0-100           ] │  │
│ │ Power/Weight: [8.33 kg/hp           ] │  │
│ └──────────────────────────────────────┘  │
│                                             │
│ ┌─ Author Information ─────────────────┐  │
│ │ Author:  [TeamSESH / User Edit      ] │  │
│ │ Version: [1.1 Custom                ] │  │
│ └──────────────────────────────────────┘  │
│                                             │
│                        [Save]  [Cancel]     │
└─────────────────────────────────────────────┘
```

## Stage Tuning System Flow

```
Car Editor Dialog
┌──────────────────────────────────────────────┐
│ Edit Car: audi_a5                            │
├──────────────────────────────────────────────┤
│ [Engine] [Suspension] [Drivetrain] [Weight] │
│ [Aero] [Brakes] [Pneumatici]                │
│                                              │
│ ... (car parameters) ...                     │
│                                              │
│ [Save Changes] [Reset] [🔧 Setup Manager]   │
│ [🚀 Stage Tuning]  ←─────────────────────────┼─ NEW BUTTON
│                                  [Cancel]    │
└──────────────────────────────────────────────┘
                    │
                    │ Click "Stage Tuning"
                    ▼
Stage Tuning Dialog
┌──────────────────────────────────────────────┐
│ Stage Tuning: audi_a5                        │
├──────────────────────────────────────────────┤
│ ┌─ Current Configuration ────────────────┐  │
│ │ Engine Type: Turbocharged              │  │
│ │ Current Stage: Stock                   │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ ┌──────────────────────────────────────┐   │
│ │ Stage 1 - ECU Remap                  │   │
│ │ ┌────────────────────────────────┐   │   │
│ │ │ • Increase turbo boost by 15%  │   │   │
│ │ │ • Safe power increase          │   │   │
│ │ └────────────────────────────────┘   │   │
│ │         [Apply Stage 1]               │   │
│ └──────────────────────────────────────┘   │
│                                              │
│ ┌──────────────────────────────────────┐   │
│ │ Stage 2 - Turbo Upgrade              │   │
│ │ ┌────────────────────────────────┐   │   │
│ │ │ • Increase turbo boost by 30%  │   │   │
│ │ │ • More aggressive tuning       │   │   │
│ │ └────────────────────────────────┘   │   │
│ │         [Apply Stage 2]               │   │
│ └──────────────────────────────────────┘   │
│                                              │
│ ┌──────────────────────────────────────┐   │
│ │ Stage 3 - Full Build                 │   │
│ │ ┌────────────────────────────────┐   │   │
│ │ │ • Increase turbo boost by 50%  │   │   │
│ │ │ • +500 RPM limit               │   │   │
│ │ │ • Reduce weight by 5%          │   │   │
│ │ │ • Improve aerodynamics         │   │   │
│ │ │ • Upgrade differential         │   │   │
│ │ │ • +10% power curve             │   │   │
│ │ └────────────────────────────────┘   │   │
│ │         [Apply Stage 3]               │   │
│ └──────────────────────────────────────┘   │
│                                              │
│ [Reset to Stock (Clear Stage Marker)]       │
│                                              │
│                              [Close]         │
└──────────────────────────────────────────────┘
                    │
                    │ Click "Apply Stage 1"
                    ▼
Confirmation Dialog
┌──────────────────────────────────────────────┐
│ Apply Stage 1 - ECU Remap                    │
├──────────────────────────────────────────────┤
│ This will apply the following modifications: │
│                                              │
│ • Increase turbo boost by 15%                │
│ • Safe power increase for daily driving      │
│                                              │
│ Backups will be created automatically.       │
│                                              │
│ Do you want to continue?                     │
│                                              │
│                     [Yes]  [No]              │
└──────────────────────────────────────────────┘
                    │
                    │ Click "Yes"
                    ▼
Success Dialog
┌──────────────────────────────────────────────┐
│ Success                                      │
├──────────────────────────────────────────────┤
│ Stage 1 - ECU Remap applied successfully!    │
│                                              │
│ Backups have been created for all modified   │
│ files.                                       │
│                                              │
│                            [OK]              │
└──────────────────────────────────────────────┘
```

## Stage Tuning Logic Comparison

### NA (Naturally Aspirated) Cars

```
Stock Car                         Stage 1 (ECU Remap)
─────────────                     ───────────────────
Power Curve: 100% baseline        Power Curve: 108%
Turbo:       None                 Turbo:       None
                                  
                ⬇                                ⬇
                                  
Stage 2 (Turbo Conversion)        Stage 3 (Full Build)
──────────────────────            ────────────────────
Power Curve: 113% (108% × 1.05)   Power Curve: 127% (113% × 1.12)
Turbo:       0.35 bar added       Turbo:       0.42 bar (0.35 × 1.20)
                                  Weight:      95% (-5%)
                                  Drag (CD):   90% (-10%)
                                  Inertia:     85% (-15%)
```

### Turbocharged Cars

```
Stock Car                         Stage 1 (ECU Remap)
─────────────                     ───────────────────
Boost:       0.50 bar baseline    Boost:       0.575 bar (+15%)
                                  
                ⬇                                ⬇
                                  
Stage 2 (Turbo Upgrade)           Stage 3 (Full Build)
───────────────────────           ────────────────────
Boost:       0.65 bar (+30%)      Boost:       0.75 bar (+50%)
                                  Power Curve: 110%
                                  Weight:      95% (-5%)
                                  Drag (CD):   85% (-15%)
                                  Downforce:   115% (+15%)
                                  RPM Limit:   +500 RPM
                                  Differential: 120% power
                                  Inertia:     85% (-15%)
```

## File Modification Matrix

### NA Cars

| File | Stage 1 | Stage 2 | Stage 3 |
|------|---------|---------|---------|
| engine.ini | ✅ (marker) | ✅ (add turbo) | ✅ (turbo + inertia) |
| power.lut | ✅ (+8%) | ✅ (+5%) | ✅ (+12%) |
| car.ini | - | - | ✅ (-5% weight) |
| aero.ini | - | - | ✅ (-10% drag) |
| drivetrain.ini | - | - | - |

### Turbocharged Cars

| File | Stage 1 | Stage 2 | Stage 3 |
|------|---------|---------|---------|
| engine.ini | ✅ (+15% boost) | ✅ (+30% boost) | ✅ (+50% boost, +500 RPM, -15% inertia) |
| power.lut | - | - | ✅ (+10%) |
| car.ini | - | - | ✅ (-5% weight) |
| aero.ini | - | - | ✅ (-15% drag, +15% downforce) |
| drivetrain.ini | - | - | ✅ (+20% diff power) |

## Integration Points

### Main Window Integration
```python
# Button added in create_car_info_panel()
self.edit_ui_btn = QPushButton("Edit UI")
self.edit_ui_btn.setEnabled(True)  # Always enabled
self.edit_ui_btn.clicked.connect(self.edit_ui_metadata)

# Method added
def edit_ui_metadata(self):
    editor = UIEditorDialog(self.current_car, car_path, self)
    editor.exec_()
```

### Car Editor Dialog Integration
```python
# Button added in init_ui()
self.stage_btn = QPushButton("🚀 Stage Tuning")
self.stage_btn.clicked.connect(self.open_stage_tuning)

# Method added
def open_stage_tuning(self):
    dlg = StageTuningDialog(self.car_name, self.car_data_path, self)
    if dlg.exec_():
        self.load_data()  # Reload if changes made
```

## Example Use Cases

### Use Case 1: Rebrand a Car
1. Select car in main window
2. Click "Edit UI"
3. Change name: "Generic A5" → "Audi A5 Stage 2 Turbo"
4. Update brand: "Unknown" → "Audi"
5. Add tags: "stage2, turbo"
6. Update specs: "180 bhp" → "220 bhp"
7. Save
8. Car now appears with new name in AC menu

### Use Case 2: Quick Performance Upgrade (Turbo Car)
1. Open car editor
2. Click "🚀 Stage Tuning"
3. See: "Engine Type: Turbocharged, Current Stage: Stock"
4. Click "Apply Stage 1"
5. Confirm (boost increases from 0.5 → 0.575 bar)
6. Success message shown
7. Dialog updates: "Current Stage: Stage 1"
8. Close stage dialog
9. Save car editor
10. Test in-game

### Use Case 3: NA to Turbo Conversion
1. Open NA car in editor
2. Click "🚀 Stage Tuning"
3. See: "Engine Type: Naturally Aspirated, Current Stage: Stock"
4. Apply Stage 1 (ECU remap, +8% power)
5. Apply Stage 2 (adds turbo system, 0.35 bar boost)
6. Apply Stage 3 (enhances turbo, reduces weight, improves aero)
7. Car is now fully turbocharged with comprehensive upgrades
8. Update UI metadata to reflect changes
9. Save and test

## Tips and Best Practices

### UI Editing
- ✅ Use HTML tags in description for formatting (`<br>` for line breaks)
- ✅ Keep specs accurate to avoid confusion
- ✅ Use descriptive tags for easy filtering
- ✅ Include author credit when modifying others' cars
- ✅ Version number helps track modifications

### Stage Tuning
- ✅ Create backup before stage tuning (main window button)
- ✅ Apply stages in order (1 → 2 → 3) for balanced progression
- ✅ Test each stage in-game before applying next
- ✅ Update UI metadata after stage tuning (e.g., add "Stage 2" to car name)
- ✅ Stage 3 is aggressive - only for experienced tuners
- ⚠️ Reset to Stock only clears marker - use backups to fully revert
- ⚠️ NA Stage 2/3 fundamentally change engine (adds turbo)
- ⚠️ Multiple turbo units (TURBO_0, TURBO_1, etc.) all get upgraded

## Technical Notes

### Stage Marker
The stage level is stored in `engine.ini`:
```ini
[HEADER]
STAGE_LEVEL=1
```

This marker is checked by `StageTuner.get_current_stage()` to display current stage and prevent accidental re-application.

### Backup Strategy
Both features use the standard backup pattern:
- UIManager: `ui_car.json.bak`
- StageTuner: `engine.ini.bak`, `power.lut.bak`, etc.

All parsers call `save(backup=True)` which creates `.bak` files before writing.

### Multi-Turbo Support
If a car has multiple turbo units (TURBO_0, TURBO_1, TURBO_2, etc.), stage tuning will:
- Iterate through all `TURBO_N` sections
- Apply boost increase to each turbo
- Maintain relative boost ratios

Example:
```
Stock:    TURBO_0 = 0.5 bar, TURBO_1 = 0.4 bar
Stage 1:  TURBO_0 = 0.575 bar, TURBO_1 = 0.46 bar (both +15%)
```

## Common Questions

**Q: Can I skip stages?**
A: Yes, you can apply any stage directly. However, applying them in order (1→2→3) is recommended for balanced progression.

**Q: What if I apply Stage 3 twice?**
A: The stage marker prevents confusion, but physically, modifications would compound (e.g., boost would increase by 50% again). Always check current stage before applying.

**Q: Can I revert stage tuning?**
A: Use the backup system. "Reset to Stock" only clears the marker, not the modifications. Restore from timestamped backups to fully revert.

**Q: Do stages work on all cars?**
A: Stage tuning works on any car with engine.ini. Features are applied based on what files exist (e.g., aero.ini needed for aero upgrades).

**Q: Does UI editing affect performance?**
A: No. ui_car.json only controls menu display. Performance is controlled by data/ folder files.

**Q: Can I edit UI without unpacking data.acd?**
A: Yes! UI editing doesn't require data folder - ui/ is separate from data.acd.
