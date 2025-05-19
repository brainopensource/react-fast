from app.domain.entities.message import Message


class GetGreetingUseCase:
    """Use case for retrieving a greeting message."""
    
    def execute(self) -> Message:
        """Get a greeting message."""
        return Message("Hello, World!")
