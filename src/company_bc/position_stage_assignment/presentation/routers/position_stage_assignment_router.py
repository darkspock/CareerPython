"""Position stage assignment router"""
from typing import List
from fastapi import APIRouter, Depends, status

from adapters.http.position_stage_assignment.controllers.position_stage_assignment_controller import PositionStageAssignmentController
from src.company_bc.position_stage_assignment.presentation.schemas import (
    AssignUsersToStageRequest,
    AddUserToStageRequest,
    RemoveUserFromStageRequest,
    CopyWorkflowAssignmentsRequest,
    PositionStageAssignmentResponse
)
from core.container import Container
from dependency_injector.wiring import inject, Provide

router = APIRouter(
    prefix="/position-stage-assignments",
    tags=["Position Stage Assignments"]
)


@router.post(
    "/assign",
    response_model=PositionStageAssignmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Assign users to a stage",
    description="Assign or replace users for a specific position-stage combination"
)
@inject
def assign_users_to_stage(
    request: AssignUsersToStageRequest,
    controller: PositionStageAssignmentController = Depends(Provide[Container.position_stage_assignment_controller])
) -> PositionStageAssignmentResponse:
    """Assign users to a stage"""
    return controller.assign_users_to_stage(request)


@router.post(
    "/add-user",
    response_model=PositionStageAssignmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Add user to a stage",
    description="Add a single user to a position-stage assignment"
)
@inject
def add_user_to_stage(
    request: AddUserToStageRequest,
    controller: PositionStageAssignmentController = Depends(Provide[Container.position_stage_assignment_controller])
) -> PositionStageAssignmentResponse:
    """Add a user to a stage"""
    return controller.add_user_to_stage(request)


@router.post(
    "/remove-user",
    response_model=PositionStageAssignmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Remove user from a stage",
    description="Remove a single user from a position-stage assignment"
)
@inject
def remove_user_from_stage(
    request: RemoveUserFromStageRequest,
    controller: PositionStageAssignmentController = Depends(Provide[Container.position_stage_assignment_controller])
) -> PositionStageAssignmentResponse:
    """Remove a user from a stage"""
    return controller.remove_user_from_stage(request)


@router.post(
    "/copy-workflow",
    response_model=List[PositionStageAssignmentResponse],
    status_code=status.HTTP_200_OK,
    summary="Copy workflow assignments",
    description="Copy default user assignments from workflow to a position"
)
@inject
def copy_workflow_assignments(
    request: CopyWorkflowAssignmentsRequest,
    controller: PositionStageAssignmentController = Depends(Provide[Container.position_stage_assignment_controller])
) -> List[PositionStageAssignmentResponse]:
    """Copy workflow assignments to a position"""
    return controller.copy_workflow_assignments(request)


@router.get(
    "/position/{position_id}",
    response_model=List[PositionStageAssignmentResponse],
    status_code=status.HTTP_200_OK,
    summary="List stage assignments",
    description="List all stage assignments for a position"
)
@inject
def list_stage_assignments(
    position_id: str,
    controller: PositionStageAssignmentController = Depends(Provide[Container.position_stage_assignment_controller])
) -> List[PositionStageAssignmentResponse]:
    """List all stage assignments for a position"""
    return controller.list_stage_assignments(position_id)


@router.get(
    "/position/{position_id}/stage/{stage_id}/users",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="Get assigned users",
    description="Get list of user IDs assigned to a specific position-stage combination"
)
@inject
def get_assigned_users(
    position_id: str,
    stage_id: str,
    controller: PositionStageAssignmentController = Depends(Provide[Container.position_stage_assignment_controller])
) -> List[str]:
    """Get assigned users for a position-stage combination"""
    return controller.get_assigned_users(position_id, stage_id)
