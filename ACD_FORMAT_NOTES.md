# Assetto Corsa data.acd Format Notes

## Problem Discovery

Real Assetto Corsa data.acd files use a **custom binary format**, not standard ZIP format. This was discovered when testing with actual car data from the game.

### File Format Analysis

```bash
$ file examples/data.acd
examples/data.acd: data

$ head -c 50 examples/data.acd | od -A x -t x1z -v
000000 08 00 00 00 61 65 72 6f 2e 69 6e 69 cc 01 00 00  >....aero.ini....<
000010 93 00 00 00 79 00 00 00 72 00 00 00 76 00 00 00  >....y...r...v...<
000020 7d 00 00 00 72 00 00 00 84 00 00 00 8f 00 00 00  >}...r...........<
```

This is clearly NOT a ZIP file (which would start with `PK` magic bytes: `50 4B`).

## Format Types

### 1. ZIP Format (Rare)
- Some mod cars package data as standard ZIP files with .acd extension
- Can be extracted with Python's `zipfile` module
- Application can auto-unpack these

### 2. Custom Binary Format (Common)
- Most official AC cars and many mods use this format
- Cannot be extracted with standard ZIP tools
- Requires AC's own tools or Content Manager to unpack
- Application **cannot** auto-unpack these

## Solution Implemented

### Scenario 1: Car has BOTH data/ folder AND data.acd

**Old Behavior:**
- Tried to unpack data.acd (failed)
- Left data.acd in place
- AC would prioritize data.acd over data/ folder

**New Behavior:**
- Simply delete data.acd
- Keep existing data/ folder intact
- AC will use the unpacked data/ folder

**Code:**
```python
if car_info['has_data_folder']:
    # Just delete data.acd
    result = self.car_manager.delete_data_acd(self.current_car)
```

### Scenario 2: Car has ONLY data.acd (no data/ folder)

**Old Behavior:**
- Tried to unpack (failed for custom format)
- Generic error message

**New Behavior:**
- Try to unpack (will fail for custom format)
- Show clear message: "Custom binary format not supported"
- Suggest using AC's own tools to unpack first

**Code:**
```python
else:
    # Try to unpack
    result = self.car_manager.unpack_data_acd(...)
    if not result:
        # Show appropriate error message
```

## User Workflow

### For Cars with Both data/ and data.acd:
1. Select car in list
2. Click "Edit Car"
3. Application automatically deletes data.acd
4. Opens editor with data/ folder contents
5. ✅ Done!

### For Cars with Only data.acd (Custom Format):
1. Select car in list
2. Status shows: "may need manual unpacking"
3. Click "Edit Car"
4. If unpacking fails, shows message:
   - "Cannot unpack - custom binary format"
   - "Use AC's tools or Content Manager to unpack first"
5. User unpacks manually using Content Manager
6. Car now has data/ folder
7. Application can edit the car

## Technical Details

### delete_data_acd() Method

New method added to `CarFileManager`:

```python
def delete_data_acd(self, car_name: str) -> bool:
    """
    Delete data.acd file for a car.
    Useful when car has both data/ folder and data.acd.
    """
    acd_path = os.path.join(self.get_car_path(car_name), 'data.acd')
    
    if not os.path.exists(acd_path):
        return True  # Not an error
    
    try:
        os.remove(acd_path)
        return True
    except Exception as e:
        print(f"Error deleting data.acd: {e}")
        return False
```

### Detection Logic

The `is_acd_encrypted()` method checks for ZIP magic bytes:

```python
with open(acd_path, 'rb') as f:
    magic = f.read(2)
    if magic == b'PK':
        return (True, False)  # ZIP format
    else:
        return (True, True)   # Custom format (marked as "encrypted")
```

## Testing

Test with real AC data from `examples/` folder:

```python
# Scenario 1: Both data/ and data.acd exist
manager.delete_data_acd("car_name")
# ✓ data.acd deleted
# ✓ data/ folder preserved

# Scenario 2: Only data.acd (custom format)
result = manager.unpack_data_acd("car_name")
# ✓ Returns False (expected)
# ✓ Shows appropriate error message
```

## Future Enhancements

Possible improvements:

1. **Implement Custom Format Decoder**
   - Reverse-engineer AC's custom format
   - Implement unpacker in Python
   - Would allow auto-unpacking all files

2. **Integration with External Tools**
   - Detect Content Manager installation
   - Automatically invoke CM's unpacking tool
   - Seamless user experience

3. **Format Documentation**
   - Document the custom format structure
   - Share with AC modding community
   - Enable third-party tool development

## References

- Assetto Corsa uses custom ACD format for official content
- Content Manager (by x4fab) can unpack these files
- Some tools exist for unpacking, but require external dependencies
- ZIP format is only used by some mod creators for convenience
