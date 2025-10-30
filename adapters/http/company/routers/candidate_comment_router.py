"""Candidate Comment Router."""
import logging
from typing import List, Annotated
import base64
import json

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer

from core.container import Container
from src.company_candidate.presentation.controllers.candidate_comment_controller import CandidateCommentController
from src.company_candidate.presentation.schemas.create_candidate_comment_request import CreateCandidateCommentRequest
from src.company_candidate.presentation.schemas.update_candidate_comment_request import UpdateCandidateCommentRequest
from src.company_candidate.presentation.schemas.candidate_comment_response import CandidateCommentResponse

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/company/candidates", tags=["Candidate Comments"])
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
        
        if not company_user_id:
            raise HTTPException(status_code=401, detail="company_user_id not found in token")
        
        return company_user_id
    except Exception as e:
        log.error(f"Error extracting company_user_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/{company_candidate_id}/comments", response_model=CandidateCommentResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_comment(
    company_candidate_id: str,
    request: CreateCandidateCommentRequest,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller]),
    company_user_id: str = Depends(get_company_user_id_from_token)
) -> CandidateCommentResponse:
    """Create a new comment for a candidate"""
    try:
        return controller.create_comment(company_candidate_id, request, company_user_id)
    except Exception as e:
        log.error(f"Error creating comment: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{company_candidate_id}/comments", response_model=List[CandidateCommentResponse])
@inject
def list_comments(
    company_candidate_id: str,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> List[CandidateCommentResponse]:
    """Get all comments for a candidate"""
    try:
        return controller.list_comments_by_company_candidate(company_candidate_id)
    except Exception as e:
        log.error(f"Error listing comments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{company_candidate_id}/comments/stage/{stage_id}", response_model=List[CandidateCommentResponse])
@inject
def list_comments_by_stage(
    company_candidate_id: str,
    stage_id: str,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> List[CandidateCommentResponse]:
    """Get all comments for a candidate in a specific stage"""
    try:
        return controller.list_comments_by_stage(company_candidate_id, stage_id)
    except Exception as e:
        log.error(f"Error listing comments by stage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{company_candidate_id}/comments/pending/count", response_model=int)
@inject
def count_pending_comments(
    company_candidate_id: str,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> int:
    """Count pending comments for a candidate"""
    try:
        return controller.count_pending_comments(company_candidate_id)
    except Exception as e:
        log.error(f"Error counting pending comments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/comments/{comment_id}", response_model=CandidateCommentResponse)
@inject
def get_comment(
    comment_id: str,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> CandidateCommentResponse:
    """Get a comment by ID"""
    result = controller.get_comment_by_id(comment_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return result


@router.put("/comments/{comment_id}", response_model=CandidateCommentResponse)
@inject
def update_comment(
    comment_id: str,
    request: UpdateCandidateCommentRequest,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> CandidateCommentResponse:
    """Update a comment"""
    result = controller.update_comment(comment_id, request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return result


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_comment(
    comment_id: str,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
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


@router.post("/comments/{comment_id}/mark-pending", response_model=CandidateCommentResponse)
@inject
def mark_comment_as_pending(
    comment_id: str,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> CandidateCommentResponse:
    """Mark a comment as pending review"""
    result = controller.mark_as_pending(comment_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return result


@router.post("/comments/{comment_id}/mark-reviewed", response_model=CandidateCommentResponse)
@inject
def mark_comment_as_reviewed(
    comment_id: str,
    controller: CandidateCommentController = Depends(Provide[Container.candidate_comment_controller])
) -> CandidateCommentResponse:
    """Mark a comment as reviewed"""
    result = controller.mark_as_reviewed(comment_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return result

