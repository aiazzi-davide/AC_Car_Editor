# AC Car Editor

A desktop application for modifying Assetto Corsa car configurations.

## Features

- Browse and select Assetto Corsa cars
- **Search and filter cars** by name ✅
- **Preview car images** from ui/preview.png or preview.jpg ✅
- View car information
- Create backups of car data
- **Automatic unpacking of data.acd files** using quickBMS ✅
- **Automatic data.acd deletion after editing** to ensure changes are used in-game ✅
- Edit car parameters:
  - **Engine settings** (RPM limits, limiter frequency, turbo boost, wastegate, engine damage thresholds) ✅
  - **Power and coast curves** (visual curve editor for .lut files) ✅
  - **Power/Torque Calculator** – real-time chart of HP and Nm with turbo boost effect ✅
  - **Suspension settings** (spring rates, dampers, rod length) ✅
  - **Drivetrain settings** (differential, gearbox, clutch, AWD/AWD2 support) ✅
  - **Weight and balance** (total mass, center of gravity, fuel) ✅
  - **Aerodynamics** (drag coefficient, downforce, wing angles) ✅
  - **Brakes** (max torque, bias, handbrake, adjust step) ✅
  - **Tyres (Pneumatici)** (compound selection, dimensions, grip, pressure) ✅
- **Setup Manager** for track-specific presets (save/load/delete per-track setups) ✅
- **Visual curve editor** for power.lut and coast.lut files:
  - Interactive matplotlib-based graph editor
  - Integer-only values for precise car tuning
  - Drag-and-drop point editing (graph stays fixed during drag)
  - Add/remove points with form input or keyboard (Delete key)
  - Mouse wheel zoom (centered on cursor) + keyboard shortcuts (+/-)
  - Simplified toolbar (Home, Back, Forward, Save)
  - Side-by-side graph and table view
  - Preset curves (Linear, Turbo Lag, NA, V-Shape Coast)
  - Export curves to other files
  - Automatic backup creation
- Component library system for pre-built configurations

## Requirements

- Python 3.x
- PyQt5
- Assetto Corsa installed
- quickBMS (included in `tools/` folder for unpacking data.acd files)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/aiazzi-davide/AC_Car_Editor.git
cd AC_Car_Editor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. On first run, set your Assetto Corsa installation path:
   - Go to File > Set AC Path...
   - Navigate to your Assetto Corsa installation folder
   - Default: `C:\Program Files (x86)\Steam\steamapps\common\assettocorsa`

3. Browse and filter cars:
   - All installed cars are shown in the left panel
   - Use the search box to filter cars by name (case-insensitive)
   - Click the ✕ button to clear the filter
   - Select a car to view its information and preview image

4. Select a car from the list to view its information
   - Car preview image is displayed (if available in ui/preview.png or preview.jpg)
   - Car details are shown below the preview

5. Edit a car:
   - Select a car (with or without unpacked data folder)
   - **If car has only data.acd**: Application will prompt to unpack it using quickBMS
   - Click "Edit Car" to open the editor
   - Use the tabs to navigate different aspects:
     - **Engine**: Modify RPM limits, turbo settings, and edit power/coast curves
       - Click "Edit Power Curve" to open the visual curve editor for power.lut
       - Click "Edit Coast Curve" to open the visual curve editor for coast.lut
       - Click "⚡ Power / Torque Calculator" to see real-time HP and Nm curves (with turbo effect)
       - In the curve editor:
         - Drag points to adjust curve shape (graph stays fixed)
         - Add points using the form (integer X/Y values) at the bottom right
         - Remove points by selecting them and pressing Delete or clicking "Remove Point"
         - Zoom with mouse wheel (centered on cursor) or +/- keyboard keys
         - Use toolbar buttons: Home (reset view), Back, Forward, Save
         - Load preset curves from the dropdown menu
         - Export curves to other .lut files
         - Save changes (automatically creates a .bak backup)
     - **Suspension**: Adjust spring rates, damper settings for front and rear
     - **Drivetrain**: Configure differential power, coast, and preload, select traction type (RWD/FWD/AWD/AWD2)
     - **Weight & Fuel**: Set total mass, center of gravity position, and fuel tank capacity
     - **Aerodynamics**: Adjust drag coefficient, downforce settings, and wing configurations
     - **Brakes**: Set maximum brake torque, brake bias, handbrake torque
     - **Pneumatici (Tyres)**: Select compound, adjust tyre dimensions (width, radius), grip coefficients (DX0/DY0), and ideal pressure
   - Click "🔧 Setup Manager" to manage track-specific setup presets (save/load/delete)
   - Click "Open Folder" to open the car's data folder in your system file explorer
   - Click "Save Changes" to apply modifications
   - A backup file (.bak) is automatically created for each modified file
   - **After editing**: Application prompts to delete data.acd to ensure changes are used in-game

