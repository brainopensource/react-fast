import unittest
from unittest.mock import patch
from backend.app.adapters.api_clients.odata_api_client import ODataAPIClient

class TestODataAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = ODataAPIClient(base_url="https://example.com/odata")  # Replace with actual OData API URL

    @patch('backend.app.adapters.api_clients.odata_api_client.requests.get')
    def test_fetch_data_success(self, mock_get):
        # Arrange
        expected_data = {"key": "value"}
        mock_get.return_value.json.return_value = expected_data
        mock_get.return_value.status_code = 200

        # Act
        result = self.client.fetch_data("username", "password")

        # Assert
        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with("https://example.com/odata", auth=('username', 'password'))

    @patch('backend.app.adapters.api_clients.odata_api_client.requests.get')
    def test_fetch_data_failure(self, mock_get):
        # Arrange
        mock_get.side_effect = Exception("API error")

        # Act & Assert
        with self.assertRaises(Exception):
            self.client.fetch_data("username", "password")

if __name__ == "__main__":
    unittest.main()
