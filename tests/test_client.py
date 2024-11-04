import pytest
from pttavm.client import PTTClient

def test_client_initialization():
    """Test client initialization with valid credentials"""
    client = PTTClient(
        username="test_user",
        password="test_pass"
    )
    assert client.username == "test_user"
    assert client.password == "test_pass"
    assert client._category_service is not None
    assert client._stock_service is not None
    assert client._product_service is not None
    assert client._version_service is not None

def test_client_invalid_credentials():
    """Test client initialization with invalid credentials"""
    client = PTTClient(
        username="invalid",
        password="invalid"
    )
    with pytest.raises(Exception):
        client.get_version()
