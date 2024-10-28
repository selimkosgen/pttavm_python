from typing import Optional
from .services.version_service import VersionService
from .services.category_service import CategoryService
from .services.product_service import ProductService

class PTTAVMClient:
    """Client for interacting with PTT AVM API"""
    
    def __init__(self, api_key: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize PTT AVM client
        
        Args:
            api_key: API key for authentication
            username: Username for authentication
            password: Password for authentication
        """
        self.api_key = api_key
        self.username = username
        self.password = password
        self._version_service = None
        self._category_service = None
        self._product_service = None

    def get_version_service(self) -> VersionService:
        """
        Get the version service instance
        
        Returns:
            VersionService instance
        """
        if not self._version_service:
            self._version_service = VersionService(
                api_key=self.api_key,
                username=self.username,
                password=self.password
            )
        return self._version_service

    def get_category_service(self) -> CategoryService:
        """
        Get the category service instance
        
        Returns:
            CategoryService instance
        """
        if not self._category_service:
            self._category_service = CategoryService(
                api_key=self.api_key,
                username=self.username,
                password=self.password
            )
        return self._category_service

    def get_product_service(self) -> ProductService:
        """
        Get the product service instance
        
        Returns:
            ProductService instance
        """
        if not self._product_service:
            self._product_service = ProductService(
                api_key=self.api_key,
                username=self.username,
                password=self.password
            )
        return self._product_service
