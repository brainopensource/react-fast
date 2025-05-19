from typing import Any
import os
from app.application.dtos.external_data_dto import ExternalDataResponse
from app.domain.interfaces.http_interfaces.external_service import ExternalServiceInterface

class FetchODataData:
    def __init__(self, external_service: ExternalServiceInterface):
        self.external_service = external_service

    async def execute(self, endpoint: str) -> ExternalDataResponse:
        # Get credentials from environment variables
        username = os.getenv("CREDENTIALS_USERNAME")
        password = os.getenv("CREDENTIALS_PASSWORD")
        
        response = await self.external_service.fetch_data(endpoint, username, password)
        return ExternalDataResponse(data=response, source_url=os.getenv("ODATA_WM_LDI_URL"))  # Use the actual OData API URL from the environment variable
