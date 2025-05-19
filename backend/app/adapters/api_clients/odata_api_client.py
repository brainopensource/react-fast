from typing import Any
from app.domain.interfaces.http_interfaces.external_service import ExternalServiceInterface
import requests
from requests.auth import HTTPBasicAuth
import os

class ODataAPIClient(ExternalServiceInterface):
    def __init__(self, base_url: str, username: str = None, password: str = None):
        self.base_url = base_url
        if username is None:
            self.username = os.getenv("ODATA_USERNAME")
        else:
            self.username = username
        if password is None:
            self.password = os.getenv("ODATA_PASSWORD")
        else:
            self.password = password

    async def fetch_data(self, endpoint: str, username: str = None, password: str = None) -> Any:
        # URL encode the endpoint to handle special characters
        encoded_endpoint = requests.utils.quote(endpoint)
        # Create the full URL
        url = f"{self.base_url}/{encoded_endpoint}"
        
        # Use credentials from environment variables if not provided
        auth_username = username if username else self.username
        auth_password = password if password else self.password
        
        # Create the auth object with the password as is
        auth = HTTPBasicAuth(auth_username, auth_password)
        # Make the request
        response = requests.get(url, auth=auth)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response
