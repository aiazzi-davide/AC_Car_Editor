# Tools Folder

This folder contains external tools required for unpacking Assetto Corsa data.acd files.

## quickBMS

QuickBMS is a generic file extractor that can handle many game archive formats.

**Folder:** `quickbms/`

**Files:**
- `quickbms.exe` - Main executable (for files < 4GB)
- `quickbms_4gb_files.exe` - Version for files >= 4GB
- `quickbms.txt` - Documentation
- Other batch files for reimporting

**Usage:**
The application automatically uses quickBMS when you try to edit a car with a packed data.acd file.

**Manual Usage:**
```cmd
quickbms.exe assetto_corsa_acd.bms input.acd output_folder
```

**Website:** http://aluigi.altervista.org/quickbms.htm

## assetto_corsa_acd.bms

**File:** `assetto_corsa_acd.bms`

This is the BMS script that tells quickBMS how to extract Assetto Corsa's data.acd files.

**How it works:**
1. Generates a decryption key based on the car folder name
2. Reads the data.acd file structure
3. Decrypts and extracts all files to the output folder

**Important:** This script only works with non-encrypted data.acd files. Some mod cars use encrypted archives that cannot be unpacked.

## Automatic Detection

The AC Car Editor automatically finds these tools using the following search paths:

1. `tools/quickbms/quickbms.exe`
2. `tools/quickbms/quickbms_4gb_files.exe`
3. `tools/assetto_corsa_acd.bms`

No manual configuration is needed - just keep the tools in this folder structure.

## Platform Requirements

- **Windows:** quickBMS executables work natively
- **Linux/Mac:** quickBMS is Windows-only, cannot be used (wine not supported)

On non-Windows platforms, you'll need to manually extract data.acd files on a Windows machine.

## Credits

- quickBMS by Luigi Auriemma (aluigi)
- assetto_corsa_acd.bms script by the Assetto Corsa modding community
