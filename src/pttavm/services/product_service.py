from typing import Optional
from .base_service import BaseService
from ..models.product import Product
import xmltodict

class ProductService(BaseService):
    """Service for product related operations"""
    
    def check_barcode(self, barcode: str) -> dict:
        """
        Check if a barcode exists in PTT AVM system.
        
        Args:
            barcode (str): The barcode to check
            
        Returns:
            dict: Response from PTT AVM API containing barcode check result
        """
        soap_action = "http://tempuri.org/IService/BarkodKontrol"
        
        soap_envelope = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
            <soapenv:Header>
                {self._get_security_header()}
            </soapenv:Header>
            <soapenv:Body>
                <tem:BarkodKontrol>
                    <tem:Barkod>{barcode}</tem:Barkod>
                </tem:BarkodKontrol>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        response = self._make_request(
            soap_action=soap_action,
            soap_envelope=soap_envelope
        )
        
        return xmltodict.parse(response.text)

    def get_stock_list(self) -> dict:
        """
        Get stock list from PTT AVM system.
        
        Returns:
            dict: Response from PTT AVM API containing stock list
        """
        soap_action = "http://tempuri.org/IService/StokKontrolListesi"
        
        soap_envelope = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
            <soapenv:Header>
                {self._get_security_header()}
            </soapenv:Header>
            <soapenv:Body>
                <tem:StokKontrolListesi/>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        response = self._make_request(
            soap_action=soap_action,
            soap_envelope=soap_envelope
        )
        
        return xmltodict.parse(response.text)