6. Create additional backups using the "Create Backup" button

## Data.acd Unpacking

The application automatically handles unpacking of non-encrypted data.acd files:

1. **Before editing**: If a car has only a data.acd file (no unpacked data/ folder), the application prompts to unpack it
2. **Unpacking process**: Uses quickBMS to extract all files to the data/ folder
3. **After editing**: Prompts to delete data.acd to ensure Assetto Corsa uses the modified files

**Why delete data.acd?** Assetto Corsa prioritizes data.acd over the unpacked data/ folder. If data.acd exists, any changes made to files in data/ will be ignored in-game.

See `DATA_ACD_UNPACKING.md` for detailed documentation.

## File Structure

```
AC_Car_Editor/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── tools/                  # External tools
│   ├── quickbms/          # quickBMS for unpacking
│   │   └── quickbms.exe
│   └── assetto_corsa_acd.bms  # Unpacking script
├── src/
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration manager
│   │   ├── car_file_manager.py  # Car file handling
│   │   ├── ini_parser.py  # INI file parser
│   │   ├── lut_parser.py  # LUT file parser
│   │   ├── power_calculator.py  # Power/torque calculator
│   │   ├── setup_manager.py     # Track setup manager
│   │   └── component_library.py  # Component library
│   ├── gui/               # GUI components
│   │   └── main_window.py # Main window
│   └── components/        # Component library data
└── backups/               # Backup storage (created automatically)
```

## Notes

### Assetto Corsa File Structure

The application works with unpacked car data folders. Each car has the following structure:

```
assettocorsa/content/cars/
├── [car_name]/
│   ├── data/              # Unpacked data folder (required)
│   │   ├── engine.ini     # Engine configuration
│   │   ├── suspensions.ini # Suspension configuration
│   │   ├── tyres.ini      # Tire configuration
│   │   ├── drivetrain.ini # Drivetrain configuration
│   │   ├── car.ini        # Car basic info
│   │   └── *.lut          # Lookup tables (curves)
│   └── ui/                # UI resources
```

### Important

- Always create a backup before modifying any car
- Cars with `data.acd` files will be automatically unpacked on first edit
- After editing, delete data.acd when prompted (or AC will ignore your changes)
- Encrypted `data.acd` files from Kunos cars cannot be unpacked
- The application does not modify the original game files until you save changes

## Development Status

### Implemented (Phase 1-7 partial)
- ✅ Project structure and configuration
- ✅ INI file parser
- ✅ LUT file parser with curve support
- ✅ Car file manager
- ✅ **Data.acd unpacking with quickBMS**
- ✅ **Automatic data.acd deletion after editing**
- ✅ **Car search and filter** (Phase 7)
- ✅ **Car preview images** (Phase 7)
- ✅ Component library system
- ✅ Main window GUI
- ✅ Car browser and selection
- ✅ Backup system
- ✅ **Car editor dialog with multiple tabs**
  - **Engine tab**: RPM settings (minimum, maximum, limiter, limiter frequency), turbo settings (max boost, wastegate, default adjustment), engine damage thresholds
  - **Power and coast curve editor**: Visual matplotlib-based editor for .lut files (power.lut uses HP, not kW)
  - **Suspension tab**: Front and rear suspension settings (spring rate, damper fast/slow bump/rebound, rod length, camber, toe)
  - **Drivetrain tab**: Traction type (RWD/FWD/AWD/AWD2), differential settings (power, coast, preload), gearbox, clutch
  - **Weight & Fuel tab**: Total mass, inertia, center of gravity, steering, fuel settings
  - **Aerodynamics tab**: Dynamic wing sections with drag/lift coefficients and angles
  - **Brakes tab**: Max torque, front bias, handbrake, cockpit adjustable settings with adjust step
  - Automatic backup creation before saving
  - Reset functionality to restore original values
- ✅ **Visual curve editor for .lut files**
  - Interactive matplotlib graph with zoom/pan
  - Drag-and-drop point editing
  - Add/remove points via mouse, keyboard, or form
  - Side-by-side graph and table view
  - Preset curves (Linear, Turbo Lag, NA, V-Shape Coast)
  - Import/export functionality
  - Real-time preview with axis labels (RPM vs HP, etc.)
- ✅ **Power/Torque Calculator** (Phase 7)
  - Real-time HP and Nm curves from power.lut
  - Turbo boost effect visualization (NA vs turbo comparison)
  - Peak power/torque statistics
- ✅ **Setup Manager** (Phase 7)
  - Read and display setup.ini parameters grouped by tab
  - Save/load/delete track-specific setup presets as JSON
  - Preset management UI with parameter editing

### Coming Soon
- Undo/redo system
- UI folder modifications (car name in menus, icons)
- Generic LUT editor for all curve types
- Smooth curve interpolation (spline)

## License

This project is for educational purposes. Assetto Corsa is © Kunos Simulazioni.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
