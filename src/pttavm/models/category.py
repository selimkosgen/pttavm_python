from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Category:
    """Category model representing PTT AVM category data"""
    id: str
    name: str
    parent_id: Optional[str] = None
    updated_at: Optional[str] = None
    children: List['Category'] = None
    success: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        """Create Category instance from dictionary data"""
        # Handle main category data
        category_data = data.get('a:category', {})
        
        # Create main category instance
        category = cls(
            id=category_data.get('a:id', ''),
            name=category_data.get('a:name', ''),
            parent_id=category_data.get('a:parent_id'),
            updated_at=category_data.get('a:updated_at'),
            success=data.get('a:success', 'true').lower() == 'true',
            children=[]
        )
        
        # Handle children if they exist
        if 'a:children' in category_data and category_data['a:children']:
            children_data = category_data['a:children'].get('a:category', [])
            # Ensure children_data is a list
            if not isinstance(children_data, list):
                children_data = [children_data]
                
            for child in children_data:
                child_category = cls(
                    id=child.get('a:id', ''),
                    name=child.get('a:name', ''),
                    parent_id=child.get('a:parent_id'),
                    updated_at=child.get('a:updated_at')
                )
                category.children.append(child_category)
                
        return category
