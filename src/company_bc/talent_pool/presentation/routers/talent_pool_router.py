"""
Talent Pool Router
Phase 8: FastAPI router for talent pool endpoints
"""

from typing import List, Optional, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.container import Container
from src.company_bc.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus
from adapters.http.talent_pool.controllers.talent_pool_controller import TalentPoolController
from src.company_bc.talent_pool.presentation.schemas.talent_pool_schemas import (
    AddToTalentPoolRequest,
    UpdateTalentPoolEntryRequest,
    ChangeTalentPoolStatusRequest,
    TalentPoolEntryResponse,
)

router = APIRouter(
    prefix="/api/company/talent-pool",
    tags=["company-talent-pool"],
)


@router.post("/{company_id}", status_code=status.HTTP_201_CREATED)
@inject
def add_to_talent_pool(
        company_id: str,
        request: AddToTalentPoolRequest,
        controller: Annotated[TalentPoolController, Depends(Provide[Container.talent_pool_controller])],
) -> dict:
    """Add a candidate to the company's talent pool"""
    try:
        return controller.add_to_talent_pool(
            company_id=company_id,
            candidate_id=request.candidate_id,
            added_reason=request.added_reason,
            tags=request.tags,
            rating=request.rating,
            notes=request.notes,
            status=request.status,
            source_application_id=request.source_application_id,
            source_position_id=request.source_position_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{company_id}/entries")
@inject
def list_talent_pool_entries(
        company_id: str,
        controller: Annotated[TalentPoolController, Depends(Provide[Container.talent_pool_controller])],
        status_filter: Optional[TalentPoolStatus] = Query(None, alias="status"),
        tags: Optional[List[str]] = Query(None),
        min_rating: Optional[int] = Query(None, ge=1, le=5),
) -> List[TalentPoolEntryResponse]:
    """List talent pool entries for a company with optional filters"""
    return controller.list_entries(
        company_id=company_id,
        status=status_filter,
        tags=tags,
        min_rating=min_rating,
    )


@router.get("/{company_id}/search")
@inject
def search_talent_pool(
        company_id: str,
        controller: Annotated[TalentPoolController, Depends(Provide[Container.talent_pool_controller])],
        search_term: Optional[str] = Query(None),
        status_filter: Optional[TalentPoolStatus] = Query(None, alias="status"),
        tags: Optional[List[str]] = Query(None),
        min_rating: Optional[int] = Query(None, ge=1, le=5),
) -> List[TalentPoolEntryResponse]:
    """Search talent pool entries"""
    return controller.search_entries(
        company_id=company_id,
        search_term=search_term,
        status=status_filter,
        tags=tags,
        min_rating=min_rating,
    )


@router.get("/entries/{entry_id}")
@inject
def get_talent_pool_entry(
        entry_id: str,
        controller: Annotated[TalentPoolController, Depends(Provide[Container.talent_pool_controller])],
) -> TalentPoolEntryResponse:
    """Get a talent pool entry by ID"""
    entry = controller.get_entry_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Talent pool entry not found")
    return entry


@router.put("/entries/{entry_id}")
@inject
def update_talent_pool_entry(
        entry_id: str,
        request: UpdateTalentPoolEntryRequest,
        controller: Annotated[TalentPoolController, Depends(Provide[Container.talent_pool_controller])],
) -> dict:
    """Update a talent pool entry"""
    try:
        return controller.update_entry(
            entry_id=entry_id,
            added_reason=request.added_reason,
            tags=request.tags,
            rating=request.rating,
            notes=request.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/entries/{entry_id}/status")
@inject
def change_talent_pool_entry_status(
        entry_id: str,
        request: ChangeTalentPoolStatusRequest,
        controller: Annotated[TalentPoolController, Depends(Provide[Container.talent_pool_controller])],
) -> dict:
    """Change talent pool entry status"""
    try:
        return controller.change_status(entry_id=entry_id, new_status=request.status)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/entries/{entry_id}")
@inject
def remove_from_talent_pool(
        entry_id: str,
        controller: Annotated[TalentPoolController, Depends(Provide[Container.talent_pool_controller])],
) -> dict:
    """Remove a candidate from the talent pool"""
    try:
        return controller.remove_from_talent_pool(entry_id=entry_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
