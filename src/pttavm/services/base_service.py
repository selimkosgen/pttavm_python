import requests
from typing import Optional, Dict, Any
import xmltodict

class BaseService:
    """Base service for SOAP API calls"""
    
    API_URL = "https://ws.pttavm.com:93/service.svc"
    SOAP_ACTION_BASE = "http://tempuri.org/IService/"
    
    def __init__(self, api_key: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        self.api_key = api_key
        self.username = username
        self.password = password

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
            param_xml += f"<tem:{key}>{value}</tem:{key}>"
            
        return f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                         xmlns:tem="http://tempuri.org/" 
                         xmlns:ept="http://schemas.datacontract.org/2004/07/ePttAVMService">
            <soapenv:Header>
                <wsse:Security soapenv:mustUnderstand="1" 
                             xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                    <wsse:UsernameToken>
                        <wsse:Username>{self.username}</wsse:Username>
                        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{self.password}</wsse:Password>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <tem:{operation}>{param_xml}</tem:{operation}>
            </soapenv:Body>
        </soapenv:Envelope>
        """

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
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"API call failed with status code: {response.status_code}")
                
            # Parse XML response
            response_dict = xmltodict.parse(response.content)
            
            # Extract response from SOAP envelope
            soap_body = response_dict['s:Envelope']['s:Body']
            response_key = f'{operation}Response'
            result_key = f'{operation}Result'
            
            if response_key in soap_body and result_key in soap_body[response_key]:
                return soap_body[response_key][result_key]
                
            return None
            
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")
