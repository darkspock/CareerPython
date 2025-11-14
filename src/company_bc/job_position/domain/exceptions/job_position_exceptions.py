"""
Job position domain exceptions
"""

from src.framework.domain.exceptions import DomainException


class JobPositionNotFoundError(DomainException):
    """Raised when a job position is not found"""
    pass


class JobPositionValidationError(DomainException):
    """Raised when job position data validation fails"""
    pass


class JobPositionNotApprovedException(DomainException):
    """Raised when trying to perform actions on a job position that is not in the correct status"""
    # Note: Kept for backward compatibility, but the concept of "approved" no longer exists
    # New statuses: draft, active, paused, closed, archived
    pass


class JobPositionCompanyNotApprovedException(DomainException):
    """Raised when trying to create a job position for a non-approved company"""
    pass


class JobPositionNotFoundException(DomainException):
    """Raised when a job position is not found"""
    pass
