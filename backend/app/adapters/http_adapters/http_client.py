import json
from typing import Any, Dict

import httpx

from app.domain.interfaces.http_interfaces.external_service import ExternalServiceInterface


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
