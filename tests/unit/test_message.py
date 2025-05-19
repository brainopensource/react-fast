import pytest
from backend.app.domain.entities.message import Message

def test_message_to_dict():
    # Arrange
    message = Message("test message")
    
    # Act
    result = message.to_dict()
    
    # Assert
    assert result == {"message": "test message"}
    assert isinstance(result, dict)
