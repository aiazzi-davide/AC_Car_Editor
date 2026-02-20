"""
Configuration Manager for AC Car Editor
Handles application settings and Assetto Corsa path configuration
"""

import json
import os
from pathlib import Path


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_AC_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\assettocorsa"
    CONFIG_FILE = "config.json"
    
    def __init__(self):
        """Initialize configuration manager"""
        self.config = self._load_config()
        
    def _load_config(self):
        """Load configuration from file or create default"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Return default config
        return {
            'ac_path': self.DEFAULT_AC_PATH,
            'last_car': None,
            'backup_enabled': True,
            'backup_path': 'backups'
        }
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get_ac_path(self):
        """Get Assetto Corsa installation path"""
        return self.config.get('ac_path', self.DEFAULT_AC_PATH)
    
    def set_ac_path(self, path):
        """Set Assetto Corsa installation path"""
        self.config['ac_path'] = path
        self.save_config()
    
    def get_cars_path(self):
        """Get path to cars folder"""
        ac_path = self.get_ac_path()
        return os.path.join(ac_path, 'content', 'cars')
    
    def get_last_car(self):
        """Get last opened car name"""
        return self.config.get('last_car')
    
    def set_last_car(self, car_name):
        """Set last opened car name"""
        self.config['last_car'] = car_name
        self.save_config()
    
    def is_backup_enabled(self):
        """Check if backup is enabled"""
        return self.config.get('backup_enabled', True)
    
    def get_backup_path(self):
        """Get backup folder path"""
        return self.config.get('backup_path', 'backups')

    def get_show_disclaimer(self):
        """Whether to show the startup compatibility disclaimer"""
        return self.config.get('show_disclaimer', True)

    def set_show_disclaimer(self, value: bool):
        """Set whether to show the startup compatibility disclaimer"""
        self.config['show_disclaimer'] = value
        self.save_config()
