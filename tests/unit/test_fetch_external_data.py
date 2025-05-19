import pytest
from unittest.mock import AsyncMock, MagicMock
from backend.app.application.use_cases.fetch_external_data import FetchExternalDataUseCase
from backend.app.domain.interfaces.http_interfaces.external_service import ExternalServiceInterface
from backend.app.application.dtos.external_data_dto import ExternalDataResponse, ExternalDataError

@pytest.fixture
def external_service_mock():
    return MagicMock(spec=ExternalServiceInterface)

@pytest.fixture
def fetch_external_data_use_case(external_service_mock):
    return FetchExternalDataUseCase(external_service=external_service_mock)

@pytest.mark.asyncio
async def test_fetch_data_success(fetch_external_data_use_case, external_service_mock):
    # Arrange
    url = "http://example.com/data"
    mock_data = {"key": "value"}
    external_service_mock.fetch_data = AsyncMock(return_value=mock_data)

    # Act
    result = await fetch_external_data_use_case.execute(url)

    # Assert
    assert isinstance(result, ExternalDataResponse)
    assert result.data == mock_data
    assert result.source_url == url
    external_service_mock.fetch_data.assert_called_once_with(url)

@pytest.mark.asyncio
async def test_fetch_data_failure(fetch_external_data_use_case, external_service_mock):
    # Arrange
    url = "http://example.com/data"
    error_message = "Network error"
    external_service_mock.fetch_data = AsyncMock(side_effect=Exception(error_message))

    # Act
    result = await fetch_external_data_use_case.execute(url)

    # Assert
    assert isinstance(result, ExternalDataError)
    assert result.error == f"Failed to fetch data: {error_message}"
    assert result.content is None
    assert result.source_url == url
    external_service_mock.fetch_data.assert_called_once_with(url)
