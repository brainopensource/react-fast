from app.adapters.http_adapters.http_client import HttpClient
from app.application.use_cases.fetch_external_data import FetchExternalDataUseCase
from app.application.use_cases.get_greeting import GetGreetingUseCase
from app.domain.interfaces.http_interfaces.external_service import ExternalServiceInterface


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
