"""
Router for task management operations
Phase 6: Task Management System
"""
from typing import Annotated, Optional, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from adapters.http.company.controllers.task_controller import TaskController
from core.container import Container
from src.candidate_application.application.queries.shared.candidate_application_dto import CandidateApplicationDto

router = APIRouter(
    prefix="/api/company/tasks",
    tags=["company-tasks"]
)


class ClaimTaskRequest(BaseModel):
    """Request to claim a task"""
    application_id: str
    user_id: str  # TODO: Get from auth token/session


class UnclaimTaskRequest(BaseModel):
    """Request to unclaim a task"""
    application_id: str
    user_id: str  # TODO: Get from auth token/session


@router.get("/my-tasks", status_code=status.HTTP_200_OK)
@inject
def get_my_assigned_tasks(
        controller: Annotated[TaskController, Depends(Provide[Container.task_controller])],
        user_id: str = Query(..., description="User ID to get tasks for"),  # TODO: Get from auth token/session
        stage_id: Optional[str] = Query(None, description="Filter by specific stage ID"),
        limit: Optional[int] = Query(None, description="Limit number of results", ge=1, le=100),
) -> List[CandidateApplicationDto]:
    """
    Get all tasks assigned to the current user.

    Returns applications sorted by:
    - Priority (calculated from deadline and time in stage)
    - Stage entered time (oldest first)

    Phase 6: Task Management - This endpoint retrieves tasks assigned to a user based on their
    position-stage assignments.
    """
    try:
        tasks = controller.get_my_assigned_tasks(
            user_id=user_id,
            stage_id=stage_id,
            limit=limit
        )

        return tasks

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        )


@router.post("/claim", status_code=status.HTTP_200_OK)
@inject
def claim_task(
        request: ClaimTaskRequest,
        controller: Annotated[TaskController, Depends(Provide[Container.task_controller])]
) -> dict:
    """
    Claim a task for processing.

    This updates the task status from PENDING to IN_PROGRESS, indicating that
    the user has started working on this application.

    Phase 6: Task Management - When a user claims a task, they take ownership
    and the task status changes to in_progress.
    """
    try:
        result = controller.claim_task(
            application_id=request.application_id,
            user_id=request.user_id
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to claim task: {str(e)}"
        )


@router.post("/unclaim", status_code=status.HTTP_200_OK)
@inject
def unclaim_task(
        request: UnclaimTaskRequest,
        controller: Annotated[TaskController, Depends(Provide[Container.task_controller])]
) -> dict:
    """
    Unclaim/release a task back to pending status.

    This updates the task status from IN_PROGRESS back to PENDING, making the
    task available for other users to claim.

    Phase 6: Task Management - When a user unclaims a task, it goes back to
    the available pool for others to pick up.
    """
    try:
        result = controller.unclaim_task(
            application_id=request.application_id,
            user_id=request.user_id
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unclaim task: {str(e)}"
        )
