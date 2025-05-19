# Adding a New Feature: Practical Guide

This guide outlines the steps to add a new feature (e.g., a new endpoint `/external_3` that interacts with an OData service using Basic Authentication) to a FastAPI application, adhering to **SOLID**, **DDD**, and **Hexagonal Architecture** principles.

---

## 1. Define Domain Interface (Core Layer)

Create an interface (e.g., `External3ServiceInterface`) in `app/domain/interfaces/http_interfaces/`.

This interface defines the contract for interacting with the external service, focusing on the domain concepts, not the technical details (e.g., OData, HTTP).

```python
# app/domain/interfaces/http_interfaces/external_3_service.py
from abc import ABC, abstractmethod
from typing import Dict

class External3ServiceInterface(ABC):
    @abstractmethod
    async def get_external_3_data(self) -> Dict:
        """
        Fetches data from the External 3 service.
        """
        raise NotImplementedError
```

---

## 2. Implement the Adapter (Infrastructure Layer)

Create a new adapter (e.g., `ODataHttpClient`) in `app/adapters/http_adapters/` that implements the domain interface.

This adapter handles the specifics of interacting with the external service, such as:
- Making OData requests
- Handling Basic Authentication (username/password)
- Parsing the response and checking the status code

```python
# app/adapters/http_adapters/odata_http_client.py
import httpx
from app.domain.interfaces.http_interfaces.external_3_service import External3ServiceInterface
from typing import Dict
from fastapi import HTTPException

class ODataHttpClient(External3ServiceInterface):
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.client = httpx.AsyncClient(
            base_url=base_url,
            auth=httpx.BasicAuth(username, password)
        )

    async def get_external_3_data(self) -> Dict:
        response = await self.client.get("/some_odata_endpoint")  # Example endpoint
        response.raise_for_status()  # Raise exception for bad status
        data = response.json()
        if "error" in data:
            raise HTTPException(status_code=400, detail=f"External service error: {data['error']}")
        return data
```

---

## 3. Create a Use Case (Application Layer)

Add a new use case (e.g., `FetchExternal3DataUseCase`) in `app/application/use_cases/` that orchestrates the interaction with the adapter to fulfill the business logic.

Use cases should depend on domain interfaces, not concrete adapters.

```python
# app/application/use_cases/fetch_external_3_data_use_case.py
from app.domain.interfaces.http_interfaces.external_3_service import External3ServiceInterface
from typing import Dict

class FetchExternal3DataUseCase:
    def __init__(self, external_3_service: External3ServiceInterface):
        self.external_3_service = external_3_service

    async def execute(self) -> Dict:
        """
        Fetches and processes data from the external service.
        """
        data = await self.external_3_service.get_external_3_data()
        # Add any business logic here (e.g., data transformation)
        return data
```

---

## 4. Register in the Dependency Injection Container (Infrastructure Layer)

Update `container.py` to register the new adapter and use case. This is where we "wire up" the dependencies.

```python
# container.py
from dependency_injector import containers, providers
from app.adapters.http_adapters.odata_http_client import ODataHttpClient
from app.application.use_cases.fetch_external_3_data_use_case import FetchExternal3DataUseCase

class Container(containers.DeclarativeContainer):
    # ... other dependencies ...

    external_3_service = providers.Factory(
        ODataHttpClient,
        base_url=config.EXTERNAL_3_BASE_URL,  # Example from config
        username=config.EXTERNAL_3_USERNAME,
        password=config.EXTERNAL_3_PASSWORD,
    )

    fetch_external_3_data_use_case = providers.Factory(
        FetchExternal3DataUseCase,
        external_3_service=external_3_service,
    )
```

---

## 5. Add an API Endpoint (Presentation Layer)

In `app/presentation/api/rest_controllers/`, add a new controller or route for `/external_3` that:
- Gets the use case from the DI container
- Calls the use case's `execute()` method
- Returns the result

```python
# app/presentation/api/rest_controllers/external_data_controller.py
from fastapi import APIRouter, Depends
from container import Container  # Import your DI Container
from typing import Dict

router = APIRouter()

@router.get("/external_3", response_model=Dict)
async def get_external_3_data(
    container: Container = Depends(Container)
) -> Dict:
    """
    Endpoint to retrieve data from External 3.
    """
    use_case = container.fetch_external_3_data_use_case()
    data = await use_case.execute()
    return data
```

---

## 6. Configuration (Infrastructure Layer)

- Store sensitive credentials (username, password, API keys) securely, preferably outside the codebase.
- Use environment variables, a dedicated configuration file, or a secrets management solution.
- Inject the configuration values into the adapter (e.g., `ODataHttpClient`) via the DI container, as shown in the `container.py` example.

---

This approach adheres to **SOLID**, **DDD**, and **Hexagonal Architecture**, resulting in a modular, testable, and maintainable codebase.