# AC Car Editor

A desktop application for modifying Assetto Corsa car configurations.

## Features

- Browse and select Assetto Corsa cars
- View car information
- Create backups of car data
- Edit car parameters:
  - **Engine settings** (RPM limits, turbo boost, wastegate) ✅
  - **Power and coast curves** (visual curve editor for .lut files) ✅
  - **Suspension settings** (spring rates, dampers, rod length) ✅
  - **Differential settings** (power, coast, preload) ✅
  - **Weight and balance** (total mass, center of gravity) ✅
  - **Aerodynamics** (drag coefficient, downforce) ✅
  - Tire settings (coming soon)
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
- Assetto Corsa installed with unpacked car data folders

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

3. Select a car from the list to view its information

4. Edit a car:
   - Select a car with an unpacked data folder
   - Click "Edit Car" to open the editor
   - Use the tabs to navigate different aspects:
     - **Engine**: Modify RPM limits, turbo settings, and edit power/coast curves
       - Click "Edit Power Curve" to open the visual curve editor for power.lut
       - Click "Edit Coast Curve" to open the visual curve editor for coast.lut
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
     - **Differential**: Configure differential power, coast, and preload
     - **Weight**: Set total mass and center of gravity position
     - **Aerodynamics**: Adjust drag coefficient and downforce settings
   - Click "Save Changes" to apply modifications
   - A backup file (.bak) is automatically created for each modified file

5. Create additional backups using the "Create Backup" button

## File Structure

```
AC_Car_Editor/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration manager
│   │   ├── car_file_manager.py  # Car file handling
│   │   ├── ini_parser.py  # INI file parser
│   │   ├── lut_parser.py  # LUT file parser
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
- Only cars with unpacked `data` folders can be edited
- Encrypted `data.acd` files are not supported yet
- The application does not modify the original game files until you save changes

## Development Status

### Implemented (Phase 1-6.5)
- ✅ Project structure and configuration
- ✅ INI file parser
- ✅ LUT file parser with curve support
- ✅ Car file manager
- ✅ Component library system
- ✅ Main window GUI
- ✅ Car browser and selection
- ✅ Backup system
- ✅ **Car editor dialog with multiple tabs**
  - **Engine tab**: RPM settings (minimum, maximum, limiter) and turbo settings (max boost, wastegate)
  - **Power and coast curve editor**: Visual matplotlib-based editor for .lut files
  - **Suspension tab**: Front and rear suspension settings (spring rate, damper fast/slow bump/rebound, rod length)
  - **Differential tab**: Traction type display and differential settings (power, coast, preload)
  - **Weight tab**: Total mass and center of gravity location (X, Y, Z coordinates)
  - **Aerodynamics tab**: Drag coefficient, front and rear downforce settings (lift coefficient, CL gain)
  - Automatic backup creation before saving
  - Reset functionality to restore original values
- ✅ **Visual curve editor for .lut files**
  - Interactive matplotlib graph with zoom/pan
  - Drag-and-drop point editing
  - Add/remove points via mouse, keyboard, or form
  - Side-by-side graph and table view
  - Preset curves (Linear, Turbo Lag, NA, V-Shape Coast)
  - Import/export functionality
  - Real-time preview with axis labels (RPM vs kW, etc.)

### Coming Soon
- Tire settings tab
- Component library GUI manager
- Import/export functionality for complete car setups
- Advanced features (car comparison, undo/redo)

## License

This project is for educational purposes. Assetto Corsa is © Kunos Simulazioni.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
