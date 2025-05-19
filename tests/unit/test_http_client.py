import pytest
import httpx
from abc import ABC, abstractmethod
from typing import Any, Dict

# Mock the interface locally for testing
class ExternalServiceInterface(ABC):
    @abstractmethod
    async def fetch_data(self, url: str) -> Dict[str, Any]:
        """Fetch data from an external service."""
        pass

# Local implementation for testing
class HttpClient(ExternalServiceInterface):
    """Implementation of the ExternalServiceInterface using httpx."""
    
    async def fetch_data(self, url: str) -> Dict[str, Any]:
        """Fetch data from an external HTTP service."""
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            if response.headers.get("Content-Type", "").startswith("application/json"):
                return response.json()
            else:
                return {"content": response.text}

@pytest.mark.asyncio
async def test_http_client_json_response():
    # Arrange
    client = HttpClient()
    test_url = "https://jsonplaceholder.typicode.com/posts/1"
    
    # Act
    result = await client.fetch_data(test_url)
    
    # Assert
    assert isinstance(result, dict)
    assert "id" in result
    assert "title" in result
    assert "body" in result

@pytest.mark.asyncio
async def test_http_client_text_response():
    # Arrange
    client = HttpClient()
    test_url = "https://example.com"  # Returns HTML
    
    # Act
    result = await client.fetch_data(test_url)
    
    # Assert
    assert isinstance(result, dict)
    assert "content" in result
    assert isinstance(result["content"], str)
    assert "Example Domain" in result["content"]

@pytest.mark.asyncio
async def test_http_client_error():
    # Arrange
    client = HttpClient()
    test_url = "https://httpstat.us/404"  # Will return 404
    
    # Act & Assert
    with pytest.raises(httpx.HTTPStatusError):
        await client.fetch_data(test_url)
