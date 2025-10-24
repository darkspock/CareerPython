"""
Company domain exceptions
"""

from src.shared.domain.exceptions import DomainException


class CompanyNotFoundError(DomainException):
    """Raised when a company is not found"""
    pass


class CompanyAlreadyExistsError(DomainException):
    """Raised when trying to create a company that already exists"""
    pass


class CompanyValidationError(DomainException):
    """Raised when company data validation fails"""
    pass


class CompanyDomainAlreadyExistsError(DomainException):
    """Raised when trying to create a company domain that already exists"""
    pass


class CompanyNotApprovedException(DomainException):
    """Raised when trying to perform actions on a non-approved company"""
    pass


class CompanyNotFoundException(DomainException):
    """Raised when a company is not found"""
    pass


class CompanyHasActiveJobPositionsException(DomainException):
    """Raised when trying to delete a company that has active job positions"""
    pass
