# AC Car Editor - Curve Editor Feature (Phase 6.5)

## Visual Curve Editor

The visual curve editor is now integrated into the Engine tab, allowing users to edit power.lut and coast.lut files graphically.

### Curve Editor Dialog

```
┌────────────────────────────────────────────────────────────────────────────────┐
│ Curve Editor                                                        ▢ ▭ ✕       │
├────────────────────────────────────────────────────────────────────────────────┤
│ ╔══════════════════════════════════════════════════════════════════════════╗  │
│ ║ Curve Information                                                         ║  │
│ ║ File: power.lut                   Load Preset: [Turbo (Lag)   ▼]         ║  │
│ ╚══════════════════════════════════════════════════════════════════════════╝  │
│                                                                                 │
│ ┌────────────────────────────────┬───────────────────────────────────────────┐│
│ │  MATPLOTLIB GRAPH              │  DATA POINTS TABLE                        ││
│ │                                │  ┌────────┬──────────┐                    ││
│ │  400┤                    ●      │  │   X    │    Y     │                    ││
│ │     │                  ●        │  ├────────┼──────────┤                    ││
│ │  350┤                ●          │  │  1000  │  100.0   │                    ││
│ │     │              ●            │  │  2000  │  180.5   │                    ││
│ │  300┤            ●              │  │  3000  │  250.0   │ ◄ Selected         ││
│ │     │          ●                │  │  4000  │  310.5   │                    ││
│ │  200┤        ●                  │  │  5000  │  360.0   │                    ││
│ │     │      ●                    │  │  6000  │  390.0   │                    ││
│ │  100┤    ●                      │  └────────┴──────────┘                    ││
│ │     │  ●                        │                                           ││
│ │    0┴────┬────┬────┬────┬───   │  X: [3000.0  ] Y: [250.0   ] [Add]       ││
│ │         2k   4k   6k   8k       │                                           ││
│ │         RPM                     │                                           ││
│ │  ⌂ ◄► + - ⊞                     │                                           ││
│ │  [Navigation Toolbar]           │                                           ││
│ │                                 │                                           ││
│ │  [Add Point] [Remove Point]    │                                           ││
│ └────────────────────────────────┴───────────────────────────────────────────┘│
│                                                                                 │
│  [Load File...] [Import...] [Export...]     [Save] [Save As...] [Close]       │
└────────────────────────────────────────────────────────────────────────────────┘
```

### Features

#### Interactive Graph (Left Panel)
- **Matplotlib Canvas**: Professional plotting with smooth curves
- **Navigation Toolbar**: Zoom, pan, home, back, forward, save buttons
- **Point Selection**: Click near a point to select it (highlighted in red)
- **Drag & Drop**: Drag selected points to adjust curve shape in real-time
- **Visual Feedback**: 
  - Blue line: The curve interpolated between points
  - Green circles: Data points
  - Red circle: Selected point
  - Grid lines for precision

#### Data Table (Right Panel)
- **Numerical View**: All curve points displayed as X|Y pairs
- **Synchronized Selection**: Selecting in table highlights point on graph and vice versa
- **Manual Editing**: Double-click cells to edit values directly
- **Auto-Sort**: Points automatically sorted by X value

#### Controls
- **Add Point Form**: Enter X and Y values, click Add button
- **Remove Point Button**: Delete selected point (also works with Delete key)
- **Load/Save**: Standard file operations with automatic backup
- **Import/Export**: Copy curves between different files
- **Presets**: Quick-load common curve patterns

### Integration with Engine Tab

```
┌────────────────────────────────────────────────────────────────────┐
│ Edit Car: Audi R8 LMS                                              │
├────────────────────────────────────────────────────────────────────┤
│ ┌═[Engine]═┬─[Suspension]─┬─[Differential]─┬─[Weight]─┬─[Aero]─┐ │
│ │                                                                 │ │
│ │  ╔═══════════════════════════════════════════════════╗         │ │
│ │  ║ Basic Engine Data                                  ║         │ │
│ │  ╠════════════════════════════════════════════════════╣         │ │
│ │  ║ Minimum RPM:         [1000      ] RPM              ║         │ │
│ │  ║ Maximum RPM:         [8500      ] RPM              ║         │ │
│ │  ║ Limiter RPM:         [8500      ] RPM              ║         │ │
│ │  ╚════════════════════════════════════════════════════╝         │ │
│ │                                                                 │ │
│ │  ╔═══════════════════════════════════════════════════╗         │ │
│ │  ║ Turbo                                              ║         │ │
│ │  ╠════════════════════════════════════════════════════╣         │ │
│ │  ║ Max Boost:           [1.50      ] bar              ║         │ │
│ │  ║ Wastegate:           [1.20      ] bar              ║         │ │
│ │  ╚════════════════════════════════════════════════════╝         │ │
│ │                                                                 │ │
│ │  ╔═══════════════════════════════════════════════════╗         │ │
│ │  ║ Power and Coast Curves               NEW! ✨       ║         │ │
│ │  ╠════════════════════════════════════════════════════╣         │ │
│ │  ║  [Edit Power Curve (power.lut)]                   ║         │ │
│ │  ║  Opens visual curve editor for power curve        ║         │ │
│ │  ║                                                    ║         │ │
│ │  ║  [Edit Coast Curve (coast.lut)]                   ║         │ │
│ │  ║  Opens visual curve editor for coast curve        ║         │ │
│ │  ╚════════════════════════════════════════════════════╝         │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  [Save Changes]  [Reset]                              [Cancel]     │
└────────────────────────────────────────────────────────────────────┘
```

### Preset Curves Available

1. **Linear**: Simple linear progression
   - Good for: Testing, basic understanding
   - Example: 0→0, 1000→100, 2000→200, etc.

2. **Turbo (Lag)**: Exponential growth with turbo lag
   - Good for: Turbocharged engines
   - Example: Slow build to 2500 RPM, then rapid increase

3. **NA (Linear Peak)**: Natural aspiration with peak
   - Good for: Naturally aspirated engines
   - Example: Linear growth to peak at 6000 RPM, then decline

4. **V-Shape (Coast)**: Coast curve with negative values
   - Good for: Engine braking curves
   - Example: Negative torque values forming V-shape

### Workflow Example

**Scenario**: Modify power curve to add more low-end torque

1. Click "Edit Power Curve" button in Engine tab
2. Curve editor dialog opens with current power.lut data
3. Select point at 2000 RPM (click on it)
4. Drag upward to increase power at that RPM
5. Click between points to add intermediate point
6. Adjust new point to smooth transition
7. Check table view for exact values
8. Click "Save" - automatic backup created
9. Close dialog
10. Test in-game!

### Technical Details

**File Format**: LUT files use pipe-delimited format
```
# Comments start with #
1000|100.5
2000|180.3
3000|250.0
```

**Features**:
- Automatic sorting by X value
- Backup creation (.lut.bak) before saving
- Linear interpolation between points
- Case-insensitive file loading
- Handles missing files gracefully

### Testing

**Test Coverage**: 37 tests total
- 7 curve editor integration tests
- All tests passing ✅

**Test Scenarios**:
- Loading existing curves
- Creating new curves from scratch
- Modifying and saving with backup verification
- Adding/removing/updating points
- Import/export workflow
- Preset curve creation

### Future Enhancements

Potential improvements for future versions:
- Spline interpolation for smoother curves
- Undo/redo functionality
- Copy/paste between curves
- Curve smoothing algorithms
- More preset templates
- Support for other .lut files (turbo.lut, ctrl.lut, etc.)
