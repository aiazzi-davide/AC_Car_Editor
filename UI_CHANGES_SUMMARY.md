# UI Changes Summary - Automatic ACD Unpacking

## Before (Previous Version)

### Car Info Panel
```
Action Buttons:
┌────────────┐ ┌───────────────┐ ┌──────────────────┐
│  Edit Car  │ │ Create Backup │ │ Unpack data.acd  │
└────────────┘ └───────────────┘ └──────────────────┘

Status: "Car has no data folder. Use 'Unpack data.acd' to extract files."
```

### Workflow
1. Select car with data.acd
2. Click "Unpack data.acd" button
3. Wait for unpacking
4. Click "Edit Car" button
5. Edit car parameters

**Issues:**
- Two-step process (unpack, then edit)
- Confusing for users (which button to click first?)
- data.acd remained after unpacking (AC would ignore unpacked folder)
- Encryption detection could prevent unpacking even if it would work

## After (Current Version)

### Car Info Panel
```
Action Buttons:
┌────────────┐ ┌───────────────┐
│  Edit Car  │ │ Create Backup │
└────────────┘ └───────────────┘

Status: "Car has data.acd - will auto-unpack when you click 'Edit Car'"
```

### Workflow
1. Select car with data.acd
2. Click "Edit Car" button
3. **Automatic unpacking happens** (with status message)
4. Edit car parameters

**Benefits:**
- One-click process (just edit)
- Simpler UI (one less button)
- Clear status messages explain what will happen
- data.acd is deleted after unpacking (correct AC behavior)
- Attempts to unpack all data.acd files

## Key Differences

### Button Changes
| Before | After |
|--------|-------|
| 3 buttons | 2 buttons |
| Separate unpack button | Removed |
| Edit only for unpacked cars | Edit for cars with data.acd too |

### Status Messages
| Before | After |
|--------|-------|
| "Use 'Unpack data.acd' to extract" | "will auto-unpack when you click 'Edit Car'" |
| "Encrypted (not supported)" | "Encrypted (will auto-unpack on edit)" |
| "Unencrypted (can unpack)" | "Unencrypted (will auto-unpack on edit)" |

### User Experience
| Before | After |
|--------|-------|
| 2 clicks needed | 1 click needed |
| Must understand unpacking | Automatic |
| data.acd remains | data.acd deleted |
| Encryption blocks unpacking | Attempts all files |

## Status Bar Messages During Editing

```
1. "Unpacking data.acd for 'car_name'..."
2. "Successfully unpacked data.acd for 'car_name'"
   OR
   "Failed to unpack - Do you want to try editing anyway?"
3. Opens car editor dialog
4. After closing: Info refreshed automatically
```

## Car Details Display

### Before
```
Folder: car_name
Brand: Brand Name
Has data folder: No
Has data.acd: Yes
data.acd: Encrypted (not supported)
```

### After
```
Folder: car_name
Brand: Brand Name
Has data folder: No
Has data.acd: Yes
data.acd: Encrypted (will auto-unpack on edit)
```

## Implementation Details

The UI changes are minimal but significantly improve the user experience:
- Removed 4 lines of button creation code
- Simplified car selection logic (30 lines → 20 lines)
- Enhanced edit_car method with auto-unpacking (5 lines → 35 lines)
- Net result: Simpler, more intuitive, and matches AC's expected behavior
