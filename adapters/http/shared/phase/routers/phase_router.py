"""
Phase router for REST API endpoints.

Company-scoped routes for phase management.
URL Pattern: /{company_slug}/admin/phases/*
"""
from typing import List, Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from adapters.http.shared.dependencies.company_context import AdminCompanyContext
from adapters.http.shared.phase.controllers.phase_controller import PhaseController
from adapters.http.shared.phase.schemas.phase_schemas import (
    CreatePhaseRequest,
    UpdatePhaseRequest,
    PhaseResponse
)
from core.containers import Container

router = APIRouter(prefix="/{company_slug}/admin/phases", tags=["phases"])


@router.post(
    "",
    response_model=PhaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new phase"
)
@inject
def create_phase(
        company: AdminCompanyContext,
        request: CreatePhaseRequest,
        controller: Annotated[PhaseController, Depends(Provide[Container.phase_controller])]
) -> PhaseResponse:
    """Create a new phase for a company"""
    try:
        return controller.create_phase(company.id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "",
    response_model=List[PhaseResponse],
    summary="List all phases for a company"
)
@inject
def list_phases(
        company: AdminCompanyContext,
        controller: Annotated[PhaseController, Depends(Provide[Container.phase_controller])]
) -> List[PhaseResponse]:
    """List all phases for a company, ordered by sort_order"""
    try:
        return controller.list_phases_by_company(company.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/{phase_id}",
    response_model=PhaseResponse,
    summary="Get a phase by ID"
)
@inject
def get_phase(
        phase_id: str,
        company: AdminCompanyContext,
        controller: Annotated[PhaseController, Depends(Provide[Container.phase_controller])]
) -> PhaseResponse:
    """Get a phase by ID"""
    try:
        return controller.get_phase_by_id(phase_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put(
    "/{phase_id}",
    response_model=PhaseResponse,
    summary="Update a phase"
)
@inject
def update_phase(
        phase_id: str,
        request: UpdatePhaseRequest,
        company: AdminCompanyContext,
        controller: Annotated[PhaseController, Depends(Provide[Container.phase_controller])]
) -> PhaseResponse:
    """Update an existing phase"""
    try:
        return controller.update_phase(phase_id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
    "/{phase_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a phase"
)
@inject
def delete_phase(
        phase_id: str,
        company: AdminCompanyContext,
        controller: Annotated[PhaseController, Depends(Provide[Container.phase_controller])]
) -> None:
    """Delete a phase"""
    try:
        controller.delete_phase(phase_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/initialize",
    response_model=List[PhaseResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Initialize default phases (reset)"
)
@inject
def initialize_default_phases(
        company: AdminCompanyContext,
        controller: Annotated[PhaseController, Depends(Provide[Container.phase_controller])]
) -> List[PhaseResponse]:
    """Initialize default phases for a company (reset to defaults)

    This will create 3 default phases with their workflows:
    - Sourcing (Kanban) - Screening process
    - Evaluation (Kanban) - Interview and assessment
    - Offer and Pre-Onboarding (List) - Offer negotiation
    """
    try:
        return controller.initialize_default_phases(company.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/{phase_id}/archive",
    response_model=PhaseResponse,
    summary="Archive a phase (soft delete)"
)
@inject
def archive_phase(
        phase_id: str,
        company: AdminCompanyContext,
        controller: Annotated[PhaseController, Depends(Provide[Container.phase_controller])]
) -> PhaseResponse:
    """Archive a phase (soft delete)"""
    try:
        return controller.archive_phase(phase_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/{phase_id}/activate",
    response_model=PhaseResponse,
    summary="Activate a phase"
)
@inject
def activate_phase(
        phase_id: str,
        company: AdminCompanyContext,
        controller: Annotated[PhaseController, Depends(Provide[Container.phase_controller])]
) -> PhaseResponse:
    """Activate a phase"""
    try:
        return controller.activate_phase(phase_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
