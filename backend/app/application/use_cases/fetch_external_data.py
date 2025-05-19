from typing import Union, Dict, Any

from app.domain.interfaces.http_interfaces.external_service import ExternalServiceInterface
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
