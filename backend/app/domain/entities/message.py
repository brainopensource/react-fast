class Message:
    """A simple message entity."""
    
    def __init__(self, content: str):
        self.content = content
    
    def to_dict(self) -> dict:
        return {"message": self.content}
