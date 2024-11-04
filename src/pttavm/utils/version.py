from typing import Dict

def get_version() -> str:
    """Return the current version of the package"""
    return "0.1.5"

class VersionController:
    """Controller for checking PTT AVM API version"""
    
    def __init__(self, client):
        self.client = client
        self.service = client.get_service('version')
    
    def get_version(self) -> Dict[str, str]:
        """
        Get current API version
        
        Returns:
            Dict containing version information
        """
        try:
            response = self.service.get_version()
            return {
                'version': response.get('version', 'unknown'),
                'release_date': response.get('releaseDate', 'unknown')
            }
        except Exception as e:
            raise Exception(f"Failed to get version: {str(e)}")
