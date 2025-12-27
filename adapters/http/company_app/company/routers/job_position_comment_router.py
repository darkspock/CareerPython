"""
Job Position Comment Router.

Company-scoped routes for managing comments on job positions.
URL Pattern: /{company_slug}/admin/positions/{position_id}/comments/*
"""
import logging
from typing import List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Query

from adapters.http.admin_app.controllers.job_position_comment_controller import JobPositionCommentController
from adapters.http.admin_app.schemas.job_position_comment import (
    CreateJobPositionCommentRequest,
    UpdateJobPositionCommentRequest,
    JobPositionCommentResponse,
    JobPositionCommentListResponse,
)
from adapters.http.shared.dependencies.company_context import CurrentCompanyUser
from core.containers import Container

log = logging.getLogger(__name__)

# Company-scoped router for position comments
router = APIRouter(prefix="/{company_slug}/admin/positions", tags=["Job Position Comments"])


@router.post("/{position_id}/comments", status_code=status.HTTP_201_CREATED)
@inject
def create_comment(
        position_id: str,
        request: CreateJobPositionCommentRequest,
        current_user: CurrentCompanyUser,
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller]),
) -> None:
    """Create a new comment for a job position"""
    try:
        controller.create_comment(position_id, request, current_user.id)
    except Exception as e:
        log.error(f"Error creating comment: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{position_id}/comments", response_model=JobPositionCommentListResponse)
@inject
def list_comments(
        position_id: str,
        current_user: CurrentCompanyUser,
        stage_id: Optional[str] = Query(None, description="Filter by stage ID (null = only global comments)"),
        include_global: bool = Query(True, description="Include global comments"),
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller]),
) -> JobPositionCommentListResponse:
    """List comments for a job position"""
    try:
        # Convert "null" string to None
        if stage_id == "null":
            stage_id = None
        return controller.list_comments(
            job_position_id=position_id,
            stage_id=stage_id,
            include_global=include_global,
            current_user_id=current_user.id
        )
    except Exception as e:
        log.error(f"Error listing comments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{position_id}/comments/all", response_model=List[JobPositionCommentResponse])
@inject
def get_all_comments(
        position_id: str,
        current_user: CurrentCompanyUser,
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller]),
) -> List[JobPositionCommentResponse]:
    """Get all comments for a position (regardless of stage)"""
    try:
        response = controller.list_all_comments(
            job_position_id=position_id,
            current_user_id=current_user.id
        )
        return response.comments
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error listing all comments: {e} {type(controller)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def update_comment(
        comment_id: str,
        request: UpdateJobPositionCommentRequest,
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller])
) -> None:
    """Update a comment"""
    try:
        controller.update_comment(comment_id, request)
    except Exception as e:
        log.error(f"Error updating comment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_comment(
        comment_id: str,
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller])
) -> None:
    """Delete a comment"""
    try:
        controller.delete_comment(comment_id)
    except Exception as e:
        log.error(f"Error deleting comment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/comments/{comment_id}/mark-reviewed", status_code=status.HTTP_204_NO_CONTENT)
@inject
def mark_comment_as_reviewed(
        comment_id: str,
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller])
) -> None:
    """Mark a comment as reviewed"""
    try:
        controller.mark_comment_as_reviewed(comment_id)
    except Exception as e:
        log.error(f"Error marking comment as reviewed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/comments/{comment_id}/mark-pending", status_code=status.HTTP_204_NO_CONTENT)
@inject
def mark_comment_as_pending(
        comment_id: str,
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller])
) -> None:
    """Mark a comment as pending"""
    try:
        controller.mark_comment_as_pending(comment_id)
    except Exception as e:
        log.error(f"Error marking comment as pending: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
