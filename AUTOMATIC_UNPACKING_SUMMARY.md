# Automatic ACD Unpacking - Implementation Summary

## Problem Statement
The user reported that:
1. The unpack button wasn't available for any cars (detection system may be wrong)
2. In Assetto Corsa, you can unpack even encrypted data.acd files (they just won't be readable)
3. Instead of a separate unpack button, unpacking should happen automatically when clicking "Edit Car"
4. After unpacking, data.acd must be deleted so AC uses the unpacked folder

## Solution Implemented

### Core Changes

#### 1. CarFileManager.unpack_data_acd()
- **Removed** encryption detection requirement
- **Added** `delete_acd` parameter to delete data.acd after successful unpacking
- Now attempts to unpack all data.acd files regardless of encryption status
- After successful unpacking, deletes data.acd if `delete_acd=True`

```python
def unpack_data_acd(self, car_name: str, backup_existing: bool = True, delete_acd: bool = False) -> bool:
    # Attempts unpacking without encryption check
    # Deletes data.acd after successful unpack if delete_acd=True
```

#### 2. MainWindow.edit_car()
- **Added** automatic unpacking before opening editor
- If car has data.acd, it's unpacked with `delete_acd=True`
- Shows clear status messages during unpacking
- Offers to continue editing if unpacking fails
- Refreshes car info after editing

#### 3. UI Changes
- **Removed** "Unpack data.acd" button
- **Updated** Edit button to enable for cars with data.acd files
- **Simplified** car selection logic
- Updated status messages to indicate auto-unpacking

### Behavior Flow

1. User selects a car with data.acd
2. Edit button is enabled (whether or not data folder exists)
3. User clicks "Edit Car"
4. Application automatically:
   - Checks if data.acd exists
   - Creates backup of existing data folder (if any)
   - Unpacks data.acd to data/ folder
   - **Deletes data.acd file**
   - Opens car editor
5. After editing, car info is refreshed

### Key Features

✅ **Automatic**: No manual unpacking needed
✅ **Safe**: Creates backup before unpacking
✅ **Clean**: Deletes data.acd so AC uses unpacked folder
✅ **Robust**: Handles failures gracefully
✅ **User-friendly**: Clear status messages

## Testing

### New Test Added
`test_unpack_data_acd_with_delete()` - Verifies data.acd is deleted after unpacking

### Test Results
- All 40 tests passing
- No security vulnerabilities
- Verified automatic unpacking works correctly
- Verified data.acd deletion

## Files Modified

1. `src/core/car_file_manager.py` - Updated unpack_data_acd method
2. `src/gui/main_window.py` - Removed unpack button, added auto-unpack to edit_car
3. `tests/test_core.py` - Added test for deletion functionality
4. `README.md` - Updated documentation

## Benefits

1. **Simpler workflow**: One click to edit instead of two
2. **Correct AC behavior**: Deleting data.acd ensures AC uses unpacked folder
3. **More flexible**: Attempts to unpack all data.acd files
4. **Better UX**: Clear feedback and error handling
5. **Cleaner UI**: One less button to confuse users

## Migration Notes

For existing users:
- No action needed - unpacking happens automatically
- data.acd files will be deleted after first edit
- Backups are created automatically before unpacking
- Edit button now works for cars with only data.acd

## Implementation Date
February 17, 2026
