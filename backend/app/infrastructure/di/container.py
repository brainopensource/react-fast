from app.adapters.http_adapters.http_client import HttpClient
from dotenv import load_dotenv
import os
from app.application.use_cases.fetch_external_data import FetchExternalDataUseCase
from app.application.use_cases.get_greeting import GetGreetingUseCase
from app.application.use_cases.fetch_odata_data import FetchODataDataUseCase
from app.adapters.api_clients.odata_api_client import ODataAPIClient
from app.adapters.api_clients.new_odata_api_client import NewODataAPIClient
from app.domain.interfaces.http_interfaces.external_service import ExternalServiceInterface

class DIContainer:
    """Simple dependency injection container."""
    
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self._services = {}
        self._register_services()

    def _register_services(self):
        # Register adapters
        self._services[ExternalServiceInterface] = HttpClient()
        self._services[NewODataAPIClient] = NewODataAPIClient(
            url=os.getenv("ODATA_WM_LDI_URL"),
            username=os.getenv("CREDENTIALS_USERNAME"),
            password=os.getenv("CREDENTIALS_PASSWORD")
        )
        
        # Register use cases
        self._services[GetGreetingUseCase] = GetGreetingUseCase()
        self._services[FetchExternalDataUseCase] = FetchExternalDataUseCase(
            external_service=self.get(ExternalServiceInterface)
        )
        self._services[FetchODataDataUseCase] = FetchODataDataUseCase(
            api_client=self.get(NewODataAPIClient)
        )
    
    def get(self, service_type):
        """Get a service from the container."""
        return self._services.get(service_type)
