class OpenF1PyException(Exception):
    """
    Base class for all exceptions raised by OpenF1Py.
    """

class APIError(OpenF1PyException):
    """
    Raised when an error occurs while interacting with the OpenF1 API.
    """
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"{status_code}: {message}")