"""
Company context dependencies for FastAPI routes.

These dependencies provide company context and validation for company-scoped routes.
"""
import logging
from typing import Annotated, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import HTTPException, Depends, Path

from adapters.http.auth.schemas.user import UserResponse
from adapters.http.auth.services.authentication_service import get_current_user
from core.containers import Container
from src.company_bc.company.application.dtos.company_dto import CompanyDto
from src.company_bc.company.application.dtos.company_user_dto import CompanyUserDto
from src.company_bc.company.application.queries import GetCompanyBySlugQuery
from src.company_bc.company.application.queries.get_company_user_by_company_and_user import (
    GetCompanyUserByCompanyAndUserQuery
)
from src.framework.application.query_bus import QueryBus

log = logging.getLogger(__name__)


@inject
def get_company_from_slug(
    company_slug: Annotated[str, Path(description="Company URL slug")],
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> CompanyDto:
    """
    FastAPI dependency to get company from URL slug.

    Validates that the company exists and is active.

    Args:
        company_slug: The company slug from the URL path
        query_bus: Query bus for executing queries

    Returns:
        CompanyDto: The company data

    Raises:
        HTTPException 404: If company not found or inactive
    """
    query = GetCompanyBySlugQuery(slug=company_slug)
    company: Optional[CompanyDto] = query_bus.query(query)

    if not company:
        log.warning(f"Company not found for slug: {company_slug}")
        raise HTTPException(status_code=404, detail="Company not found")

    if company.status.upper() != "ACTIVE":
        log.warning(f"Company {company_slug} is not active: {company.status}")
        raise HTTPException(status_code=404, detail="Company not found")

    return company


@inject
def get_optional_company_from_slug(
    company_slug: Annotated[str, Path(description="Company URL slug")],
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> Optional[CompanyDto]:
    """
    FastAPI dependency to get company from URL slug (optional).

    Returns None if company not found instead of raising an exception.
    Useful for public routes where company context is optional.

    Args:
        company_slug: The company slug from the URL path
        query_bus: Query bus for executing queries

    Returns:
        Optional[CompanyDto]: The company data or None
    """
    query = GetCompanyBySlugQuery(slug=company_slug)
    return query_bus.query(query)


@inject
def validate_not_own_company_staff(
    company: Annotated[CompanyDto, Depends(get_company_from_slug)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> CompanyDto:
    """
    FastAPI dependency that validates the current user is NOT staff of the company.

    This is used for candidate routes where company staff members should not
    be able to access candidate functionality for their own company.

    Args:
        company: The company from the URL slug
        current_user: The authenticated user
        query_bus: Query bus for executing queries

    Returns:
        CompanyDto: The company data (pass-through if validation passes)

    Raises:
        HTTPException 403: If user is staff of this company
    """
    # Check if user is staff of this company
    query = GetCompanyUserByCompanyAndUserQuery(
        company_id=company.id,
        user_id=current_user.id
    )
    company_user: Optional[CompanyUserDto] = query_bus.query(query)

    if company_user:
        log.warning(
            f"Staff member {current_user.email} attempted to access candidate "
            f"portal for their own company {company.slug}"
        )
        raise HTTPException(
            status_code=403,
            detail="Staff members cannot access the candidate portal for their own company"
        )

    return company


@inject
def require_company_staff(
    company: Annotated[CompanyDto, Depends(get_company_from_slug)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> CompanyDto:
    """
    FastAPI dependency that requires the current user to be staff of the company.

    This is used for admin routes where only company staff should have access.

    Args:
        company: The company from the URL slug
        current_user: The authenticated user
        query_bus: Query bus for executing queries

    Returns:
        CompanyDto: The company data (pass-through if validation passes)

    Raises:
        HTTPException 403: If user is NOT staff of this company
    """
    # Check if user is staff of this company
    query = GetCompanyUserByCompanyAndUserQuery(
        company_id=company.id,
        user_id=current_user.id
    )
    company_user: Optional[CompanyUserDto] = query_bus.query(query)

    if not company_user:
        log.warning(
            f"Non-staff user {current_user.email} attempted to access admin "
            f"portal for company {company.slug}"
        )
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this company"
        )

    return company


@inject
def get_current_company_user(
    company: Annotated[CompanyDto, Depends(get_company_from_slug)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> CompanyUserDto:
    """
    FastAPI dependency that returns the company user record for the current user.

    This is used for admin routes that need the company_user_id for audit/tracking.

    Args:
        company: The company from the URL slug
        current_user: The authenticated user
        query_bus: Query bus for executing queries

    Returns:
        CompanyUserDto: The company user data

    Raises:
        HTTPException 403: If user is NOT staff of this company
    """
    from src.company_bc.company.application.dtos.company_user_dto import CompanyUserDto

    # Check if user is staff of this company
    query = GetCompanyUserByCompanyAndUserQuery(
        company_id=company.id,
        user_id=current_user.id
    )
    company_user: Optional[CompanyUserDto] = query_bus.query(query)

    if not company_user:
        log.warning(
            f"Non-staff user {current_user.email} attempted to access admin "
            f"portal for company {company.slug}"
        )
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this company"
        )

    return company_user


# Type aliases for cleaner dependency injection
CompanyContext = Annotated[CompanyDto, Depends(get_company_from_slug)]
CandidateCompanyContext = Annotated[CompanyDto, Depends(validate_not_own_company_staff)]
AdminCompanyContext = Annotated[CompanyDto, Depends(require_company_staff)]

CurrentCompanyUser = Annotated[CompanyUserDto, Depends(get_current_company_user)]
