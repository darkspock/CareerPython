"""
Shared FastAPI dependencies for company-scoped routes.
"""
from .company_context import (
    get_company_from_slug,
    get_optional_company_from_slug,
    validate_not_own_company_staff,
    require_company_staff,
    CompanyContext,
    CandidateCompanyContext,
    AdminCompanyContext,
)

__all__ = [
    "get_company_from_slug",
    "get_optional_company_from_slug",
    "validate_not_own_company_staff",
    "require_company_staff",
    "CompanyContext",
    "CandidateCompanyContext",
    "AdminCompanyContext",
]
