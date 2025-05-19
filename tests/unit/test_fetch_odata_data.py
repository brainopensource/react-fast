import unittest
from unittest.mock import MagicMock
from backend.app.application.use_cases.fetch_odata_data import FetchODataData
from backend.app.adapters.api_clients.odata_api_client import ODataAPIClient

class TestFetchODataData(unittest.TestCase):
    def setUp(self):
        self.mock_external_service = MagicMock(spec=ODataAPIClient)
        self.use_case = FetchODataData(self.mock_external_service)

    def test_execute_success(self):
        # Arrange
        expected_data = {"key": "value"}
        self.mock_external_service.fetch_data.return_value = expected_data

        # Act
        result = self.use_case.execute("username", "password")

        # Assert
        self.assertEqual(result.data, expected_data)
        self.mock_external_service.fetch_data.assert_called_once_with("username", "password")

    def test_execute_failure(self):
        # Arrange
        self.mock_external_service.fetch_data.side_effect = Exception("API error")

        # Act & Assert
        with self.assertRaises(Exception):
            self.use_case.execute("username", "password")

if __name__ == "__main__":
    unittest.main()
