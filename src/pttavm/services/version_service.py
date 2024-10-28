from typing import Dict
from .base_service import BaseService

class VersionService(BaseService):
    """Service for version related operations"""
    
    def get_version(self) -> Dict[str, str]:
        """
        Get current API version
        
        Returns:
            Dict containing version information
            
        Example:
            {
                'version': '1.0.4.0'
            }
            
        Raises:
            Exception: If API call fails
        """
        try:
            response = self.call_service('GetVersion')
            return {
                'version': response if response else 'unknown'
            }
        except Exception as e:
            raise Exception(f"Failed to get version: {str(e)}")
