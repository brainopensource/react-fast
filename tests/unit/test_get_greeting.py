import pytest
from backend.app.application.use_cases.get_greeting import GetGreetingUseCase
from backend.app.domain.entities.message import Message

def test_get_greeting():
    # Arrange
    get_greeting_use_case = GetGreetingUseCase()

    # Act
    result = get_greeting_use_case.execute()

    # Assert
    assert isinstance(result, Message)
    assert result.content == "Hello, World!"
