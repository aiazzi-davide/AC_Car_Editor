# AC Car Editor

A desktop application for modifying Assetto Corsa car configurations.

## Features

- Browse and select Assetto Corsa cars
- View car information
- Create backups of car data
- Edit car parameters (coming soon):
  - Engine settings (power, torque, limiter, turbo)
  - Suspension settings
  - Differential settings
  - Weight and balance
  - Aerodynamics
  - Tire settings
- Component library system for pre-built configurations
- Visual curve editor for .lut files (coming soon)

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

4. Create a backup before making any modifications

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

### Implemented (Phase 1-4)
- ✅ Project structure and configuration
- ✅ INI file parser
- ✅ LUT file parser with curve support
- ✅ Car file manager
- ✅ Component library system
- ✅ Main window GUI
- ✅ Car browser and selection
- ✅ Backup system

### Coming Soon
- Car editor tabs (engine, suspension, etc.)
- Visual curve editor for .lut files
- Component library GUI manager
- Import/export functionality
- Advanced features (car comparison, undo/redo)

## License

This project is for educational purposes. Assetto Corsa is © Kunos Simulazioni.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
