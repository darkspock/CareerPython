"""Company domain module"""
from .entities import Company, CompanyUser
from .enums import CompanyStatusEnum, CompanyUserRole, CompanyUserStatus
from .exceptions import (
    CompanyNotFoundError,
    CompanyAlreadyExistsError,
    CompanyValidationError,
    CompanyNotApprovedException
)
from .value_objects import CompanyId, CompanySettings

# Backward compatibility
CompanyStatusEnum = CompanyStatusEnum

__all__ = [
    "Company",
    "CompanyUser",
    "CompanyStatusEnum",
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
