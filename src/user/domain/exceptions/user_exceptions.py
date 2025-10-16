from typing import Any

from src.shared.domain.exceptions import DomainException


class UserException(DomainException):
    """Base exception for user-related errors"""
    pass


class EmailAlreadyExistException(UserException):
    """Raised when the email already exists"""

    def __init__(
            self,
            email: str,
            **kwargs: Any
    ):
        message = f"Email already exists: {email}"
        super().__init__(message, **kwargs)


class UserNotFoundError(UserException):
    """Raised when a user is not found"""

    def __init__(
            self,
            user_id: str,
            **kwargs: Any
    ):
        message = f"User not found: {user_id}"
        super().__init__(message, **kwargs)
