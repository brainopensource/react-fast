import os
from fastapi import APIRouter, Depends, HTTPException

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

    # get_external_data_2 has been consolidated into get_external_data
