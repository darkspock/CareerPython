"""Shared domain exceptions"""


class DomainException(Exception):
    """Base exception for domain-related errors"""
    pass


class AIProcessingException(DomainException):
    """Raised when AI service fails to process content"""

    def __init__(self, message: str, operation: str = None, retry_count: int = 0):
        super().__init__(message)
        self.operation = operation
        self.retry_count = retry_count


class AIServiceUnavailableException(AIProcessingException):
    """Raised when AI service is unavailable or not configured"""
    pass


class AIResponseParsingException(AIProcessingException):
    """Raised when AI service response cannot be parsed"""
    pass


class AITimeoutException(AIProcessingException):
    """Raised when AI service request times out"""
    pass


class ValidationException(DomainException):
    """Raised when input validation fails"""
    pass


class BusinessRuleException(DomainException):
    """Raised when business rules are violated"""
    pass


class EntityNotFoundException(DomainException):
    """Raised when an entity is not found"""
    pass
