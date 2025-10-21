"""Company domain module"""
from .entities import Company, CompanyUser
from .enums import CompanyStatus, CompanyUserRole, CompanyUserStatus
from .value_objects import CompanyId, CompanySettings
from .exceptions import (
    CompanyNotFoundError,
    CompanyAlreadyExistsError,
    CompanyValidationError,
    CompanyNotApprovedException
)

# Backward compatibility
CompanyStatusEnum = CompanyStatus

__all__ = [
    "Company",
    "CompanyUser",
    "CompanyStatus",
    "CompanyStatusEnum",  # Backward compatibility
    "CompanyUserRole",
    "CompanyUserStatus",
    "CompanyId",
    "CompanySettings",
    "CompanyNotFoundError",
    "CompanyAlreadyExistsError",
    "CompanyValidationError",
    "CompanyNotApprovedException"
]
