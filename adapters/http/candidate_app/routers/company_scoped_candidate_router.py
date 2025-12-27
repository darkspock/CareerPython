"""
Company-scoped candidate routes.

All routes in this router require a company_slug in the URL path.
Staff members of a company cannot access these routes for their own company.

These routes handle company-specific candidate actions:
- Viewing positions at a company
- Applying to positions at a company
- Viewing applications to a company

Note: Profile routes (experience, education, projects) remain global
because a candidate's CV is the same regardless of which company they apply to.
"""
import logging
from typing import Annotated, Any, List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from adapters.http.auth.schemas.user import UserResponse
from adapters.http.auth.services.authentication_service import get_current_user
from adapters.http.candidate_app.schemas.candidate_job_applications import (
    CandidateJobApplicationSummary,
    JobApplicationListFilters,
)
from adapters.http.shared.dependencies.company_context import (
    CandidateCompanyContext,
    CompanyContext,
)
from core.containers import Container
from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.company_bc.company.application.dtos.company_dto import CompanyDto
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus

log = logging.getLogger(__name__)

# Router with company_slug prefix
router = APIRouter(
    prefix="/{company_slug}/candidate",
    tags=["Company-Scoped Candidate"],
)


@router.get("/company-info")
@inject
def get_company_info(
    company: CompanyContext,
) -> dict:
    """
    Get public company information.

    This endpoint is accessible without authentication.
    Returns basic company info for the candidate portal.
    """
    return {
        "id": company.id,
        "name": company.name,
        "slug": company.slug,
        "logo_url": company.logo_url,
    }


@router.get("/me")
@inject
def get_my_profile_for_company(
    company: CandidateCompanyContext,  # This validates user is NOT staff
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> dict:
    """
    Get the authenticated user's candidate profile for this company.

    Staff members of this company cannot access this endpoint.
    They must use a different company's candidate portal.

    Returns:
        Candidate profile information
    """
    from src.candidate_bc.candidate.application import GetCandidateByUserIdQuery
    from src.auth_bc.user.domain.value_objects import UserId

    # Get candidate profile
    query = GetCandidateByUserIdQuery(UserId.from_string(current_user.id))
    candidate: Optional[Any] = query_bus.query(query)

    if not candidate:
        # Don't auto-create - return 404
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found. Please complete your profile first."
        )

    return {
        "candidate_id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "company_context": {
            "company_id": company.id,
            "company_name": company.name,
            "company_slug": company.slug,
        }
    }


@router.get("/positions")
@inject
def list_company_positions(
    company: CompanyContext,
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> dict:
    """
    List open positions for this company.

    This endpoint is public - no authentication required.
    """
    from src.company_bc.job_position.application.queries.list_published_job_positions import (
        ListPublishedJobPositionsQuery
    )
    from src.company_bc.company.domain import CompanyId

    query = ListPublishedJobPositionsQuery(company_id=CompanyId.from_string(company.id))
    positions: List[Any] = query_bus.query(query) or []

    return {
        "company": {
            "id": company.id,
            "name": company.name,
            "slug": company.slug,
        },
        "positions": positions or [],
        "total": len(positions) if positions else 0,
    }


@router.get("/applications", response_model=List[CandidateJobApplicationSummary])
@inject
def list_my_applications_for_company(
    company: CandidateCompanyContext,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
    status: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[CandidateJobApplicationSummary]:
    """
    List the authenticated user's applications to this company.

    Staff members of this company cannot access this endpoint.
    Returns only applications to positions belonging to this company.
    """
    from adapters.http.candidate_app.controllers.application_controller import ApplicationController
    from src.candidate_bc.candidate.application import GetCandidateByUserIdQuery
    from src.auth_bc.user.domain.value_objects import UserId

    # Get candidate profile
    query = GetCandidateByUserIdQuery(UserId.from_string(current_user.id))
    candidate: Optional[Any] = query_bus.query(query)

    if not candidate:
        return []

    # Get applications filtered by company
    filters = JobApplicationListFilters(
        status=ApplicationStatusEnum(status) if status else None,
        limit=limit,
        company_id=company.id  # Filter by this company
    )

    from core.containers import Container as ContainerRef
    controller = ContainerRef.application_controller()
    applications: List[CandidateJobApplicationSummary] = controller.get_applications_by_candidate(candidate.id, filters)
    return applications


@router.post("/apply/{position_id}", status_code=201)
@inject
def apply_to_position(
    position_id: str,
    company: CandidateCompanyContext,  # Validates user is NOT staff of this company
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
    command_bus: Annotated[CommandBus, Depends(Provide[Container.command_bus])],
    cover_letter: Optional[str] = None,
) -> dict:
    """
    Apply to a position at this company.

    Staff members of this company cannot apply to their own company's positions.
    This endpoint validates that:
    1. The user is not staff of this company
    2. The position belongs to this company
    3. The user has a candidate profile
    """
    from src.candidate_bc.candidate.application import GetCandidateByUserIdQuery
    from src.auth_bc.user.domain.value_objects import UserId
    from src.company_bc.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
    from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId

    # Verify position belongs to this company
    position: Optional[Any] = query_bus.query(GetJobPositionByIdQuery(id=JobPositionId.from_string(position_id)))
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    if str(position.company_id) != company.id:
        raise HTTPException(
            status_code=400,
            detail="Position does not belong to this company"
        )

    # Get or verify candidate profile exists
    query = GetCandidateByUserIdQuery(UserId.from_string(current_user.id))
    candidate: Optional[Any] = query_bus.query(query)

    if not candidate:
        raise HTTPException(
            status_code=400,
            detail="Please complete your candidate profile before applying"
        )

    # Create the application
    from src.company_bc.candidate_application.application.commands.create_candidate_application import (
        CreateCandidateApplicationCommand
    )

    try:
        command = CreateCandidateApplicationCommand(
            candidate_id=str(candidate.id),
            job_position_id=position_id,
            notes=cover_letter or ""
        )
        command_bus.dispatch(command)

        log.info(
            f"Application created: candidate={candidate.id}, "
            f"position={position_id}, company={company.slug}"
        )

        return {
            "message": "Application submitted successfully",
            "position_id": position_id,
            "company": {
                "id": company.id,
                "name": company.name,
                "slug": company.slug,
            }
        }
    except Exception as e:
        log.error(f"Failed to create application: {e}")
        raise HTTPException(status_code=400, detail=str(e))
