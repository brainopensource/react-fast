# Ideas to implement, don use yet

# backend/app/domain/interfaces/data_transfer/external_service.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ExternalServiceInterface(ABC):
    """Interface for external service communication."""
    
    @abstractmethod
    async def fetch_data(self, url: str) -> Dict[str, Any]:
        """Fetch data from an external service."""
        pass


# backend/app/domain/entities/message.py
class Message:
    """A simple message entity."""
    
    def __init__(self, content: str):
        self.content = content
    
    def to_dict(self) -> dict:
        return {"message": self.content}


# backend/app/application/dtos/external_data_dto.py
from typing import Any, Dict, Optional
from pydantic import BaseModel


class ExternalDataResponse(BaseModel):
    """DTO for external data responses."""
    data: Dict[str, Any]
    source_url: str


class ExternalDataError(BaseModel):
    """DTO for external data errors."""
    error: str
    content: Optional[str] = None
    source_url: str


# backend/app/application/use_cases/get_greeting.py
from app.domain.entities.message import Message


class GetGreetingUseCase:
    """Use case for retrieving a greeting message."""
    
    def execute(self) -> Message:
        """Get a greeting message."""
        return Message("Hello, World!")


# backend/app/application/use_cases/fetch_external_data.py
from typing import Union, Dict, Any

from app.domain.interfaces.data_transfer.external_service import ExternalServiceInterface
from app.application.dtos.external_data_dto import ExternalDataResponse, ExternalDataError


class FetchExternalDataUseCase:
    """Use case for fetching data from external sources."""
    
    def __init__(self, external_service: ExternalServiceInterface):
        self.external_service = external_service
    
    async def execute(self, url: str) -> Union[ExternalDataResponse, ExternalDataError]:
        """Fetch data from an external URL."""
        try:
            data = await self.external_service.fetch_data(url)
            return ExternalDataResponse(data=data, source_url=url)
        except Exception as e:
            return ExternalDataError(
                error=f"Failed to fetch data: {str(e)}",
                content=None,
                source_url=url
            )


# backend/app/adapters/data_transfer/http_client.py
import json
from typing import Any, Dict

import httpx

from app.domain.interfaces.data_transfer.external_service import ExternalServiceInterface


class HttpClient(ExternalServiceInterface):
    """Implementation of the ExternalServiceInterface using httpx."""
    
    async def fetch_data(self, url: str) -> Dict[str, Any]:
        """Fetch data from an external HTTP service."""
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            
            if response.headers.get("Content-Type", "").startswith("application/json"):
                return response.json()
            else:
                return {"content": response.text}


# backend/app/infrastructure/di/container.py
from app.adapters.data_transfer.http_client import HttpClient
from app.application.use_cases.fetch_external_data import FetchExternalDataUseCase
from app.application.use_cases.get_greeting import GetGreetingUseCase
from app.domain.interfaces.data_transfer.external_service import ExternalServiceInterface


class DIContainer:
    """Simple dependency injection container."""
    
    def __init__(self):
        self._services = {}
        self._register_services()
    
    def _register_services(self):
        # Register adapters
        self._services[ExternalServiceInterface] = HttpClient()
        
        # Register use cases
        self._services[GetGreetingUseCase] = GetGreetingUseCase()
        self._services[FetchExternalDataUseCase] = FetchExternalDataUseCase(
            external_service=self.get(ExternalServiceInterface)
        )
    
    def get(self, service_type):
        """Get a service from the container."""
        return self._services.get(service_type)


# backend/app/presentation/api/rest_controllers/greeting_controller.py
from fastapi import APIRouter, Depends

from app.application.use_cases.get_greeting import GetGreetingUseCase
from app.infrastructure.di.container import DIContainer


class GreetingController:
    """Controller for greeting-related endpoints."""
    
    def __init__(self, container: DIContainer):
        self.router = APIRouter()
        self.container = container
        self._configure_routes()
    
    def _configure_routes(self):
        self.router.add_api_route("/", self.get_greeting, methods=["GET"])
    
    def get_greeting(self):
        """Get a greeting message."""
        use_case = self.container.get(GetGreetingUseCase)
        message = use_case.execute()
        return message.to_dict()


# backend/app/presentation/api/rest_controllers/external_data_controller.py
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


# backend/app/presentation/api/api_setup.py
from fastapi import FastAPI

from app.infrastructure.di.container import DIContainer
from app.presentation.api.rest_controllers.external_data_controller import ExternalDataController
from app.presentation.api.rest_controllers.greeting_controller import GreetingController


def setup_api(app: FastAPI, container: DIContainer):
    """Configure the FastAPI application with all controllers."""
    # Initialize controllers
    greeting_controller = GreetingController(container)
    external_data_controller = ExternalDataController(container)
    
    # Include routers
    app.include_router(greeting_controller.router, tags=["greetings"])
    app.include_router(external_data_controller.router, tags=["external_data"])


# backend/main.py
import asyncio
from fastapi import FastAPI

from app.infrastructure.di.container import DIContainer
from app.presentation.api.api_setup import setup_api


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Hexagonal FastAPI App")
    
    # Create the DI container
    container = DIContainer()
    
    # Setup API routes
    setup_api(app, container)
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)