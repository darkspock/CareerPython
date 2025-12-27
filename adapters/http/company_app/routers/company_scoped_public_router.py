"""
Company-scoped public routes.

All routes in this router require a company_slug in the URL path.
These routes are public (no authentication required) and provide:
- Public job board for a specific company
- Company information page

URL Pattern: /{company_slug}/positions, /{company_slug}/about
"""
import logging
from typing import Annotated, Any, Optional, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, status

from adapters.http.shared.dependencies.company_context import CompanyContext
from core.containers import Container
from src.company_bc.company.application.dtos.company_dto import CompanyDto
from src.framework.application.query_bus import QueryBus

log = logging.getLogger(__name__)

# Router with company_slug prefix - NO authentication required
router = APIRouter(
    prefix="/{company_slug}",
    tags=["Company Public"],
)


@router.get("/positions")
@inject
def list_company_positions(
    company: CompanyContext,
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
    search: Optional[str] = Query(None, description="Search term for title/description"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(12, ge=1, le=100, description="Items per page"),
) -> dict:
    """
    List published job positions for this company.

    This endpoint is public - no authentication required.
    Returns only published positions visible to candidates.
    """
    from src.company_bc.job_position.application.queries.list_published_job_positions import (
        ListPublishedJobPositionsQuery
    )
    from src.company_bc.company.domain import CompanyId

    query = ListPublishedJobPositionsQuery(company_id=CompanyId.from_string(company.id))
    positions: Optional[List[Any]] = query_bus.query(query)

    # Apply search filter if provided
    if search and positions:
        search_lower = search.lower()
        positions = [
            p for p in positions
            if search_lower in (p.title or "").lower()
            or search_lower in (p.description or "").lower()
        ]

    # Apply pagination
    total = len(positions) if positions else 0
    start = (page - 1) * page_size
    end = start + page_size
    paginated_positions = positions[start:end] if positions else []

    return {
        "company": {
            "id": company.id,
            "name": company.name,
            "slug": company.slug,
            "logo_url": company.logo_url,
        },
        "positions": paginated_positions,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if total > 0 else 1,
    }


@router.get("/positions/{position_id}")
@inject
def get_company_position(
    position_id: str,
    company: CompanyContext,
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> dict:
    """
    Get details of a specific job position at this company.

    This endpoint is public - no authentication required.
    Returns position details only if it belongs to this company and is published.
    """
    from src.company_bc.job_position.application.queries.get_job_position_by_id import (
        GetJobPositionByIdQuery
    )
    from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId

    query = GetJobPositionByIdQuery(id=JobPositionId.from_string(position_id))
    position: Optional[Any] = query_bus.query(query)

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    # Verify position belongs to this company
    if str(position.company_id) != company.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    # Verify position is published (status should be 'published' or similar)
    # Note: Adjust this check based on your actual status enum
    if hasattr(position, 'status') and position.status not in ['published', 'PUBLISHED', 'open', 'OPEN']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )

    return {
        "id": str(position.id),
        "title": position.title,
        "description": position.description,
        "location": position.location,
        "employment_type": position.employment_type,
        "job_category": position.job_category,
        "required_experience": position.required_experience,
        "salary_range": position.salary_range,
        "benefits": position.benefits,
        "requirements": position.requirements,
        "responsibilities": position.responsibilities,
        "status": position.status,
        "public_slug": position.public_slug,
        "created_at": position.created_at.isoformat() if position.created_at else None,
        "company": {
            "id": company.id,
            "name": company.name,
            "slug": company.slug,
            "logo_url": company.logo_url,
        },
    }


@router.get("/about")
@inject
def get_company_about(
    company: CompanyContext,
    query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
) -> dict:
    """
    Get public company information (about page).

    This endpoint is public - no authentication required.
    Returns basic company information for the careers page.
    """
    from adapters.http.company_app.company_page.controllers.company_page_controller import CompanyPageController
    from core.containers import Container as ContainerRef

    try:
        # Try to get the about page from the company page controller
        controller: CompanyPageController = ContainerRef.company_page_controller()
        page = controller.get_public_page(company.id, "about")

        if page:
            return {
                "company": {
                    "id": company.id,
                    "name": company.name,
                    "slug": company.slug,
                    "logo_url": company.logo_url,
                },
                "page": {
                    "type": "about",
                    "title": page.title if hasattr(page, 'title') else company.name,
                    "content": page.content if hasattr(page, 'content') else None,
                    "sections": page.sections if hasattr(page, 'sections') else [],
                }
            }
    except Exception as e:
        log.warning(f"Could not load company about page: {e}")

    # Return basic company info if no custom about page exists
    return {
        "company": {
            "id": company.id,
            "name": company.name,
            "slug": company.slug,
            "logo_url": company.logo_url,
        },
        "page": {
            "type": "about",
            "title": company.name,
            "content": None,
            "sections": [],
        }
    }


@router.get("")
@inject
def get_company_info(
    company: CompanyContext,
) -> dict:
    """
    Get basic company information.

    This endpoint is public - no authentication required.
    Returns basic company details for the landing page.
    """
    return {
        "id": company.id,
        "name": company.name,
        "slug": company.slug,
        "logo_url": company.logo_url,
    }
