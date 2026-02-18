# AC Car Editor - Tools

This folder contains external tools used by the application.

## QuickBMS

**Purpose**: Unpacking Assetto Corsa data.acd files

**Files**:
- `quickbms/quickbms.exe` - QuickBMS executable
- `assetto_corsa_acd.bms` - AC data.acd extraction script

### About QuickBMS

QuickBMS is a generic file extractor/importer that uses special scripts to work with various file formats.

**Website**: http://aluigi.org/quickbms.htm
**License**: Freeware for personal/non-commercial use

### Usage in AC Car Editor

The application automatically uses quickBMS when:
1. User tries to edit a car with only a data.acd file (no unpacked data/ folder)
2. User confirms the unpacking prompt

**Command executed**:
```bash
quickbms.exe -o assetto_corsa_acd.bms <car_path>/data.acd <car_path>/data/
```

**Parameters**:
- `-o` - Overwrite existing files without prompting
- `assetto_corsa_acd.bms` - Script that handles AC file format
- First path - Input data.acd file
- Second path - Output folder where files are extracted

### AC Data.acd Format

The `assetto_corsa_acd.bms` script handles the special format used by Assetto Corsa for data.acd files:

1. **Key Generation**: Uses the car folder name to generate a decryption key
2. **File Structure**: data.acd contains a list of files with their sizes and encrypted content
3. **Decryption**: Each file is decrypted using ROT cipher with the generated key
4. **Extraction**: Decrypted files are written to the output folder with original names

**Important**: This only works for **non-encrypted** data.acd files. Kunos original cars use a different encryption method that cannot be unpacked.

### Manual Usage

If you want to manually unpack a data.acd file:

```bash
cd tools/quickbms
quickbms.exe -o ../assetto_corsa_acd.bms "C:\path\to\car\data.acd" "C:\path\to\car\data\"
```

Make sure to:
1. Run from the quickbms folder (or provide full path to quickbms.exe)
2. Provide full paths to both script and data.acd
3. Create the output folder first if it doesn't exist
4. The car folder name is important (used for key generation)

### Troubleshooting

**"quickbms.exe not found"**
- Make sure quickbms.exe is in `tools/quickbms/` folder
- Check that the file is actually named `quickbms.exe` (not `quickbms (1).exe` etc.)

**"assetto_corsa_acd.bms not found"**
- Make sure the script is in `tools/` folder (not in `tools/quickbms/`)
- Check that the file is named exactly `assetto_corsa_acd.bms`

**"Error unpacking data.acd"**
- The data.acd file might be encrypted (Kunos original cars)
- The data.acd file might be corrupted
- Try manually unpacking to see the error message

**Extraction produces no files**
- Check that you're unpacking from the correct car folder (name matters for key generation)
- Verify the data.acd is not encrypted

### Alternative: Manual Unpacking

Some community tools can also unpack data.acd files:
- Content Manager (CM) - Popular AC mod manager with built-in unpacker
- AC Car Tuner - Another car editing tool

However, this application uses quickBMS for:
- Lightweight (no need for full Content Manager installation)
- Scriptable (can be automated)
- Reliable (proven extraction method)

### Credits

- **QuickBMS**: Created by Luigi Auriemma (aluigi)
- **assetto_corsa_acd.bms**: AC modding community script
- Used with permission for personal/non-commercial use

### Legal Notice

QuickBMS is freeware for personal use. Commercial use requires permission from the author.

Assetto Corsa is © Kunos Simulazioni. This tool is for personal modding purposes only and does not distribute any Kunos Simulazioni content.
