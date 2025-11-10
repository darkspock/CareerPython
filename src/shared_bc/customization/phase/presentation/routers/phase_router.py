"""Phase router for REST API endpoints"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from core.container import Container
from adapters.http.phase.controllers.phase_controller import PhaseController
from src.shared_bc.customization.phase.presentation.schemas.phase_schemas import (
    CreatePhaseRequest,
    UpdatePhaseRequest,
    PhaseResponse
)

router = APIRouter(prefix="/api/companies/{company_id}/phases", tags=["phases"])


@router.post(
    "",
    response_model=PhaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new phase"
)
@inject
def create_phase(
    company_id: str,
    request: CreatePhaseRequest,
    controller: PhaseController = Depends(Provide[Container.phase_controller])
) -> PhaseResponse:
    """Create a new phase for a company

    Args:
        company_id: Company ID
        request: Create phase request

    Returns:
        Created phase

    Raises:
        HTTPException: If creation fails
    """
    try:
        return controller.create_phase(company_id, request)
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
    company_id: str,
    controller: PhaseController = Depends(Provide[Container.phase_controller])
) -> List[PhaseResponse]:
    """List all phases for a company, ordered by sort_order

    Args:
        company_id: Company ID

    Returns:
        List of phases
    """
    try:
        return controller.list_phases_by_company(company_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/{phase_id}",
    response_model=PhaseResponse,
    summary="Get a phase by ID"
)
@inject
def get_phase(
    company_id: str,
    phase_id: str,
    controller: PhaseController = Depends(Provide[Container.phase_controller])
) -> PhaseResponse:
    """Get a phase by ID

    Args:
        company_id: Company ID
        phase_id: Phase ID

    Returns:
        Phase details

    Raises:
        HTTPException: If phase not found
    """
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
    company_id: str,
    phase_id: str,
    request: UpdatePhaseRequest,
    controller: PhaseController = Depends(Provide[Container.phase_controller])
) -> PhaseResponse:
    """Update an existing phase

    Args:
        company_id: Company ID
        phase_id: Phase ID
        request: Update phase request

    Returns:
        Updated phase

    Raises:
        HTTPException: If phase not found or update fails
    """
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
    company_id: str,
    phase_id: str,
    controller: PhaseController = Depends(Provide[Container.phase_controller])
) -> None:
    """Delete a phase

    Args:
        company_id: Company ID
        phase_id: Phase ID

    Raises:
        HTTPException: If phase not found or deletion fails
    """
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
    company_id: str,
    controller: PhaseController = Depends(Provide[Container.phase_controller])
) -> List[PhaseResponse]:
    """Initialize default phases for a company (reset to defaults)

    This will create 3 default phases with their workflows:
    - Sourcing (Kanban) - Screening process
    - Evaluation (Kanban) - Interview and assessment
    - Offer and Pre-Onboarding (List) - Offer negotiation

    Args:
        company_id: Company ID

    Returns:
        List of created phases

    Raises:
        HTTPException: If initialization fails
    """
    try:
        return controller.initialize_default_phases(company_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/{phase_id}/archive",
    response_model=PhaseResponse,
    summary="Archive a phase (soft delete)"
)
@inject
def archive_phase(
    company_id: str,
    phase_id: str,
    controller: PhaseController = Depends(Provide[Container.phase_controller])
) -> PhaseResponse:
    """Archive a phase (soft delete)

    Args:
        company_id: Company ID
        phase_id: Phase ID to archive

    Returns:
        Archived phase

    Raises:
        HTTPException: If phase not found or archiving fails
    """
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
    company_id: str,
    phase_id: str,
    controller: PhaseController = Depends(Provide[Container.phase_controller])
) -> PhaseResponse:
    """Activate a phase

    Args:
        company_id: Company ID
        phase_id: Phase ID to activate

    Returns:
        Activated phase

    Raises:
        HTTPException: If phase not found or activation fails
    """
    try:
        return controller.activate_phase(phase_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
