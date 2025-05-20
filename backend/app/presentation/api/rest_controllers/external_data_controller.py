import os
from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.fetch_odata_data import FetchODataDataUseCase
from app.adapters.api_clients.new_odata_api_client import NewODataAPIClient

from app.application.dtos.external_data_dto import ExternalDataError, ExternalDataResponse
from app.application.use_cases.fetch_external_data import FetchExternalDataUseCase
from app.infrastructure.di.container import DIContainer


class ExternalDataController:
    """Controller for external data-related endpoints."""
    
    def __init__(self, container: DIContainer):
        self.router = APIRouter()
        self.container = container
        self._configure_routes()
    
    def _configure_routes(self):
        self.router.add_api_route("/external/{api_type}", self.get_external_data, methods=["GET"])
        self.router.add_api_route("/odata", self.get_odata_data, methods=["GET"])
        self.router.add_api_route("/odata_new", self.get_odata_new_data, methods=["GET"])
    
    async def get_external_data(self, api_type: str):
        """Get data from an external API based on the provided type."""
        if api_type == "google":
            url = os.getenv("EXTERNAL_API_GOOGLE_URL", "https://google.com")
        elif api_type == "json":
            url = os.getenv("EXTERNAL_API_JSON_PLACEHOLDER_URL", "https://jsonplaceholder.typicode.com/posts/2")
        else:
            raise HTTPException(status_code=400, detail="Invalid api_type")
        
        use_case = self.container.get(FetchExternalDataUseCase)
        result = await use_case.execute(url)
        
        if isinstance(result, ExternalDataError):
            return {"error": result.error, "content": result.content if hasattr(result, 'content') else None}
        
        return result.data

    async def get_odata_data(self, odata_url: str, username: str, password: str):
        """Get data from an OData API."""
        client = NewODataAPIClient(odata_url, username, password)
        use_case = FetchODataDataUseCase(client)
        result = await use_case.execute()
        
        if isinstance(result, ExternalDataError):
            return {"error": result.error, "content": result.content if hasattr(result, 'content') else None}
        
        return result.data

    async def get_odata_new_data(self):
        """Get data from the OData API using hardcoded credentials."""
        odata_url = os.getenv("ODATA_WM_LDI_URL")
        username = os.getenv("CREDENTIALS_USERNAME")
        password = os.getenv("CREDENTIALS_PASSWORD")
        
        client = NewODataAPIClient(odata_url, username, password)
        use_case = FetchODataDataUseCase(client)
        result = await use_case.execute(endpoint="anp__field_reference_prices_gas__transform")  # Pass the endpoint from feedback
        
        if isinstance(result, ExternalDataError):
            return {"error": result.error, "content": result.content if hasattr(result, 'content') else None}
        
        return result.data
