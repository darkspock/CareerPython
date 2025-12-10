"""
Job position domain exceptions
"""
from typing import Optional

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


class JobPositionInvalidStatusTransitionError(DomainException):
    """Raised when an invalid status transition is attempted"""
    def __init__(self, current_status: str, target_status: str, message: Optional[str] = None):
        self.current_status = current_status
        self.target_status = target_status
        super().__init__(
            message or f"Invalid status transition from '{current_status}' to '{target_status}'"
        )


class JobPositionFieldLockedError(DomainException):
    """Raised when trying to modify a locked field"""
    def __init__(self, field_name: str, current_status: str, message: Optional[str] = None):
        self.field_name = field_name
        self.current_status = current_status
        super().__init__(
            message or f"Field '{field_name}' cannot be modified in status '{current_status}'"
        )


class JobPositionBudgetExceededError(DomainException):
    """Raised when salary exceeds budget limit"""
    def __init__(self, salary_max: str, budget_max: str, message: Optional[str] = None):
        self.salary_max = salary_max
        self.budget_max = budget_max
        super().__init__(
            message or f"Salary maximum ({salary_max}) exceeds budget limit ({budget_max})"
        )


class JobPositionInvalidScreeningTemplateError(DomainException):
    """Raised when screening template is invalid or has wrong scope"""
    def __init__(self, template_id: str, reason: str, message: Optional[str] = None):
        self.template_id = template_id
        self.reason = reason
        super().__init__(
            message or f"Invalid screening template '{template_id}': {reason}"
        )
