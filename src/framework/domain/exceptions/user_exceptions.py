"""
User and authentication-related domain exceptions
"""
from typing import Optional, Any

from .base import (
    DomainException,
    ValidationException,
    AuthenticationException,
    BusinessRuleException
)


class UserException(DomainException):
    """Base exception for user-related errors"""

    def __init__(
            self,
            message: str,
            user_id: Optional[str] = None,
            email: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if user_id:
            self.details.update({"user_id": user_id})
        if email:
            self.details.update({"email": email})


class UserAlreadyExistsException(UserException):
    """Raised when attempting to create a user that already exists"""

    def __init__(
            self,
            email: str,
            **kwargs: Any
    ):
        message = f"User with email {email} already exists"
        super().__init__(message, email=email, **kwargs)


class UserNotFoundException(UserException):
    """Raised when user is not found"""

    def __init__(
            self,
            identifier: str,
            identifier_type: str = "id",
            **kwargs: Any
    ):
        message = f"User not found with {identifier_type}: {identifier}"
        super().__init__(message, **kwargs)
        self.details.update({
            "identifier": identifier,
            "identifier_type": identifier_type
        })


class UserNotActiveException(UserException):
    """Raised when user account is not active"""

    def __init__(
            self,
            message: str = "User account is not active",
            user_status: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if user_status:
            self.details.update({"user_status": user_status})


class InvalidCredentialsException(AuthenticationException):
    """Raised when user credentials are invalid"""

    def __init__(
            self,
            message: str = "Invalid credentials provided",
            **kwargs: Any
    ):
        super().__init__(message, auth_method="password", **kwargs)


class PasswordValidationException(ValidationException):
    """Raised when password validation fails"""

    def __init__(
            self,
            message: str,
            validation_rules: Optional[list] = None,
            **kwargs: Any
    ):
        super().__init__(message, field="password", **kwargs)
        if validation_rules:
            self.details.update({"validation_rules": validation_rules})


class EmailValidationException(ValidationException):
    """Raised when email validation fails"""

    def __init__(
            self,
            message: str,
            email: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, field="email", value=email, **kwargs)


class TokenException(AuthenticationException):
    """Base exception for token-related errors"""

    def __init__(
            self,
            message: str,
            token_type: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if token_type:
            self.details.update({"token_type": token_type})


class InvalidTokenException(TokenException):
    """Raised when token is invalid or malformed"""

    def __init__(
            self,
            message: str = "Invalid token provided",
            token_type: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, token_type=token_type, **kwargs)


class ExpiredTokenException(TokenException):
    """Raised when token has expired"""

    def __init__(
            self,
            message: str = "Token has expired",
            token_type: Optional[str] = None,
            expired_at: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, token_type=token_type, **kwargs)
        if expired_at:
            self.details.update({"expired_at": expired_at})


class PasswordResetException(UserException):
    """Raised when password reset fails"""

    def __init__(
            self,
            message: str,
            reset_stage: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if reset_stage:
            self.details.update({"reset_stage": reset_stage})


class AccountLockedException(UserException):
    """Raised when user account is locked"""

    def __init__(
            self,
            message: str = "User account is locked",
            lock_reason: Optional[str] = None,
            unlock_time: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if lock_reason:
            self.details.update({"lock_reason": lock_reason})
        if unlock_time:
            self.details.update({"unlock_time": unlock_time})


class ProfileIncompleteException(BusinessRuleException):
    """Raised when user profile is incomplete for operation"""

    def __init__(
            self,
            message: str = "User profile is incomplete",
            missing_fields: Optional[list] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if missing_fields:
            self.details.update({"missing_fields": missing_fields})
