class CustomError(Exception):
    """Custom error with optional message."""
    def __init__(self, message="Something went wrong", success=False, status_code=400, id=None):
        self.message = message
        self.success = success
        self.status_code = status_code
        self.id = id
        super().__init__(self.message)
        
class NotificationError(Exception):
    """Model error only returns success field."""
    def __init__(self, success=False, status_code=404, id=None):
        self.success = success
        self.status_code = status_code
        self.id = id
        super().__init__("Model error")