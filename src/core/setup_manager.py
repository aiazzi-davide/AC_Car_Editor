"""
Setup Manager for Assetto Corsa car setups.

Handles reading setup.ini parameters and saving/loading track-specific
setup presets as JSON files stored alongside the car data.

Setup presets are stored in:
    content/cars/<car_name>/setups/<track_name>.json
"""

import os
import json
from typing import List, Dict, Optional, Any

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.ini_parser import IniParser


class SetupManager:
    """Manage track-specific car setup presets."""

    SETUPS_DIR = 'setups'

    def __init__(self, car_data_path: str):
        """
        Args:
            car_data_path: Path to the car's data/ folder
        """
        self.car_data_path = car_data_path
        self.car_path = os.path.dirname(car_data_path)
        self.setup_ini_path = os.path.join(car_data_path, 'setup.ini')
        self.setups_dir = os.path.join(self.car_path, self.SETUPS_DIR)
        self.setup_ini = None
        self.parameters = []

        if os.path.exists(self.setup_ini_path):
            self.setup_ini = IniParser(self.setup_ini_path)
            self._parse_parameters()

    def _parse_parameters(self):
        """Parse setup.ini into a list of parameter dicts."""
        if not self.setup_ini:
            return
        self.parameters = []
        for section_name in self.setup_ini.get_sections():
            section = self.setup_ini.get_section(section_name)
            if not section:
                continue
            # Skip non-parameter sections
            if section_name in ('DISPLAY_METHOD', 'GEARS'):
                continue
            # Only include sections that have MIN (actual tuning parameters)
            if 'MIN' not in section:
                continue
            tab = section.get('TAB', 'GENERIC')
            name = section.get('NAME', section_name)
            param = {
                'section': section_name,
                'tab': tab,
                'name': name,
                'min': float(section.get('MIN', '0')),
                'max': float(section.get('MAX', '100')),
                'step': float(section.get('STEP', '1')),
                'help': section.get('HELP', ''),
                'show_clicks': int(float(section.get('SHOW_CLICKS', '0'))),
            }
            self.parameters.append(param)

    def get_parameters(self) -> List[Dict]:
        """Return parsed setup parameters."""
        return self.parameters

    def get_tabs(self) -> List[str]:
        """Return unique list of TAB names in order found."""
        seen = []
        for p in self.parameters:
            t = p['tab']
            if t not in seen:
                seen.append(t)
        return seen

    def get_parameters_by_tab(self, tab: str) -> List[Dict]:
        """Return parameters belonging to a specific tab."""
        return [p for p in self.parameters if p['tab'] == tab]

    # ------------------------------------------------------------------ presets

    def _ensure_setups_dir(self):
        os.makedirs(self.setups_dir, exist_ok=True)

    @staticmethod
    def _safe_preset_name(preset_name: str) -> Optional[str]:
        """Sanitize preset name to prevent path traversal."""
        if not preset_name or not isinstance(preset_name, str):
            return None
        name = preset_name.strip()
        if not name:
            return None
        # Reject any path separators or parent-directory references
        if os.sep in name or '/' in name or '\\' in name or '..' in name:
            return None
        return name

    def list_presets(self) -> List[str]:
        """List available preset names (track names)."""
        if not os.path.isdir(self.setups_dir):
            return []
        presets = []
        for f in sorted(os.listdir(self.setups_dir)):
            if f.endswith('.json'):
                presets.append(f[:-5])
        return presets

    def save_preset(self, preset_name: str, values: Dict[str, float]) -> bool:
        """Save a setup preset.

        Args:
            preset_name: Name of the preset (typically a track name)
            values: Dict mapping section names to their current values
        Returns:
            True if saved successfully
        """
        name = self._safe_preset_name(preset_name)
        if not name:
            return False
        self._ensure_setups_dir()
        path = os.path.join(self.setups_dir, f'{name}.json')
        try:
            data = {
                'name': name,
                'values': values,
            }
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving preset: {e}")
            return False

    def load_preset(self, preset_name: str) -> Optional[Dict[str, float]]:
        """Load a setup preset and return its values dict."""
        name = self._safe_preset_name(preset_name)
        if not name:
            return None
        path = os.path.join(self.setups_dir, f'{name}.json')
        if not os.path.exists(path):
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('values', {})
        except Exception as e:
            print(f"Error loading preset: {e}")
            return None

    def delete_preset(self, preset_name: str) -> bool:
        """Delete a saved preset."""
        name = self._safe_preset_name(preset_name)
        if not name:
            return False
        path = os.path.join(self.setups_dir, f'{name}.json')
        if not os.path.exists(path):
            return False
        try:
            os.remove(path)
            return True
        except Exception as e:
            print(f"Error deleting preset: {e}")
            return False

    def has_setup_ini(self) -> bool:
        """Return True if setup.ini exists for this car."""
        return self.setup_ini is not None
