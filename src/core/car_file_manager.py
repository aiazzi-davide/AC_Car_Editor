"""
Car File Manager for handling Assetto Corsa car files and folders
"""

import os
import shutil
import zipfile
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
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
            print(f"data.acd is not a valid ZIP file (may be encrypted): {car_name}")
            return False
        except Exception as e:
            print(f"Error unpacking data.acd: {e}")
            return False
