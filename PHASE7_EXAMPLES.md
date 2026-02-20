# Stage Tuning - Before/After Examples

This document shows concrete examples of how stage tuning modifies car files.

## Example 1: NA Car - Stage 1 (ECU Remap)

### Before (Stock)

**engine.ini:**
```ini
[ENGINE_DATA]
MINIMUM=1000
MAXIMUM=7000
LIMITER=7500
INERTIA=0.20
```

**power.lut:**
```
1000|100
3000|200
5000|300
7000|280
```

### After Stage 1

**engine.ini:**
```ini
[HEADER]
STAGE_LEVEL=1

[ENGINE_DATA]
MINIMUM=1000
MAXIMUM=7000
LIMITER=7500
INERTIA=0.20
```

**power.lut:**
```
1000|108
3000|216
5000|324
7000|302
```

**Changes:**
- ✅ Power curve increased by 8% (100→108, 200→216, 300→324, 280→302)
- ✅ Stage marker added: STAGE_LEVEL=1

---

## Example 2: NA Car - Stage 2 (Turbo Conversion)

### Before (After Stage 1)

**engine.ini:**
```ini
[HEADER]
STAGE_LEVEL=1

[ENGINE_DATA]
MINIMUM=1000
MAXIMUM=7000
LIMITER=7500
INERTIA=0.20
```

### After Stage 2

**engine.ini:**
```ini
[HEADER]
STAGE_LEVEL=2

[ENGINE_DATA]
MINIMUM=1000
MAXIMUM=7000
LIMITER=7500
INERTIA=0.20

[TURBO_0]
LAG_DN=0.92
LAG_UP=0.97
MAX_BOOST=0.35
WASTEGATE=0.50
DISPLAY_MAX_BOOST=1.0
REFERENCE_RPM=3000
```

**power.lut:**
```
1000|113
3000|227
5000|340
7000|317
```

**Changes:**
- ✅ TURBO_0 section added with 0.35 bar boost
- ✅ Power curve increased by additional 5% (108→113, 216→227, etc.)
- ✅ Stage marker updated: STAGE_LEVEL=2
- 🔄 Car is now turbocharged!

---

## Example 3: Turbo Car - Stage 1 (ECU Remap)

### Before (Stock Turbo Car)

**engine.ini:**
```ini
[ENGINE_DATA]
MINIMUM=1000
MAXIMUM=7000
LIMITER=7500
INERTIA=0.20

[TURBO_0]
LAG_DN=0.92
LAG_UP=0.97
MAX_BOOST=0.50
WASTEGATE=0.60
```

### After Stage 1

**engine.ini:**
```ini
[HEADER]
STAGE_LEVEL=1

[ENGINE_DATA]
MINIMUM=1000
MAXIMUM=7000
LIMITER=7500
INERTIA=0.20

[TURBO_0]
LAG_DN=0.92
LAG_UP=0.97
MAX_BOOST=0.575
WASTEGATE=0.60
```

**Changes:**
- ✅ MAX_BOOST increased by 15% (0.50 → 0.575)
- ✅ Stage marker added: STAGE_LEVEL=1

---

## Example 4: Turbo Car - Stage 3 (Full Build)

### Before (Stock Turbo Car)

**engine.ini:**
```ini
[ENGINE_DATA]
MINIMUM=1000
MAXIMUM=7000
LIMITER=7500
INERTIA=0.20

[TURBO_0]
MAX_BOOST=0.50
```

**car.ini:**
```ini
[BASIC]
TOTALMASS=1400
```

**aero.ini:**
```ini
[HEADER]
CD=0.35

[WING_0]
CL=0.50
```

**drivetrain.ini:**
```ini
[DIFFERENTIAL]
POWER=0.10
```

**power.lut:**
```
1000|100
7000|280
```

### After Stage 3

**engine.ini:**
```ini
[HEADER]
STAGE_LEVEL=3

[ENGINE_DATA]
MINIMUM=1000
MAXIMUM=7000
LIMITER=8000
INERTIA=0.17

[TURBO_0]
MAX_BOOST=0.75
```

**car.ini:**
```ini
[BASIC]
TOTALMASS=1330
```

**aero.ini:**
```ini
[HEADER]
CD=0.2975

[WING_0]
CL=0.575
```

**drivetrain.ini:**
```ini
[DIFFERENTIAL]
POWER=0.12
```

**power.lut:**
```
1000|110
7000|308
```

