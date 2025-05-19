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
