"""
Public Position Router
Phase 10: REST API endpoints for public job positions (no auth required for browsing)
"""
from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Query

from core.container import Container
from src.company_bc.job_position.domain.exceptions import JobPositionNotFoundError
from adapters.http.company_app.job_position.controllers.public_position_controller import PublicPositionController
from adapters.http.company_app.job_position.schemas.public_position_schemas import (
    PublicPositionResponse,
    PublicPositionListResponse,
    SubmitApplicationRequest,
    SubmitApplicationResponse
)

router = APIRouter(prefix="/public/positions", tags=["public-positions"])


@router.get(
    "",
    response_model=PublicPositionListResponse,
    summary="List public job positions",
    description="Browse all public job positions. No authentication required. Only returns positions with visibility=PUBLIC."
)
@inject
def list_public_positions(
        search: Optional[str] = Query(None, description="Search term for title/description"),
        page: int = Query(1, ge=1, description="Page number (1-indexed)"),
        page_size: int = Query(12, ge=1, le=100, description="Items per page"),
        controller: PublicPositionController = Depends(Provide[Container.public_position_controller])
) -> PublicPositionListResponse:
    """
    List public job positions with optional filters - simplified

    No authentication required. Only returns positions with visibility=PUBLIC.
    Custom fields are filtered to show only those visible to candidates based on workflow/stage configuration.

    Args:
        search: Search keyword in title/description
        page: Page number
        page_size: Number of items per page

    Returns:
        PublicPositionListResponse with positions and pagination info
    """
    try:
        return controller.list_public_positions(
            search=search,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list public positions: {str(e)}"
        )


@router.get(
    "/{slug_or_id}",
    response_model=PublicPositionResponse,
    summary="Get public job position details",
    description="Get detailed information about a public job position by slug or ID. No authentication required."
)
@inject
def get_public_position(
        slug_or_id: str,
        controller: PublicPositionController = Depends(Provide[Container.public_position_controller])
) -> PublicPositionResponse:
    """
    Get a single public job position by slug or ID

    No authentication required. Only returns positions with visibility=PUBLIC.
    Custom fields are filtered to show only those visible to candidates based on workflow/stage configuration.

    Args:
        slug_or_id: Position public slug or ID

    Returns:
        PublicPositionResponse with only visible fields for candidates

    Raises:
        404: If position not found or not public
    """
    try:
        return controller.get_public_position(slug_or_id)
    except JobPositionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get public position: {str(e)}"
        )


@router.post(
    "/{slug_or_id}/apply",
    response_model=SubmitApplicationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit application to position",
    description="Submit an application to a public job position. Requires candidate authentication."
)
@inject
def submit_application(
        slug_or_id: str,
        request: SubmitApplicationRequest,
        controller: PublicPositionController = Depends(Provide[Container.public_position_controller])
        # TODO: Add candidate authentication dependency
) -> SubmitApplicationResponse:
    """
    Submit an application to a public job position

    Requires candidate authentication. Creates a CompanyCandidate record
    and assigns the candidate to the position's default workflow.

    Args:
        slug_or_id: Position public slug or ID
        request: Application request data (cover letter, referral source)

    Returns:
        SubmitApplicationResponse with application ID

    Raises:
        401: If not authenticated as candidate
        404: If position not found or not public
        400: If candidate has already applied
    """
    # TODO: Get candidate_id from authentication token
    candidate_id = "placeholder-candidate-id"

    try:
        return controller.submit_application(
            slug_or_id=slug_or_id,
            candidate_id=candidate_id,
            request=request
        )
    except JobPositionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit application: {str(e)}"
        )
