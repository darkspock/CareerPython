"""
Job position domain exceptions
"""

from src.shared.domain.exceptions import DomainException


class JobPositionNotFoundError(DomainException):
    """Raised when a job position is not found"""
    pass


class JobPositionValidationError(DomainException):
    """Raised when job position data validation fails"""
    pass


class JobPositionNotApprovedException(DomainException):
    """Raised when trying to perform actions on a non-approved job position"""
    pass


class JobPositionCompanyNotApprovedException(DomainException):
    """Raised when trying to create a job position for a non-approved company"""
    pass


class JobPositionNotFoundException(DomainException):
    """Raised when a job position is not found"""
    pass
