from http import HTTPStatus


class TorpedoException(Exception):
    """Exceptions that can be turned into HTTP responses"""

    error: str = "Something went wrong"
    status_code: int = HTTPStatus.BAD_REQUEST

    def __init__(self, error: str, status_code: int):
        self.error = error
        self.status_code = status_code


class NoSuchUserException(TorpedoException):
    def __init__(self, error: str):
        super().__init__(error, HTTPStatus.NOT_FOUND)


class AuthException(TorpedoException):
    def __init__(self, error: str, status_code: int):
        super().__init__(error, status_code)
