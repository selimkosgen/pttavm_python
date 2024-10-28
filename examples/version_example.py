import os
from pttavm.client import PTTAVMClient

def main():
    # Get credentials from environment variables
    username = os.getenv('PTT_USERNAME')
    password = os.getenv('PTT_PASSWORD')
    
    if not username or not password:
        print("Error: PTT_USERNAME and PTT_PASSWORD environment variables must be set")
        return
    
    # Initialize client
    client = PTTAVMClient(
        username=username,
        password=password
    )
    
    try:
        # Get version service
        version_service = client.get_version_service()
        
        # Get API version
        version_info = version_service.get_version()
        
        print("API Version Information:")
        print(f"Version: {version_info['version']}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
