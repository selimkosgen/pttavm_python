from typing import Optional
from .base_service import BaseService
from ..models.product import Product

class ProductService(BaseService):
    """Service for product related operations"""
    
    def check_barcode(self, barcode: str) -> Optional[Product]:
        """
        Check product information by barcode
        
        Args:
            barcode: Product barcode to check
            
        Returns:
            Product object if found, None otherwise
            
        Raises:
            Exception: If API call fails
        """
        try:
            params = {'Barkod': barcode}
            response = self.call_service('BarkodKontrol', params)
            
            if not response:
                return None
                
            return Product.from_dict(response)
            
        except Exception as e:
            raise Exception(f"Failed to check barcode: {str(e)}")
