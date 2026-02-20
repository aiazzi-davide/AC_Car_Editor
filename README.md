# AC Car Editor

A desktop application for modifying Assetto Corsa car configurations.

## Features

- Browse and select Assetto Corsa cars
- **Search and filter cars** by name
- **Preview car images** from ui/preview.png or preview.jpg
- View car information
- Create backups of car data
- **Automatic unpacking of data.acd files** using quickBMS
- **Automatic data.acd deletion after editing** to ensure changes are used in-game
- **UI Metadata Editor** - Edit car name, brand, description, tags, specs, and author info in ui_car.json
- **Stage Tuning System** - One-click performance upgrades (Stage 1/2/3) with different logic for NA vs Turbo cars
  - **NA Stage 1**: More aggressive ECU mapping (+8% power)
  - **NA Stage 2**: Add turbo system (turbo conversion)
  - **NA Stage 3**: Full turbo build with mechanical and aero upgrades
  - **Turbo Stage 1**: ECU remap (+15% boost)
  - **Turbo Stage 2**: Turbo upgrade (+30% boost)
  - **Turbo Stage 3**: Full build (+50% boost, mechanical, aero, differential upgrades)
- Edit car parameters:
  - **Engine settings** (RPM limits, limiter frequency, turbo boost, wastegate, engine damage thresholds)
  - **Power and coast curves** (visual curve editor for .lut files)
  - **Power/Torque Calculator** – real-time chart of power (HP, derived) and torque (Nm) with turbo boost effect
  - **Suspension settings** (spring rates, dampers, rod length)
  - **Drivetrain settings** (differential, gearbox, clutch, AWD/AWD2 support)
    - **Gear Ratio Editor**: Individual gear ratio editing (R, 1-10) with collapsible UI 
    - **Gear Ratio Presets**: Import from library (4 presets: Street 5-speed, Sport 6-speed, Race 6-speed, Drift 6-speed) 
    - **Speed Estimation**: Real-time max speed calculation for each gear (based on RPM, tire radius, ratios)
    - **RTO File Manager**: Edit final.rto and ratios.rto for in-game selectable gear ratios 
      - Import RTO presets from library (3 final ratio sets, 3 gear ratio sets)
      - Speed estimation for alternative ratios
  - **Weight and balance** (total mass, center of gravity, fuel) 
  - **Aerodynamics** (drag coefficient, downforce, wing angles) 
  - **Brakes** (max torque, bias, handbrake, adjust step) 
  - **Tyres (Pneumatici)** (compound selection, dimensions, grip, pressure) 
    - **Tire Presets**: Import from library (6 presets: Street, Sport, Semi-Slick, Soft/Medium/Hard Slicks) 
- **Setup Manager** for track-specific presets (save/load/delete per-track setups) 
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

5. Edit UI Metadata (optional):
   - Select a car and click "Edit UI" button
   - Modify car name, brand, class, country, year
   - Edit description (supports HTML tags like `<br>` for line breaks)
   - Add/edit tags for filtering (comma-separated)
   - Update specs (power, torque, weight, top speed, acceleration, power/weight ratio)
   - Set author name and version
   - Changes are saved to ui/ui_car.json with automatic backup

6. Edit a car:
   - Select a car (with or without unpacked data folder)
   - **If car has only data.acd**: Application will prompt to unpack it using quickBMS
   - Click "Edit Car" to open the editor
   - Use the tabs to navigate different aspects:
     - **Engine**: Modify RPM limits, turbo settings, and edit power/coast curves
       - Click "Edit Power Curve" to open the visual curve editor for power.lut
       - Click "Edit Coast Curve" to open the visual curve editor for coast.lut
       - Click "⚡ Power / Torque Calculator" to see real-time power and torque curves (with turbo effect)
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
   - Click "🚀 Stage Tuning" for one-click performance upgrades:
     - **Stage 1**: Light tuning (NA: +8% power, Turbo: +15% boost)
     - **Stage 2**: Moderate tuning (NA: add turbo, Turbo: +30% boost)
     - **Stage 3**: Full build (NA/Turbo: major boost/power + weight reduction + aero + mechanical upgrades)
     - Automatic detection of NA vs turbocharged engines
     - Backup creation for all modifications
  - Click "↩ Restore Backup" to undo the last save: restores all `.bak` files back to the originals, removes the `.bak` files, and reloads the editor
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
  - **Power and coast curve editor**: Visual matplotlib-based editor for .lut files (power.lut stores Nm torque)
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
  - Real-time preview with axis labels (RPM vs Nm, etc.)
- ✅ **Power/Torque Calculator** (Phase 7)
  - Torque (Nm) and derived HP curves from power.lut
  - Turbo boost effect visualization (NA vs turbo comparison)
  - Peak power/torque statistics
- ✅ **Setup Manager** (Phase 7)
  - Read and display setup.ini parameters grouped by tab
  - Save/load/delete track-specific setup presets as JSON
  - Preset management UI with parameter editing
- ✅ **UI Metadata Editor** (Phase 7)
  - Edit ui_car.json: car name, brand, class, country, year
  - Edit description with HTML support
  - Manage tags for filtering
  - Update specs (power, torque, weight, top speed, acceleration, power/weight)
  - Set author and version information
  - Automatic backup creation
- ✅ **Stage Tuning System** (Phase 7)
  - One-click performance upgrades (Stage 1/2/3)
  - Automatic detection of NA vs turbocharged engines
  - Different tuning logic for NA and turbo cars
  - Stage 1: Light tuning (power/boost increase)
  - Stage 2: Moderate tuning (NA: turbo conversion, Turbo: more boost)
  - Stage 3: Full build (power, weight, aero, mechanical, differential upgrades)
  - Stage marker tracking in engine.ini
  - Reset to stock functionality

### Coming Soon
- Generic LUT editor for all curve types (traction_control.lut, throttle.lut, etc.)
- Smooth curve interpolation (spline)
- Sound engine investigation (bank files, GUIDs)

## License

This project is for educational purposes. Assetto Corsa is © Kunos Simulazioni.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
