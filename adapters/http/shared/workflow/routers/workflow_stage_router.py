"""Workflow Stage Router."""
from typing import List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, status

from adapters.http.shared.workflow.controllers import WorkflowStageController
from adapters.http.shared.workflow.schemas import UpdateStageRequest
from adapters.http.shared.workflow.schemas import WorkflowStageResponse
from adapters.http.shared.workflow.schemas.create_stage_request import CreateStageRequest
from adapters.http.shared.workflow.schemas.reorder_stages_request import ReorderStagesRequest
from adapters.http.shared.workflow.schemas.stage_style_request import UpdateStageStyleRequest
from core.container import Container

router = APIRouter(
    prefix="/api/workflow-stages",
    tags=["workflow-stages"]
)


@router.post(
    "/",
    response_model=WorkflowStageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new workflow stage"
)
@inject
def create_stage(
        request: CreateStageRequest,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> WorkflowStageResponse:
    """Create a new workflow stage"""
    try:
        return controller.create_stage(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{stage_id}",
    response_model=WorkflowStageResponse,
    summary="Get a stage by ID"
)
@inject
def get_stage_by_id(
        stage_id: str,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> Optional[WorkflowStageResponse]:
    """Get a stage by ID"""
    result = controller.get_stage_by_id(stage_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stage not found")
    return result


@router.get(
    "/workflow/{workflow_id}",
    response_model=List[WorkflowStageResponse],
    summary="List all stages for a workflow"
)
@inject
def list_stages_by_workflow(
        workflow_id: str,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> List[WorkflowStageResponse]:
    """List all stages for a workflow"""
    return controller.list_stages_by_workflow(workflow_id)


@router.get(
    "/phase/{phase_id}",
    response_model=List[WorkflowStageResponse],
    summary="List all stages for a phase"
)
@inject
def list_stages_by_phase(
        phase_id: str,
        workflow_type: str = Query(..., description="Workflow type (CA, PO, CO)"),
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> List[WorkflowStageResponse]:
    """List all stages for a phase"""
    return controller.list_stages_by_phase(phase_id, workflow_type)


@router.get(
    "/workflow/{workflow_id}/initial",
    response_model=WorkflowStageResponse,
    summary="Get the initial stage of a workflow"
)
@inject
def get_initial_stage(
        workflow_id: str,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> Optional[WorkflowStageResponse]:
    """Get the initial stage of a workflow"""
    result = controller.get_initial_stage(workflow_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Initial stage not found")
    return result


@router.get(
    "/workflow/{workflow_id}/final",
    response_model=List[WorkflowStageResponse],
    summary="Get all final stages of a workflow"
)
@inject
def get_final_stages(
        workflow_id: str,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> List[WorkflowStageResponse]:
    """Get all final stages of a workflow"""
    return controller.get_final_stages(workflow_id)


@router.put(
    "/{stage_id}",
    response_model=WorkflowStageResponse,
    summary="Update stage information"
)
@inject
def update_stage(
        stage_id: str,
        request: UpdateStageRequest,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> WorkflowStageResponse:
    """Update stage information"""
    try:
        return controller.update_stage(stage_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{stage_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a stage"
)
@inject
def delete_stage(
        stage_id: str,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> None:
    """Delete a stage"""
    try:
        controller.delete_stage(stage_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/workflow/{workflow_id}/reorder",
    response_model=List[WorkflowStageResponse],
    summary="Reorder stages in a workflow"
)
@inject
def reorder_stages(
        workflow_id: str,
        request: ReorderStagesRequest,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> List[WorkflowStageResponse]:
    """Reorder stages in a workflow"""
    try:
        return controller.reorder_stages(workflow_id, request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{stage_id}/activate",
    response_model=WorkflowStageResponse,
    summary="Activate a stage"
)
@inject
def activate_stage(
        stage_id: str,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> WorkflowStageResponse:
    """Activate a stage"""
    try:
        return controller.activate_stage(stage_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{stage_id}/deactivate",
    response_model=WorkflowStageResponse,
    summary="Deactivate a stage"
)
@inject
def deactivate_stage(
        stage_id: str,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> WorkflowStageResponse:
    """Deactivate a stage"""
    try:
        return controller.deactivate_stage(stage_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    "/{stage_id}/style",
    response_model=WorkflowStageResponse,
    summary="Update stage style"
)
@inject
def update_stage_style(
        stage_id: str,
        style_request: UpdateStageStyleRequest,
        controller: WorkflowStageController = Depends(Provide[Container.workflow_stage_controller])
) -> WorkflowStageResponse:
    """Update the visual style of a workflow stage"""
    try:
        return controller.update_stage_style(stage_id, style_request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
