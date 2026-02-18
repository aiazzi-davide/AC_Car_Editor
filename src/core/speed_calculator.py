"""
Speed Calculator for gear ratios.

Calculates maximum speed for each gear based on:
- Gear ratio
- Final drive ratio
- Engine max RPM
- Tire radius/diameter
"""

import math
import os
from typing import Optional


class SpeedCalculator:
    """Calculate maximum speed for gears"""
    
    @staticmethod
    def calculate_max_speed(gear_ratio: float, final_ratio: float, 
                           max_rpm: int, tire_radius: float) -> float:
        """
        Calculate maximum speed for a gear.
        
        Formula: Speed (km/h) = (RPM × 2π × Radius × 60) / (Gear × Final × 1000)
        
        Where:
        - Radius is in meters
        - RPM is engine revolutions per minute
        - Gear and Final are ratio values
        
        Args:
            gear_ratio: Individual gear ratio
            final_ratio: Final drive ratio
            max_rpm: Maximum engine RPM
            tire_radius: Tire radius in meters
            
        Returns:
            Maximum speed in km/h
        """
        if gear_ratio == 0 or final_ratio == 0:
            return 0.0
        
        # Calculate wheel RPM
        wheel_rpm = max_rpm / (abs(gear_ratio) * final_ratio)
        
        # Calculate speed: wheel_rpm × circumference × 60 min/hr / 1000 m/km
        tire_circumference = 2 * math.pi * tire_radius
        speed_kmh = (wheel_rpm * tire_circumference * 60) / 1000
        
        return speed_kmh
    
    @staticmethod
    def get_tire_radius_from_ini(tyres_ini_path: str, compound_index: int = 0) -> Optional[float]:
        """
        Get tire radius from tyres.ini file.
        
        Args:
            tyres_ini_path: Path to tyres.ini
            compound_index: Compound index (0 for FRONT, 1 for FRONT_1, etc.)
            
        Returns:
            Tire radius in meters, or None if not found
        """
        if not os.path.exists(tyres_ini_path):
            return None
        
        try:
            from core.ini_parser import IniParser
            parser = IniParser(tyres_ini_path)
            
            # Try FRONT section first (compound 0), then FRONT_N
            section = 'FRONT' if compound_index == 0 else f'FRONT_{compound_index}'
            
            if parser.has_section(section):
                radius_str = parser.get_value(section, 'RADIUS', None)
                if radius_str:
                    return float(radius_str)
            
            # Fallback to FRONT if specific compound not found
            if compound_index > 0 and parser.has_section('FRONT'):
                radius_str = parser.get_value('FRONT', 'RADIUS', None)
                if radius_str:
                    return float(radius_str)
                    
        except Exception as e:
            print(f"Error reading tire radius: {e}")
        
        return None
    
    @staticmethod
    def get_max_rpm_from_ini(engine_ini_path: str) -> Optional[int]:
        """
        Get maximum RPM from engine.ini file.
        
        Args:
            engine_ini_path: Path to engine.ini
            
        Returns:
            Maximum RPM (LIMITER value), or None if not found
        """
        if not os.path.exists(engine_ini_path):
            return None
        
        try:
            from core.ini_parser import IniParser
            parser = IniParser(engine_ini_path)
            
            if parser.has_section('ENGINE_DATA'):
                limiter_str = parser.get_value('ENGINE_DATA', 'LIMITER', None)
                if limiter_str:
                    return int(float(limiter_str))
                    
        except Exception as e:
            print(f"Error reading max RPM: {e}")
        
        return None
    
    @staticmethod
    def format_speed(speed: float) -> str:
        """
        Format speed for display.
        
        Args:
            speed: Speed in km/h
            
        Returns:
            Formatted string (e.g., "245 km/h")
        """
        if speed <= 0:
            return "N/A"
        return f"{speed:.0f} km/h"
