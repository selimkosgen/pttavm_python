import os
import unittest
from unittest.mock import patch, MagicMock
from pttavm.client import PTTAVMClient
from pttavm.services.version_service import VersionService

class TestVersionService(unittest.TestCase):
    def setUp(self):
        # Use environment variables or default test values
        self.client = PTTAVMClient(
            username=os.getenv('PTT_TEST_USERNAME', 'test_user'),
            password=os.getenv('PTT_TEST_PASSWORD', 'test_pass')
        )
        self.version_service = self.client.get_version_service()

    @patch('pttavm.services.base_service.requests.post')
    def test_get_version_success(self, mock_post):
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = """
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
                <GetVersionResponse xmlns="http://tempuri.org/">
                    <GetVersionResult>1.0.4.0</GetVersionResult>
                </GetVersionResponse>
            </s:Body>
        </s:Envelope>
        """.encode('utf-8')
        mock_post.return_value = mock_response

        # Test get_version
        version_info = self.version_service.get_version()
        
        # Assertions
        self.assertIsInstance(version_info, dict)
        self.assertIn('version', version_info)
        self.assertEqual(version_info['version'], '1.0.4.0')

    @patch('pttavm.services.base_service.requests.post')
    def test_get_version_error(self, mock_post):
        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Test error handling
        with self.assertRaises(Exception) as context:
            self.version_service.get_version()
        
        self.assertTrue('API call failed with status code: 500' in str(context.exception))

    def test_client_initialization(self):
        # Test client initialization
        self.assertIsInstance(self.client.get_service(), VersionService)
        self.assertEqual(self.client.api_key, "test_key")
        self.assertEqual(self.client.username, "test_user")
        self.assertEqual(self.client.password, "test_pass")

if __name__ == '__main__':
    unittest.main()
