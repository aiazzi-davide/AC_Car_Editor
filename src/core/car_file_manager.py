"""
Car File Manager for handling Assetto Corsa car files and folders
"""

import os
import shutil
import subprocess
import sys
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
        Delete data.acd file from car folder
        This should be called after unpacking or modifying a car
        so that Assetto Corsa uses the data folder instead
        
        Args:
            car_name: Car folder name
            
        Returns:
            True if deleted successfully or file doesn't exist
        """
        acd_path = os.path.join(self.get_car_path(car_name), 'data.acd')
        
        if not os.path.exists(acd_path):
            return True
        
        try:
            os.remove(acd_path)
            print(f"Deleted data.acd: {acd_path}")
            return True
        except Exception as e:
            print(f"Error deleting data.acd: {e}")
            return False
    
    def _find_quickbms_path(self) -> Optional[str]:
        """
        Find quickBMS executable path
        
        Returns:
            Path to quickbms.exe or None if not found
        """
        # Get the project root directory (where main.py is located)
        if hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Running as script - go up from core/ to project root
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Check tools/quickbms folder
        tools_path = os.path.join(base_path, 'tools', 'quickbms', 'quickbms.exe')
        if os.path.exists(tools_path):
            return tools_path
        
        # Check for 4gb version
        tools_path_4gb = os.path.join(base_path, 'tools', 'quickbms', 'quickbms_4gb_files.exe')
        if os.path.exists(tools_path_4gb):
            return tools_path_4gb
        
        return None
    
    def _find_quickbms_script(self) -> Optional[str]:
        """
        Find quickBMS script for Assetto Corsa
        
        Returns:
            Path to assetto_corsa_acd.bms or None if not found
        """
        # Get the project root directory
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        script_path = os.path.join(base_path, 'tools', 'assetto_corsa_acd.bms')
        if os.path.exists(script_path):
            return script_path
        
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
        data_path = self.get_car_data_path(car_name)
        
        # Check if data.acd exists
        if not os.path.exists(acd_path):
            print(f"data.acd not found: {acd_path}")
            return False
        
        # Check if data folder already exists
        if os.path.exists(data_path):
            print(f"Data folder already exists: {data_path}")
            # If we should delete acd and folder exists, just delete the acd
            if delete_acd:
                return self.delete_data_acd(car_name)
            return True
        
        # Find quickBMS executable and script
        quickbms_exe = self._find_quickbms_path()
        quickbms_script = self._find_quickbms_script()
        
        if not quickbms_exe:
            print("quickBMS executable not found in tools/quickbms/")
            return False
        
        if not quickbms_script:
            print("quickBMS script not found in tools/")
            return False
        
        # Check if we're on Windows
        if sys.platform != 'win32':
            print("quickBMS unpacking is only supported on Windows")
            print(f"Please manually extract {acd_path} on Windows")
            return False
        
        # Create data folder
        os.makedirs(data_path, exist_ok=True)
        
        # Run quickBMS
        # Command: quickbms.exe script.bms input.acd output_folder
        try:
            cmd = [quickbms_exe, '-o', quickbms_script, acd_path, data_path]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"Successfully unpacked data.acd to: {data_path}")
                
                # Delete data.acd if requested
                if delete_acd:
                    self.delete_data_acd(car_name)
                
                return True
            else:
                print(f"quickBMS failed with return code {result.returncode}")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("quickBMS process timed out")
            return False
        except Exception as e:
            print(f"Error running quickBMS: {e}")
            return False
