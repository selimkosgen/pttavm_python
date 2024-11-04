import requests
import xmltodict
from typing import Dict, Any, Optional

class BaseService:
    """Base service for SOAP API calls"""
    
    API_URL = "https://ws.pttavm.com:93/service.svc"
    SOAP_ACTION_BASE = "http://tempuri.org/IService/"
    
    def __init__(self, api_key: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        self.api_key = api_key
        self.username = username
        self.password = password
        self.base_url = "https://ws.pttavm.com:93"

    def _create_soap_envelope(self, operation: str, params: Dict = None) -> str:
        """
        Create SOAP envelope with authentication header
        
        Args:
            operation: Operation name
            params: Parameters for the operation
        """
        if params is None:
            params = {}
            
        param_xml = ""
        for key, value in params.items():
            if isinstance(value, dict):
                param_xml += f"<tem:{key}>"
                for sub_key, sub_value in value.items():
                    param_xml += f"<{sub_key}>{sub_value}</{sub_key}>"
                param_xml += f"</tem:{key}>"
            else:
                param_xml += f"<tem:{key}>{value}</tem:{key}>"
            
        return f"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                      xmlns:tem="http://tempuri.org/" 
                      xmlns:ept="http://schemas.datacontract.org/2004/07/ePttAVMService">
            <soap:Header>
                <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                    <wsse:UsernameToken>
                        <wsse:Username>{self.username}</wsse:Username>
                        <wsse:Password>{self.password}</wsse:Password>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soap:Header>
            <soap:Body>
                <tem:{operation}>{param_xml}</tem:{operation}>
            </soap:Body>
        </soap:Envelope>"""

    def call_service(self, operation: str, params: Dict = None) -> Any:
        """
        Make SOAP API call
        
        Args:
            operation: Operation name
            params: Parameters for the operation
            
        Returns:
            Response from the API
        """
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': f'{self.SOAP_ACTION_BASE}{operation}'
        }
        
        body = self._create_soap_envelope(operation, params)
        
        try:
            response = requests.post(
                self.API_URL,
                data=body.encode('utf-8'),
                headers=headers,
                verify=False,  # SSL sertifika doğrulamasını devre dışı bırak
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"API call failed with status code: {response.status_code}, Response: {response.text}")
                
            # Parse XML response
            response_dict = xmltodict.parse(response.content)
            
            # Extract response from SOAP envelope
            soap_body = response_dict['soap:Envelope']['soap:Body']
            response_key = f'{operation}Response'
            result_key = f'{operation}Result'
            
            if response_key in soap_body and result_key in soap_body[response_key]:
                return soap_body[response_key][result_key]
                
            return None
            
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")

    def _make_request(
        self, 
        method: str, 
        url: str, 
        headers: Optional[Dict[str, str]] = None,
        data: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        HTTP isteği yapmak için kullanılan yardımcı metod.

        Args:
            method (str): HTTP metodu (GET, POST, etc.)
            url (str): İstek yapılacak URL
            headers (Dict[str, str], optional): HTTP başlıkları
            data (str, optional): İstek gövdesi
            params (Dict[str, Any], optional): URL parametreleri

        Returns:
            requests.Response: HTTP yanıtı
        """
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params
        )
        response.raise_for_status()
        return response
