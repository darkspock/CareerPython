"""Job Position Comment Router."""
import base64
import json
import logging
from typing import List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from fastapi.security import OAuth2PasswordBearer

from adapters.http.admin_app.controllers.job_position_comment_controller import JobPositionCommentController
from adapters.http.admin_app.schemas.job_position_comment import (
    CreateJobPositionCommentRequest,
    UpdateJobPositionCommentRequest,
    JobPositionCommentResponse,
    JobPositionCommentListResponse,
)
from core.container import Container

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/company/positions", tags=["Job Position Comments"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/companies/auth/login")


def get_company_user_id_from_token(token: str = Security(oauth2_scheme)) -> str:
    """Extract company_user_id from JWT token"""
    try:
        # Decode JWT token (payload is in the second part)
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")

        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)
        company_user_id = data.get('company_user_id')

        if not company_user_id or not isinstance(company_user_id, str):
            raise HTTPException(status_code=401, detail="company_user_id not found in token")

        return str(company_user_id)
    except Exception as e:
        log.error(f"Error extracting company_user_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/{position_id}/comments", status_code=status.HTTP_201_CREATED)
@inject
def create_comment(
        position_id: str,
        request: CreateJobPositionCommentRequest,
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller]),
        company_user_id: str = Depends(get_company_user_id_from_token)
) -> None:
    """Create a new comment for a job position"""
    try:
        controller.create_comment(position_id, request, company_user_id)
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
        stage_id: Optional[str] = Query(None, description="Filter by stage ID (null = only global comments)"),
        include_global: bool = Query(True, description="Include global comments"),
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller]),
        company_user_id: str = Depends(get_company_user_id_from_token)
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
            current_user_id=company_user_id
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
        controller: JobPositionCommentController = Depends(Provide[Container.job_position_comment_controller]),
        company_user_id: str = Depends(get_company_user_id_from_token)
) -> List[JobPositionCommentResponse]:
    """Get all comments for a position (regardless of stage)"""
    try:
        response = controller.list_all_comments(
            job_position_id=position_id,
            current_user_id=company_user_id
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
