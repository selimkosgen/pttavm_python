from typing import Dict
from pttavm.client import PTTAVMClient  # Changed from relative to absolute import

class VersionController:
    """Controller for checking PTT AVM API version"""
    
    def __init__(self, client: PTTAVMClient):
        self.client = client
        self.service = client.get_service()
    
    def get_version(self) -> Dict[str, str]:
        """
        Get current API version
        
        Returns:
            Dict containing version information
        """
        try:
            response = self.service.GetVersion()
            return {
                'version': response.get('version', 'unknown'),
                'release_date': response.get('releaseDate', 'unknown')
            }
        except Exception as e:
            raise Exception(f"Failed to get version: {str(e)}")

def get_version() -> str:
    """Return the current version of the package"""
    return "0.1.0"
