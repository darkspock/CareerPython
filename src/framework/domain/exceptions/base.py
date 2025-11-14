"""
Base exception classes for the AI Resume Enhancement Platform
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any


class DomainException(Exception):
    """Base exception for domain-related errors"""

    def __init__(
            self,
            message: str,
            error_code: Optional[str] = None,
            details: Optional[Dict[str, Any]] = None,
            correlation_id: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging and responses"""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp.isoformat(),
            "exception_type": self.__class__.__name__
        }


class ValidationException(DomainException):
    """Raised when input validation fails"""

    def __init__(
            self,
            message: str,
            field: Optional[str] = None,
            value: Optional[Any] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.field = field
        self.value = value
        if field:
            self.details.update({"field": field, "value": str(value) if value is not None else None})


class BusinessRuleException(DomainException):
    """Raised when business rules are violated"""

    def __init__(
            self,
            message: str,
            rule_name: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.rule_name = rule_name
        if rule_name:
            self.details.update({"rule_name": rule_name})


class EntityNotFoundException(DomainException):
    """Raised when an entity is not found"""

    def __init__(
            self,
            entity_type: str,
            entity_id: str,
            **kwargs: Any
    ):
        message = f"{entity_type} with id {entity_id} not found"
        super().__init__(message, **kwargs)
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.details.update({
            "entity_type": entity_type,
            "entity_id": entity_id
        })


class AuthenticationException(DomainException):
    """Raised when authentication fails"""

    def __init__(
            self,
            message: str = "Authentication failed",
            auth_method: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.auth_method = auth_method
        if auth_method:
            self.details.update({"auth_method": auth_method})


class AuthorizationException(DomainException):
    """Raised when authorization fails"""

    def __init__(
            self,
            message: str = "Access denied",
            required_permission: Optional[str] = None,
            resource: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.required_permission = required_permission
        self.resource = resource
        if required_permission:
            self.details.update({"required_permission": required_permission})
        if resource:
            self.details.update({"resource": resource})


class ConcurrencyException(DomainException):
    """Raised when concurrent operations conflict"""

    def __init__(
            self,
            message: str = "Concurrent operation conflict",
            resource_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.resource_id = resource_id
        if resource_id:
            self.details.update({"resource_id": resource_id})


class ExternalServiceException(DomainException):
    """Base exception for external service errors"""

    def __init__(
            self,
            message: str,
            service_name: str,
            operation: Optional[str] = None,
            retry_count: int = 0,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.service_name = service_name
        self.operation = operation
        self.retry_count = retry_count
        self.details.update({
            "service_name": service_name,
            "operation": operation,
            "retry_count": retry_count
        })


class ConfigurationException(DomainException):
    """Raised when configuration is invalid or missing"""

    def __init__(
            self,
            message: str,
            config_key: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.config_key = config_key
        if config_key:
            self.details.update({"config_key": config_key})
