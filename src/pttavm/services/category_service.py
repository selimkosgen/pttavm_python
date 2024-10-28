import requests
import xmltodict
from typing import List, Optional, Dict
from .base_service import BaseService
from ..models.category import Category

class CategoryService(BaseService):
    """Service for category related operations"""
    
    def get_categories(self, category_id: str = "1") -> Category:
        """
        Get category and its children from PTT AVM
        
        Args:
            category_id: Category ID to get details for. Defaults to "1" for root category.
            
        Returns:
            Category object with children
            
        Raises:
            Exception: If API call fails
        """
        try:
            params = {'id': category_id}
            response = self.call_service('GetCategory', params)
            
            if not response:
                return None
                
            return Category.from_dict(response)
            
        except Exception as e:
            raise Exception(f"Failed to get categories: {str(e)}")
