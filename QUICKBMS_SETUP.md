# QuickBMS Setup Guide for AC Car Editor

## What is QuickBMS?

QuickBMS is a universal file extractor tool that can unpack many game file formats, including Assetto Corsa's custom data.acd format. The AC Car Editor can use QuickBMS to automatically unpack data.acd files that are in AC's custom format (not ZIP).

## Why Do I Need It?

Many Assetto Corsa cars use a custom binary format for their data.acd files. This format cannot be unpacked with standard ZIP tools. QuickBMS, combined with the correct script, can extract these files so you can edit them.

**You need QuickBMS if:**
- You want to edit cars that only have data.acd (no data/ folder)
- The data.acd file is not a standard ZIP file
- You see an error message about "custom format" when trying to edit a car

## Installation

### Step 1: Download QuickBMS

1. Go to: http://aluigi.altervista.org/quickbms.htm
2. Download the appropriate version:
   - **Windows**: Download "quickbms.exe" (or "quickbms_4gb_files.exe" for large files)
   - **Linux/Mac**: Download the appropriate version for your system

### Step 2: Download the AC Unpacker Script

The AC Car Editor includes an `acd.bms` script in its main folder. If you don't have it:

1. It should be in the same folder as the application
2. The file is named `acd.bms`

Alternatively, you can find AC unpacker scripts online in the QuickBMS script collection.

### Step 3: Place Files

**Option A: In the Application Folder (Recommended)**
```
AC_Car_Editor/
├── main.py
├── quickbms.exe (or quickbms)
├── acd.bms
└── ...
```

**Option B: In a Tools Subfolder**
```
AC_Car_Editor/
├── main.py
├── tools/
│   ├── quickbms.exe
│   └── acd.bms
└── ...
```

**Option C: System-wide Installation**
- Place quickbms.exe in a folder that's in your system PATH
- Place acd.bms in the same folder or in the application folder

## How It Works

1. When you click "Edit Car" on a car with only data.acd:
2. The app first tries to unpack it as a ZIP file
3. If that fails (custom format), it looks for QuickBMS
4. If QuickBMS is found, it uses it to unpack the data.acd
5. The unpacked files go into a new data/ folder
6. You can then edit the car normally

## Configuration

### Manual Path Configuration

If QuickBMS is installed in a custom location, you can configure it:

1. Open the application
2. Go to File > Settings (if available)
3. Set the path to your QuickBMS executable

Or edit `config.json` directly:
```json
{
  "ac_path": "...",
  "quickbms_path": "C:/path/to/quickbms.exe"
}
```

## Troubleshooting

### "QuickBMS not found"

**Solution:**
- Make sure quickbms.exe is in one of the searched locations
- Check the filename is exactly "quickbms.exe" (or "quickbms" on Linux)
- Try placing it directly in the AC_Car_Editor folder

### "AC data.acd unpacker script (acd.bms) not found"

**Solution:**
- Make sure acd.bms is in the application folder
- Check the filename is exactly "acd.bms"
- Verify the file is not empty

### "QuickBMS failed with return code 1"

**Possible causes:**
- The data.acd file might be corrupted
- The BMS script might not be compatible with this specific data.acd version
- Try using Content Manager to unpack the car instead

### Permission Errors

**Solution:**
- Run the application as administrator (Windows)
- Check file permissions on the quickbms executable
- Make sure the car folder is writable

## Alternative: Content Manager

If you have Assetto Corsa Content Manager installed, you can use it to unpack cars:

1. Open Content Manager
2. Go to Content > Cars
3. Right-click the car
4. Select "Unpack data" or similar option
5. After unpacking, use AC Car Editor to edit the car

## Security Note

QuickBMS is a legitimate tool used by many game modders. However:
- Only download from the official site: http://aluigi.altervista.org/quickbms.htm
- Scan downloads with antivirus if concerned
- The tool needs to execute, so some antivirus software may flag it

## Technical Details

### How the Unpacker Works

The AC data.acd format is a simple archive format:
```
[Number of files: 4 bytes]
For each file:
  [Filename length: 4 bytes]
  [Filename: variable]
  [File offset: 4 bytes]
  [File size: 4 bytes]
[File data...]
```

The acd.bms script tells QuickBMS how to parse this format and extract the files.

### File Locations Searched

The application searches for QuickBMS in:
1. Current directory
2. tools/ subfolder
3. quickbms/ subfolder
4. User's home directory
5. System PATH directories
6. Configured custom path (if set)

### BMS Script Locations Searched

The application searches for acd.bms in:
1. Current directory
2. tools/ subfolder
3. scripts/ subfolder
4. quickbms/ subfolder
5. User's home directory

## Support

If you encounter issues:
1. Check this guide carefully
2. Verify QuickBMS works standalone: `quickbms acd.bms data.acd output_folder`
3. Check the application console output for detailed error messages
4. Try unpacking with Content Manager as an alternative
