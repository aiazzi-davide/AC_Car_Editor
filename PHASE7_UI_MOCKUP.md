# AC Car Editor - Phase 7 UI Changes

## Before Phase 7 (Original Layout)

```
┌──────────────────────────────────────────────────────────────────┐
│  AC Car Editor                                        [_][□][X]  │
├──────────────────────────────────────────────────────────────────┤
│  File    Tools    Help                                           │
├──────────────────┬───────────────────────────────────────────────┤
│                  │                                               │
│  ╔═════════════╗ │  ╔══════════════════════════════════════════╗│
│  ║ Cars        ║ │  ║ Car Information                          ║│
│  ╠═════════════╣ │  ╠══════════════════════════════════════════╣│
│  ║             ║ │  ║                                          ║│
│  ║  bmw_m3_e92 ║ │  ║  BMW M3 E92                              ║│
│  ║  ferrari_458║ │  ║  ════════════                            ║│
│  ║  porsche_911║ │  ║                                          ║│
│  ║  lambo_aven ║ │  ║  Folder: bmw_m3_e92                      ║│
│  ║  alfa_4c    ║ │  ║  Brand: BMW                              ║│
│  ║  ...        ║ │  ║  Has data folder: Yes                    ║│
│  ║  ...        ║ │  ║  Has data.acd: Yes                       ║│
│  ║  ...        ║ │  ║                                          ║│
│  ║  ...        ║ │  ║                                          ║│
│  ║             ║ │  ║                                          ║│
│  ║             ║ │  ║  [Edit Car]  [Create Backup]             ║│
│  ║             ║ │  ║                                          ║│
│  ╠═════════════╣ │  ╚══════════════════════════════════════════╝│
│  ║[Refresh    ]║ │                                               │
│  ╚═════════════╝ │                                               │
│                  │                                               │
└──────────────────┴───────────────────────────────────────────────┘
│  Ready                                                           │
└──────────────────────────────────────────────────────────────────┘
```

## After Phase 7 (New Features)

```
┌──────────────────────────────────────────────────────────────────┐
│  AC Car Editor                                        [_][□][X]  │
├──────────────────────────────────────────────────────────────────┤
│  File    Tools    Help                                           │
├──────────────────┬───────────────────────────────────────────────┤
│                  │                                               │
│  ╔═════════════╗ │  ╔══════════════════════════════════════════╗│
│  ║ Cars        ║ │  ║ Car Information                          ║│
│  ╠═════════════╣ │  ╠══════════════════════════════════════════╣│
│  ║ Search:     ║ │  ║                                          ║│
│  ║ [bmw___ ✕] ║ │  ║  BMW M3 E92                              ║│ <-- Car Name
│  ╠═════════════╣ │  ║  ════════════                            ║│
│  ║             ║ │  ║ ┌──────────────────────────────────────┐ ║│
│  ║  bmw_m3_e30 ║ │  ║ │                                      │ ║│
│  ║  bmw_m3_e92 ║ │  ║ │      [Preview Image]                 │ ║│ <-- NEW! Preview
│  ║             ║ │  ║ │      BMW M3 E92                      │ ║│     Image Display
│  ║             ║ │  ║ │                                      │ ║│
│  ║             ║ │  ║ └──────────────────────────────────────┘ ║│
│  ║             ║ │  ║                                          ║│
│  ║             ║ │  ║  Folder: bmw_m3_e92                      ║│
│  ║             ║ │  ║  Brand: BMW                              ║│
│  ║             ║ │  ║  Has data folder: Yes                    ║│
│  ╠═════════════╣ │  ║  Has data.acd: Yes                       ║│
│  ║[Refresh    ]║ │  ║                                          ║│
│  ╚═════════════╝ │  ║  [Edit Car]  [Create Backup]             ║│
│   ↑              │  ║                                          ║│
│   NEW! Search    │  ╚══════════════════════════════════════════╝│
│                  │                                               │
└──────────────────┴───────────────────────────────────────────────┘
│  Showing 2 of 50 cars                            ← NEW! Status  │
└──────────────────────────────────────────────────────────────────┘
```

## Key Changes Highlighted

### 1. Search Box (Left Panel - Top)
```
Before:  [No search capability]

After:   Search: [bmw_________ ✕]
         ↑                     ↑
         Search input          Clear button
```

**Features:**
- Real-time filtering as you type
- Case-insensitive matching
- Partial string search
- Clear button (✕) to reset

### 2. Preview Image (Right Panel - Center)
```
Before:  [No image display]

After:   ┌────────────────────┐
         │                    │
         │   [Car Preview]    │  ← Loads from ui/preview.png
         │                    │     or ui/preview.jpg
         └────────────────────┘
```

**Features:**
- Automatic image loading
- Scaled to fit (maintains aspect ratio)
- PNG preferred over JPG
- Fallback text for missing images

### 3. Status Bar (Bottom)
```
Before:  Ready

After:   Showing 2 of 50 cars  ← Shows filter results
```

## Example Workflow

### Scenario: Finding and Viewing a BMW
```
Step 1: Type "bmw" in search box
┌──────────────┐
│ Search: bmw  │  →  List filters to 2 cars:
└──────────────┘     - bmw_m3_e30
                     - bmw_m3_e92

Step 2: Click on "bmw_m3_e92"
┌────────────────────┐
│   BMW M3 E92       │
│ ┌────────────────┐ │
│ │   [E92 Image]  │ │  →  Preview loads automatically
│ └────────────────┘ │
│ Folder: bmw_m3_e92 │
│ Brand: BMW         │
└────────────────────┘

Step 3: Click ✕ to clear
┌──────────────┐
│ Search: ___  │  →  All 50 cars shown again
└──────────────┘     bmw_m3_e92 still selected
```

## Technical Implementation

### Search/Filter Algorithm
```python
# Pseudocode
if search_text is empty:
    show all_cars
else:
    filtered = [car for car in all_cars 
                if search_text.lower() in car.lower()]
    show filtered
    update status bar
```

### Preview Loading Logic
```python
# Pseudocode
preview_path = find_preview_in_ui_folder(car_name)
if preview_path exists:
    load image with QPixmap
    scale to fit with aspect ratio
    display in label
else:
    show "No preview image" text
```

---

**Implementation Date:** February 18, 2026  
**Status:** ✅ Complete and Tested  
**Tests:** 33/33 Passing (10 new + 23 existing)
