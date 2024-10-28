from pttavm.client import PTTAVMClient

# İstemci oluşturma
client = PTTAVMClient()

# API versiyonunu kontrol etme
# Get version service
version_service = client.get_version_service()

# Get API version
version_info = version_service.get_version()

print("API Version Information:")
print(f"Version: {version_info['version']}")

