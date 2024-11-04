import pytest
from pttavm.client import PTTAVMClient
from unittest.mock import patch

@pytest.fixture
def client():
    return PTTAVMClient(
        username="test_user",
        password="test_pass"
    )

@pytest.fixture
def product_service(client):
    return client.get_product_service()

def test_get_stock_list(product_service):
    with patch('pttavm.services.base_service.BaseService._make_request') as mock_request:
        # Mock response setup
        mock_request.return_value.text = """
        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <StokKontrolListesiResponse xmlns="http://tempuri.org/">
                    <StokKontrolListesiResult>
                        <!-- Mock stock list data -->
                        <Stoklar>
                            <Stok>
                                <Barkod>123456</Barkod>
                                <StokAdedi>10</StokAdedi>
                            </Stok>
                        </Stoklar>
                    </StokKontrolListesiResult>
                </StokKontrolListesiResponse>
            </soap:Body>
        </soap:Envelope>
        """
        
        result = product_service.get_stock_list()
        
        assert result is not None
        # Add more specific assertions based on expected response structure 