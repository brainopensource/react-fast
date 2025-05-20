import pytest
from fastapi.testclient import TestClient
from app.main import app  # Assuming the FastAPI app is defined in main.py
from unittest.mock import patch

@pytest.fixture
def client():
    return TestClient(app)

def test_get_odata_data(client):
    odata_url = "https://example.com/odata"
    username = "test_user"
    password = "test_password"

    with patch('app.adapters.api_clients.new_odata_api_client.NewODataAPIClient') as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.fetch_data.return_value.json.return_value = {"data": "mocked data"}

        response = client.get("/odata", params={"odata_url": odata_url, "username": username, "password": password})

        assert response.status_code == 200
        assert response.json() == {"data": "mocked data"}
