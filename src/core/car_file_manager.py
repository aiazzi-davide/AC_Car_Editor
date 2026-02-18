"""
Car File Manager for handling Assetto Corsa car files and folders
"""

import os
import shutil
import zipfile
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime


class CarFileManager:
    """Manages Assetto Corsa car files and folders"""
    
    def __init__(self, cars_path: str, config_manager=None):
        """
        Initialize car file manager
        
        Args:
            cars_path: Path to AC cars folder
            config_manager: Optional ConfigManager instance for accessing QuickBMS path
        """
        self.cars_path = cars_path
        self.config_manager = config_manager
    
    def get_car_list(self) -> List[str]:
        """
        Get list of all car folders
        
        Returns:
            List of car folder names
        """
        if not os.path.exists(self.cars_path):
            return []
        
        cars = []
        try:
            for item in os.listdir(self.cars_path):
                car_path = os.path.join(self.cars_path, item)
                if os.path.isdir(car_path):
                    cars.append(item)
        except Exception as e:
            print(f"Error listing cars: {e}")
        
        return sorted(cars)
    
    def get_car_path(self, car_name: str) -> str:
        """
        Get full path to car folder
        
        Args:
            car_name: Car folder name
            
        Returns:
            Full path to car folder
        """
        return os.path.join(self.cars_path, car_name)
    
    def get_car_data_path(self, car_name: str) -> str:
        """
        Get path to car data folder
        
        Args:
            car_name: Car folder name
            
        Returns:
            Full path to data folder
        """
        return os.path.join(self.get_car_path(car_name), 'data')
    
    def has_data_folder(self, car_name: str) -> bool:
        """
        Check if car has unpacked data folder
        
        Args:
            car_name: Car folder name
            
        Returns:
            True if data folder exists
        """
        data_path = self.get_car_data_path(car_name)
        return os.path.exists(data_path) and os.path.isdir(data_path)
    
    def has_data_acd(self, car_name: str) -> bool:
        """
        Check if car has data.acd file
        
        Args:
            car_name: Car folder name
            
        Returns:
            True if data.acd exists
        """
        acd_path = os.path.join(self.get_car_path(car_name), 'data.acd')
        return os.path.exists(acd_path)
    
    def get_car_info(self, car_name: str) -> Dict[str, Any]:
        """
        Get basic car information
        
        Args:
            car_name: Car folder name
            
        Returns:
            Dictionary with car info
        """
        info = {
            'name': car_name,
            'has_data_folder': self.has_data_folder(car_name),
            'has_data_acd': self.has_data_acd(car_name),
            'display_name': car_name,
            'brand': '',
        }
        
        # Try to get display name from ui_car.json
        ui_path = os.path.join(self.get_car_path(car_name), 'ui', 'ui_car.json')
        if os.path.exists(ui_path):
            try:
                import json
                with open(ui_path, 'r', encoding='utf-8') as f:
                    ui_data = json.load(f)
                    info['display_name'] = ui_data.get('name', car_name)
                    info['brand'] = ui_data.get('brand', '')
            except Exception as e:
                print(f"Error reading ui_car.json: {e}")
        
        return info
    
    def create_backup(self, car_name: str, backup_dir: str = 'backups') -> Optional[str]:
        """
        Create backup of car data folder
        
        Args:
            car_name: Car folder name
            backup_dir: Backup directory path
            
        Returns:
            Path to backup folder or None on error
        """
        if not self.has_data_folder(car_name):
            print(f"Car {car_name} has no data folder to backup")
            return None
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create timestamped backup folder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{car_name}_{timestamp}"
        backup_path = os.path.join(backup_dir, backup_name)
        
        try:
            data_path = self.get_car_data_path(car_name)
            shutil.copytree(data_path, backup_path)
            print(f"Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
    
    def restore_backup(self, car_name: str, backup_path: str) -> bool:
        """
        Restore car data from backup
        
        Args:
            car_name: Car folder name
            backup_path: Path to backup folder
            
        Returns:
            True if successful
        """
        if not os.path.exists(backup_path):
            print(f"Backup path does not exist: {backup_path}")
            return False
        
        data_path = self.get_car_data_path(car_name)
        
        try:
            # Remove existing data folder
            if os.path.exists(data_path):
                shutil.rmtree(data_path)
            
            # Copy backup to data folder
            shutil.copytree(backup_path, data_path)
            print(f"Backup restored to: {data_path}")
            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False
    
    def get_ini_file_path(self, car_name: str, ini_name: str) -> str:
        """
        Get path to specific INI file in car data
        
        Args:
            car_name: Car folder name
            ini_name: INI file name (e.g., 'engine.ini')
            
        Returns:
            Full path to INI file
        """
        return os.path.join(self.get_car_data_path(car_name), ini_name)
    
    def get_lut_file_path(self, car_name: str, lut_name: str) -> str:
        """
        Get path to specific LUT file in car data
        
        Args:
            car_name: Car folder name
            lut_name: LUT file name (e.g., 'power.lut')
            
        Returns:
            Full path to LUT file
        """
        return os.path.join(self.get_car_data_path(car_name), lut_name)
    
    def delete_data_acd(self, car_name: str) -> bool:
        """
        Delete data.acd file for a car
        
        This is useful when a car has both data/ folder and data.acd.
        AC will use data.acd if it exists, so deleting it forces AC to use the data/ folder.
        
        Args:
            car_name: Car folder name
            
        Returns:
            True if successful or file doesn't exist, False on error
        """
        acd_path = os.path.join(self.get_car_path(car_name), 'data.acd')
        
        if not os.path.exists(acd_path):
            print(f"No data.acd file to delete for car: {car_name}")
            return True  # Not an error if file doesn't exist
        
        try:
            os.remove(acd_path)
            print(f"Deleted data.acd file for car: {car_name}")
            return True
        except Exception as e:
            print(f"Error deleting data.acd: {e}")
            return False
    
    def is_acd_encrypted(self, car_name: str) -> Tuple[bool, Optional[bool]]:
        """
        Check if data.acd file is encrypted
        
        Args:
            car_name: Car folder name
            
        Returns:
            Tuple of (acd_exists, is_encrypted)
            - acd_exists: True if data.acd exists
            - is_encrypted: True if encrypted, False if unencrypted (ZIP), None if file doesn't exist
        """
        acd_path = os.path.join(self.get_car_path(car_name), 'data.acd')
        
        if not os.path.exists(acd_path):
            return (False, None)
        
        try:
            # Check if it's a valid ZIP file (unencrypted ACD)
            # ZIP files start with PK magic bytes (0x50 0x4B)
            with open(acd_path, 'rb') as f:
                magic = f.read(2)
                if magic == b'PK':
                    # It's a ZIP file (unencrypted)
                    return (True, False)
                else:
                    # It's encrypted
                    return (True, True)
        except Exception as e:
            print(f"Error checking ACD file: {e}")
            return (True, None)
    
    def unpack_data_acd(self, car_name: str, backup_existing: bool = True, delete_acd: bool = False) -> bool:
        """
        Unpack data.acd file to data/ folder
        
        Attempts to unpack any data.acd file (encrypted or not).
        Encrypted files may extract but contents may not be readable.
        
        Args:
            car_name: Car folder name
            backup_existing: If True, backup existing data folder before unpacking
            delete_acd: If True, delete data.acd file after successful unpacking
            
        Returns:
            True if successful, False otherwise
        """
        acd_path = os.path.join(self.get_car_path(car_name), 'data.acd')
        data_path = self.get_car_data_path(car_name)
        
        # Check if ACD file exists
        if not os.path.exists(acd_path):
            print(f"No data.acd file found for car: {car_name}")
            return False
        
        try:
            # Backup existing data folder if requested
            if backup_existing and os.path.exists(data_path):
                backup_path = self.create_backup(car_name)
                if backup_path:
                    print(f"Existing data folder backed up to: {backup_path}")
            
            # Remove existing data folder if it exists
            if os.path.exists(data_path):
                shutil.rmtree(data_path)
            
            # Create data folder
            os.makedirs(data_path, exist_ok=True)
            
            # Try to extract as ZIP archive
            with zipfile.ZipFile(acd_path, 'r') as zip_ref:
                zip_ref.extractall(data_path)
            
            print(f"Successfully unpacked data.acd for car: {car_name}")
            
            # Delete data.acd if requested
            if delete_acd:
                try:
                    os.remove(acd_path)
                    print(f"Deleted data.acd file for car: {car_name}")
                except Exception as e:
                    print(f"Warning: Could not delete data.acd: {e}")
            
            return True
            
        except zipfile.BadZipFile:
            # Not a ZIP file - try QuickBMS if available
            print(f"data.acd is not a ZIP file, trying QuickBMS unpacker...")
            return self.unpack_data_acd_with_quickbms(car_name, backup_existing, delete_acd)
        except Exception as e:
            print(f"Error unpacking data.acd: {e}")
            return False
    
    def find_quickbms(self) -> Optional[str]:
        """
        Find QuickBMS executable
        
        Searches common locations for QuickBMS executable.
        
        Returns:
            Path to QuickBMS executable if found, None otherwise
        """
        # Check if QuickBMS path is configured
        quickbms_path = self.config_manager.get_quickbms_path() if self.config_manager is not None else None
        if quickbms_path and os.path.exists(quickbms_path):
            return quickbms_path
        
        # Common QuickBMS executable names
        if platform.system() == 'Windows':
            exe_names = ['quickbms.exe', 'QuickBMS.exe']
        else:
            exe_names = ['quickbms', 'QuickBMS']
        
        # Search in common locations (prioritize safe locations)
        search_paths = [
            # User-configured path first (most trusted)
            # Specific tool directories (safer than current dir)
            os.path.join(os.getcwd(), 'tools'),
            os.path.join(os.getcwd(), 'quickbms'),
            os.path.join(os.path.expanduser('~'), 'quickbms'),
            # System directories (trusted)
            '/usr/local/bin',
            '/usr/bin',
        ]
        
        # Add PATH directories
        if 'PATH' in os.environ:
            search_paths.extend(os.environ['PATH'].split(os.pathsep))
        
        # NOTE: Current directory is intentionally last for security
        search_paths.append(os.getcwd())
        search_paths.append(os.path.expanduser('~'))
        
        for path in search_paths:
            for exe_name in exe_names:
                full_path = os.path.join(path, exe_name)
                if os.path.exists(full_path) and os.path.isfile(full_path):
                    return full_path
        
        return None
    
    def find_acd_bms_script(self) -> Optional[str]:
        """
        Find the AC data.acd unpacker BMS script
        
        Returns:
            Path to acd.bms script if found, None otherwise
        """
        # Common script names
        script_names = ['acd.bms', 'ac_acd.bms', 'assetto_corsa.bms']
        
        # Search in common locations
        search_paths = [
            os.getcwd(),
            os.path.join(os.getcwd(), 'tools'),
            os.path.join(os.getcwd(), 'scripts'),
            os.path.join(os.getcwd(), 'quickbms'),
            os.path.expanduser('~'),
            os.path.join(os.path.expanduser('~'), 'quickbms'),
        ]
        
        for path in search_paths:
            for script_name in script_names:
                full_path = os.path.join(path, script_name)
                if os.path.exists(full_path) and os.path.isfile(full_path):
                    return full_path
        
        return None
    
    def unpack_data_acd_with_quickbms(self, car_name: str, backup_existing: bool = True, delete_acd: bool = False) -> bool:
        """
        Unpack data.acd using QuickBMS tool
        
        This method uses QuickBMS with the AC unpacker script to extract
        data.acd files in AC's custom format.
        
        Args:
            car_name: Car folder name
            backup_existing: If True, backup existing data folder before unpacking
            delete_acd: If True, delete data.acd file after successful unpacking
            
        Returns:
            True if successful, False otherwise
        """
        acd_path = os.path.join(self.get_car_path(car_name), 'data.acd')
        data_path = self.get_car_data_path(car_name)
        
        # Find QuickBMS executable
        quickbms_exe = self.find_quickbms()
        if not quickbms_exe:
            print("QuickBMS not found. Please install QuickBMS to unpack AC data.acd files.")
            print("Download from: http://aluigi.altervista.org/quickbms.htm")
            return False
        
        # Security: Validate the executable path is not in potentially unsafe locations
        unsafe_locations = [os.getcwd(), os.path.join(os.getcwd(), '.')]
        quickbms_dir = os.path.dirname(os.path.abspath(quickbms_exe))
        if quickbms_dir in unsafe_locations:
            print(f"WARNING: QuickBMS found in current directory ({quickbms_exe})")
            print("For security, consider moving it to a dedicated tools folder.")
        
        # Find BMS script
        bms_script = self.find_acd_bms_script()
        if not bms_script:
            print("AC data.acd unpacker script (acd.bms) not found.")
            print("Please download the Assetto Corsa BMS script for QuickBMS.")
            return False
        
        try:
            # Backup existing data folder if requested
            if backup_existing and os.path.exists(data_path):
                backup_path = self.create_backup(car_name)
                if backup_path:
                    print(f"Existing data folder backed up to: {backup_path}")
            
            # Remove existing data folder if it exists
            if os.path.exists(data_path):
                shutil.rmtree(data_path)
            
            # Create data folder
            os.makedirs(data_path, exist_ok=True)
            
            # Run QuickBMS
            print(f"Running QuickBMS to unpack {acd_path}...")
            cmd = [quickbms_exe, '-o', bms_script, acd_path, data_path]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )
            
            if result.returncode == 0:
                print(f"Successfully unpacked data.acd using QuickBMS for car: {car_name}")
                
                # Delete data.acd if requested
                if delete_acd:
                    try:
                        os.remove(acd_path)
                        print(f"Deleted data.acd file for car: {car_name}")
                    except Exception as e:
                        print(f"Warning: Could not delete data.acd: {e}")
                
                return True
            else:
                print(f"QuickBMS failed with return code {result.returncode}")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("QuickBMS timed out after 60 seconds")
            return False
        except Exception as e:
            print(f"Error running QuickBMS: {e}")
            return False
