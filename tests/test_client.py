import pytest
from pttavm.client import PTTAVMClient

def test_client_initialization():
    """Test client initialization with valid credentials"""
    client = PTTAVMClient(
        username="test_user",
        password="test_pass"
    )
    assert client.username == "test_user"
    assert client.password == "test_pass"
    assert client.client is not None

def test_client_invalid_wsdl():
    """Test client initialization with invalid WSDL URL"""
    with pytest.raises(Exception):
        PTTAVMClient(
            username="test_user",
            password="test_pass",
            wsdl_url="invalid_url"
        )
