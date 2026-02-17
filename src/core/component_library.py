"""
Component Library Manager for pre-built car components
"""

import json
import os
from typing import List, Dict, Optional, Any


class ComponentLibrary:
    """Manages library of pre-built car components"""
    
    COMPONENT_TYPES = [
        'engine',
        'suspension',
        'differential',
        'drivetrain',
        'aero',
        'tyres',
    ]
    
    def __init__(self, library_path: str = 'src/components/library.json'):
        """
        Initialize component library
        
        Args:
            library_path: Path to library JSON file
        """
        self.library_path = library_path
        self.components: Dict[str, List[Dict]] = {
            comp_type: [] for comp_type in self.COMPONENT_TYPES
        }
        
        # Create directory if needed
        os.makedirs(os.path.dirname(library_path), exist_ok=True)
        
        if os.path.exists(library_path):
            self.load()
        else:
            self._create_default_library()
            self.save()
    
    def load(self):
        """Load component library from file"""
        try:
            with open(self.library_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.components = data.get('components', self.components)
        except Exception as e:
            print(f"Error loading component library: {e}")
            self._create_default_library()
    
    def save(self):
        """Save component library to file"""
        try:
            data = {
                'version': '1.0',
                'components': self.components
            }
            with open(self.library_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving component library: {e}")
    
    def _create_default_library(self):
        """Create default component library with some examples"""
        # Example engine components
        self.components['engine'] = [
            {
                'id': 'engine_default',
                'name': 'Default Engine',
                'description': 'Default engine configuration',
                'tags': ['stock'],
                'data': {
                    'MINIMUM': 1000,
                    'LIMITER': 8000,
                    'INERTIA': 0.15,
                }
            }
        ]
        
        # Example suspension components
        self.components['suspension'] = [
            {
                'id': 'suspension_default',
                'name': 'Default Suspension',
                'description': 'Default suspension setup',
                'tags': ['stock'],
                'data': {}
            }
        ]
        
        # Example differential components
        self.components['differential'] = [
            {
                'id': 'diff_default',
                'name': 'Default Differential',
                'description': 'Default differential setup',
                'tags': ['stock'],
                'data': {}
            }
        ]
    
    def get_components(self, component_type: str) -> List[Dict]:
        """
        Get all components of a specific type
        
        Args:
            component_type: Type of component
            
        Returns:
            List of components
        """
        return self.components.get(component_type, [])
    
    def get_component(self, component_type: str, component_id: str) -> Optional[Dict]:
        """
        Get specific component by ID
        
        Args:
            component_type: Type of component
            component_id: Component ID
            
        Returns:
            Component dictionary or None
        """
        for component in self.components.get(component_type, []):
            if component.get('id') == component_id:
                return component
        return None
    
    def add_component(self, component_type: str, component: Dict) -> bool:
        """
        Add a new component to library
        
        Args:
            component_type: Type of component
            component: Component dictionary
            
        Returns:
            True if successful
        """
        if component_type not in self.COMPONENT_TYPES:
            print(f"Invalid component type: {component_type}")
            return False
        
        # Check if ID already exists
        component_id = component.get('id')
        if self.get_component(component_type, component_id):
            print(f"Component with ID {component_id} already exists")
            return False
        
        self.components[component_type].append(component)
        self.save()
        return True
    
    def update_component(self, component_type: str, component_id: str, component: Dict) -> bool:
        """
        Update existing component
        
        Args:
            component_type: Type of component
            component_id: Component ID
            component: Updated component dictionary
            
        Returns:
            True if successful
        """
        components = self.components.get(component_type, [])
        for i, comp in enumerate(components):
            if comp.get('id') == component_id:
                components[i] = component
                self.save()
                return True
        return False
    
    def delete_component(self, component_type: str, component_id: str) -> bool:
        """
        Delete component from library
        
        Args:
            component_type: Type of component
            component_id: Component ID
            
        Returns:
            True if successful
        """
        components = self.components.get(component_type, [])
        for i, comp in enumerate(components):
            if comp.get('id') == component_id:
                components.pop(i)
                self.save()
                return True
        return False
    
    def search_components(self, component_type: str, query: str) -> List[Dict]:
        """
        Search components by name or tags
        
        Args:
            component_type: Type of component
            query: Search query
            
        Returns:
            List of matching components
        """
        query = query.lower()
        results = []
        
        for component in self.components.get(component_type, []):
            name = component.get('name', '').lower()
            tags = ' '.join(component.get('tags', [])).lower()
            description = component.get('description', '').lower()
            
            if query in name or query in tags or query in description:
                results.append(component)
        
        return results
