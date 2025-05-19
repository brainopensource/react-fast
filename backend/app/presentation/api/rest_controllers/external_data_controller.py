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
        self.router.add_api_route("/external", self.get_external_data, methods=["GET"])
        self.router.add_api_route("/external_2", self.get_external_data_2, methods=["GET"])
    
    async def get_external_data(self):
        """Get data from an external API (Google)."""
        use_case = self.container.get(FetchExternalDataUseCase)
        result = await use_case.execute("https://google.com")
        
        if isinstance(result, ExternalDataError):
            return {"error": result.error, "content": result.content}
        
        return result.data
    
    async def get_external_data_2(self):
        """Get data from JSON Placeholder API."""
        use_case = self.container.get(FetchExternalDataUseCase)
        result = await use_case.execute("https://jsonplaceholder.typicode.com/posts/2")
        
        if isinstance(result, ExternalDataError):
            return {"error": result.error}
        
        return result.data
