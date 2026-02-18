"""
Car File Manager for handling Assetto Corsa car files and folders
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime


class CarFileManager:
    """Manages Assetto Corsa car files and folders"""
    
    def __init__(self, cars_path: str):
        """
        Initialize car file manager
        
        Args:
            cars_path: Path to AC cars folder
        """
        self.cars_path = cars_path
    
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
    
    def get_car_preview_path(self, car_name: str) -> Optional[str]:
        """
        Get path to car preview image (preview.png or preview.jpg)
        
        Args:
            car_name: Car folder name
            
        Returns:
            Full path to preview image or None if not found
        """
        ui_dir = os.path.join(self.get_car_path(car_name), 'ui')
        
        # Check for preview.png first, then preview.jpg
        for ext in ['.png', '.jpg', '.jpeg']:
            preview_path = os.path.join(ui_dir, f'preview{ext}')
            if os.path.exists(preview_path):
                return preview_path
        
        return None
    
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
            'preview_path': None,
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
        
        # Get preview image path
        info['preview_path'] = self.get_car_preview_path(car_name)
        
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
        Rename data.acd to data.acd.bak for a car.

        AC prioritizes data.acd over the unpacked data/ folder, so renaming
        it disables it while keeping a recoverable backup.

        Args:
            car_name: Car folder name

        Returns:
            True if renamed successfully or file doesn't exist
        """
        acd_path = os.path.join(self.get_car_path(car_name), 'data.acd')
        bak_path = acd_path + '.bak'

        if not os.path.exists(acd_path):
            return True

        try:
            os.rename(acd_path, bak_path)
            print(f"Renamed data.acd to data.acd.bak for {car_name}")
            return True
        except Exception as e:
            print(f"Error renaming data.acd: {e}")
            return False
    
    def _find_quickbms_path(self) -> Optional[str]:
        """
        Find quickbms.exe in the tools folder
        
        Returns:
            Path to quickbms.exe or None if not found
        """
        # Try relative to project root
        possible_paths = [
            os.path.join('tools', 'quickbms', 'quickbms.exe'),
            os.path.join('tools', 'quickbms.exe'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'quickbms', 'quickbms.exe'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'quickbms.exe'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return None
    
    def _find_quickbms_script(self) -> Optional[str]:
        """
        Find assetto_corsa_acd.bms script
        
        Returns:
            Path to script or None if not found
        """
        possible_paths = [
            os.path.join('tools', 'assetto_corsa_acd.bms'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'assetto_corsa_acd.bms'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return None
    
    def unpack_data_acd(self, car_name: str, delete_acd: bool = True) -> bool:
        """
        Unpack data.acd file using quickBMS
        
        Args:
            car_name: Car folder name
            delete_acd: If True, delete data.acd after successful unpacking
            
        Returns:
            True if unpacked successfully
        """
        acd_path = os.path.join(self.get_car_path(car_name), 'data.acd')
        
        if not os.path.exists(acd_path):
            print(f"No data.acd file found for {car_name}")
            return False
        
        # Find quickBMS executable
        quickbms_exe = self._find_quickbms_path()
        if not quickbms_exe:
            print("Error: quickbms.exe not found in tools folder")
            return False
        
        # Find quickBMS script
        quickbms_script = self._find_quickbms_script()
        if not quickbms_script:
            print("Error: assetto_corsa_acd.bms script not found in tools folder")
            return False
        
        # Create data folder if it doesn't exist
        data_path = self.get_car_data_path(car_name)
        os.makedirs(data_path, exist_ok=True)
        
        try:
            # Run quickBMS: quickbms.exe -o script.bms data.acd output_folder
            # -o flag overwrites existing files
            cmd = [quickbms_exe, '-o', quickbms_script, acd_path, data_path]
            
            # Run quickBMS and capture output
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(quickbms_exe)
            )
            
            # Check if extraction was successful
            if result.returncode == 0:
                print(f"Successfully unpacked data.acd for {car_name}")
                
                # Delete data.acd if requested
                if delete_acd:
                    self.delete_data_acd(car_name)
                
                return True
            else:
                print(f"Error unpacking data.acd: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error running quickBMS: {e}")
            return False
