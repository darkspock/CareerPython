"""Candidate Interview Router - For candidates to access interviews via secure links"""
import logging
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query

from core.container import Container
from adapters.http.admin_app.controllers.interview_controller import InterviewController
from adapters.http.admin_app.schemas.interview_management import InterviewManagementResponse

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/candidate/interviews", tags=["Candidate Interviews"])


@router.get("/{interview_id}/access", response_model=InterviewManagementResponse)
@inject
def access_interview_by_token(
    interview_id: str,
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    token: str = Query(..., description="Secure token for interview access"),
) -> InterviewManagementResponse:
    """
    Access interview by secure token link.
    This endpoint allows candidates to access their interviews using a secure token.
    The token is validated and must not be expired.
    """
    try:
        interview_dto = controller.get_interview_by_token(
            interview_id=interview_id,
            token=token
        )
        
        return InterviewManagementResponse.from_dto(interview_dto)
    
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error accessing interview {interview_id} by token: {e}")
        raise HTTPException(status_code=404, detail="Interview not found or token is invalid/expired")
