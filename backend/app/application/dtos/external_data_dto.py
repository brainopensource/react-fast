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