**Changes:**
- ✅ MAX_BOOST: 0.50 → 0.75 (+50%)
- ✅ LIMITER: 7500 → 8000 (+500 RPM)
- ✅ INERTIA: 0.20 → 0.17 (-15%, faster revving)
- ✅ TOTALMASS: 1400 → 1330 kg (-5%)
- ✅ CD (drag): 0.35 → 0.2975 (-15%)
- ✅ CL (downforce): 0.50 → 0.575 (+15%)
- ✅ DIFFERENTIAL POWER: 0.10 → 0.12 (+20%)
- ✅ Power curve: +10% (100→110, 280→308)
- ✅ Stage marker: STAGE_LEVEL=3

---

## UI Metadata Example

### Before Editing

**ui/ui_car.json:**
```json
{
  "name": "Audi A5 2.0 TFSI",
  "brand": "Audi",
  "class": "street",
  "country": "Germany",
  "description": "Stock Audi A5.",
  "tags": ["fwd", "manual", "street"],
  "specs": {
    "bhp": "180 bhp",
    "torque": "320 Nm",
    "weight": "1425 kg"
  },
  "year": 2008
}
```

### After Stage 3 + UI Edit

**ui/ui_car.json:**
```json
{
  "name": "Audi A5 2.0 TFSI Stage 3",
  "brand": "Audi / Tuning Shop",
  "class": "street",
  "country": "Germany",
  "description": "Fully built Audi A5.<br>Stage 3: Turbo + Weight Reduction + Aero.<br>220+ bhp.",
  "tags": ["fwd", "manual", "street", "stage3", "turbo", "tuned"],
  "specs": {
    "bhp": "220+ bhp",
    "torque": "380+ Nm",
    "weight": "1330 kg",
    "topspeed": "250+ km/h"
  },
  "year": 2008,
  "author": "Original: TeamSESH | Stage Tuning: User",
  "version": "1.1 Stage 3"
}
```

**Changes:**
- ✅ Name updated to reflect Stage 3
- ✅ Brand includes tuning shop credit
- ✅ Description updated with modifications
- ✅ Tags added: stage3, turbo, tuned
- ✅ Specs updated to match Stage 3 performance
- ✅ Author credit preserved and extended
- ✅ Version reflects modification

---

## Performance Impact

### NA Car Progression

| Stage | Power | Torque @ 5000 RPM | 0-100 km/h | Top Speed |
|-------|-------|-------------------|------------|-----------|
| Stock | 100% | 300 Nm | 8.0s | 220 km/h |
| Stage 1 | 108% | 324 Nm | ~7.5s | ~228 km/h |
| Stage 2 | 113% + Turbo | 340 Nm + boost | ~7.0s | ~240 km/h |
| Stage 3 | 127% + Turbo | 381 Nm + boost | ~6.0s | ~260 km/h |

*Note: 0-100 and top speed are estimates. Stage 3 also reduces weight (-5%) and drag (-10%) which further improves performance.*

### Turbo Car Progression

| Stage | Boost | Power Curve | Weight | Drag | Performance Gain |
|-------|-------|-------------|--------|------|------------------|
| Stock | 0.50 bar | 100% | 1400 kg | CD 0.35 | Baseline |
| Stage 1 | 0.575 bar | 100% | 1400 kg | CD 0.35 | +15% (boost only) |
| Stage 2 | 0.65 bar | 100% | 1400 kg | CD 0.35 | +30% (boost only) |
| Stage 3 | 0.75 bar | 110% | 1330 kg | CD 0.30 | +65% (boost + power + weight + aero) |

*Stage 3 provides compound improvements: higher boost (50%), more power (10%), less weight (5%), better aero (15%), improved differential, and higher RPM limit.*

## Backup File Examples

After applying Stage 3, the following backup files are created:

```
data/
├── engine.ini
├── engine.ini.bak           ← Backup before Stage 3
├── power.lut
├── power.lut.bak            ← Backup before Stage 3
├── car.ini
├── car.ini.bak              ← Backup before Stage 3
├── aero.ini
├── aero.ini.bak             ← Backup before Stage 3
├── drivetrain.ini
└── drivetrain.ini.bak       ← Backup before Stage 3
```

You can manually restore by:
1. Copy `.bak` file
2. Rename removing `.bak` extension
3. Reload car in editor

Or use the "Create Backup" button for timestamped backups:
```
backups/
└── audi_a5_20260219_143052/
    └── data/
        └── (complete car data snapshot)
```
