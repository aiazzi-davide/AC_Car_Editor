# Component Import Feature - UI Overview

## Main Window Integration

The component import feature is integrated into the Car Editor Dialog through prominent green buttons in each tab.

## Car Editor Dialog - Engine Tab

```
┌─────────────────────────────────────────────────────────┐
│ Edit Car: [Car Name]                                    │
├─────────────────────────────────────────────────────────┤
│ [Engine] [Suspension] [Differential] [Weight] [Aero]    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─── Basic Engine Data ───────────────────────┐       │
│  │  Minimum RPM:    [1000    ] RPM             │       │
│  │  Maximum RPM:    [7000    ] RPM             │       │
│  │  Limiter RPM:    [7500    ] RPM             │       │
│  └─────────────────────────────────────────────┘       │
│                                                          │
│  ┌─── Turbo ────────────────────────────────────┐       │
│  │  Max Boost:      [1.00 ] bar                │       │
│  │  Wastegate:      [0.80 ] bar                │       │
│  └─────────────────────────────────────────────┘       │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Import Engine from Library...                   │  │ <- Green button
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌─── Power and Coast Curves ──────────────────┐       │
│  │  [Edit Power Curve (power.lut)]             │       │
│  │  [Edit Coast Curve (coast.lut)]             │       │
│  └─────────────────────────────────────────────┘       │
│                                                          │
│                          [Save Changes] [Reset] [Close] │
└─────────────────────────────────────────────────────────┘
```

## Component Selector Dialog

When clicking "Import Engine from Library...", the following dialog opens:

```
┌─────────────────────────────────────────────────────────────────┐
│ Select Engine Component                                 [×]     │
├─────────────────────────────────────────────────────────────────┤
│  Select an engine component from the library:                   │
├─────────────────────────────────────────────────────────────────┤
│ ┌─ Available Components ─┐  ┌─ Component Details ────────────┐ │
│ │                         │  │ Name:                          │ │
│ │ Street NA Engine      ← │  │ Street Turbo Engine            │ │
│ │ Race NA Engine          │  │                                │ │
│ │ Street Turbo Engine     │  │ Tags:                          │ │
│ │ Race Turbo Engine       │  │ turbo, street, boost           │ │
│ │                         │  │                                │ │
│ │                         │  │ Description:                   │ │
│ │                         │  │ Turbocharged street engine     │ │
│ │                         │  │ with moderate boost            │ │
│ │                         │  │                                │ │
│ │                         │  │ Parameters:                    │ │
│ │                         │  │ MINIMUM = 1000                 │ │
│ │                         │  │ MAXIMUM = 7000                 │ │
│ │                         │  │ LIMITER = 7500                 │ │
│ │                         │  │ INERTIA = 0.18                 │ │
│ │                         │  │ TURBO_MAX_BOOST = 1.0          │ │
│ │                         │  │ TURBO_WASTEGATE = 0.8          │ │
│ └─────────────────────────┘  └────────────────────────────────┘ │
│                                                                  │
│                          [Apply Component] [Cancel]             │
└─────────────────────────────────────────────────────────────────┘
```

## Confirmation Dialog

After clicking "Apply Component", a confirmation appears:

```
┌─────────────────────────────────────────────────┐
│ Apply Component                          [?]    │
├─────────────────────────────────────────────────┤
│ Apply 'Street Turbo Engine' to the car?         │
│                                                  │
│ This will update the current values in the      │
│ editor.                                          │
│                                                  │
│                              [Yes]    [No]      │
└─────────────────────────────────────────────────┘
```

## Success Message

After applying, an information dialog shows:

```
┌─────────────────────────────────────────────────┐
│ Component Applied                       [i]     │
├─────────────────────────────────────────────────┤
│ Applied 'Street Turbo Engine' to engine         │
│ settings.                                        │
│                                                  │
│ Updated fields:                                  │
│ - Minimum RPM                                    │
│ - Maximum RPM                                    │
│ - Limiter RPM                                    │
│ - Max Boost                                      │
│ - Wastegate                                      │
│                                                  │
│ Remember to save changes to apply them to       │
│ the car.                                         │
│                                                  │
│                                    [OK]          │
└─────────────────────────────────────────────────┘
```

## Other Tabs

The same "Import from Library..." button appears in:

### Suspension Tab
- Button: "Import Suspension from Library..."
- Components: Street Suspension (Soft), Sport Suspension, Race Suspension (Stiff)
- Updates: Spring rates, dampers (fast/slow, bump/rebound), rod lengths

### Differential Tab  
- Button: "Import Differential from Library..."
- Components: Open Differential, Street LSD, Race LSD, Spool (Locked)
- Updates: Differential type, power, coast, preload

### Aerodynamics Tab
- Button: "Import Aero from Library..."
- Components: Street Aero, Sport Aero, Race Aero
- Updates: Drag coefficient, front/rear lift coefficients, CL gains

## Key Visual Elements

1. **Green Buttons**: All "Import from Library..." buttons use green color (#4CAF50) for high visibility
2. **Split Layout**: Component Selector uses a 1:2 ratio split (list:details)
3. **Clear Labeling**: All fields show units (RPM, bar, N/m, etc.)
4. **Confirmation Flow**: Preview → Confirm → Success message
5. **Feedback**: Success dialog explicitly lists which fields were updated

## User Experience Flow

1. User opens car editor
2. Navigates to desired tab (Engine, Suspension, etc.)
3. Clicks green "Import from Library..." button
4. Component Selector dialog opens
5. User browses available components in left panel
6. Selection shows full details in right panel
7. User reviews parameters
8. Clicks "Apply Component"
9. Confirmation dialog asks for final approval
10. Success message confirms which fields were updated
11. User sees updated values in the car editor
12. User clicks "Save Changes" to persist to files
13. Automatic backup is created

This workflow provides a safe, transparent, and user-friendly way to apply library components to cars.
