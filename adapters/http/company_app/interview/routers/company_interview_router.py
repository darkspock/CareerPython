"""Company Interview Router - For company users to manage their interviews"""
import logging
from datetime import datetime
from typing import List, Optional
import base64
import json

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, Security
from typing import Annotated

from core.container import Container
from adapters.http.admin_app.controllers.interview_controller import InterviewController
from adapters.http.admin_app.schemas.interview_management import (
    InterviewCreateRequest, InterviewUpdateRequest, InterviewManagementResponse,
    InterviewListResponse, InterviewStatsResponse, InterviewActionResponse,
    InterviewScoreSummaryResponse, StartInterviewRequest, FinishInterviewRequest
)
from fastapi.security import OAuth2PasswordBearer

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/company/interviews", tags=["Company Interviews"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/companies/auth/login")


def get_company_id_from_token(token: str = Security(oauth2_scheme)) -> str:
    """Extract company_id from JWT token"""
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
        company_id = data.get('company_id')
        
        if not company_id or not isinstance(company_id, str):
            raise HTTPException(status_code=401, detail="company_id not found in token")
        
        return str(company_id)
    except Exception as e:
        log.error(f"Error extracting company_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


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
        company_user_id = data.get('company_user_id') or data.get('user_id')
        
        if not company_user_id or not isinstance(company_user_id, str):
            raise HTTPException(status_code=401, detail="company_user_id not found in token")
        
        return str(company_user_id)
    except Exception as e:
        log.error(f"Error extracting company_user_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("", response_model=InterviewListResponse)
@inject
def list_interviews(
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
    candidate_id: Optional[str] = Query(None, description="Filter by candidate ID"),
    job_position_id: Optional[str] = Query(None, description="Filter by job position ID"),
    interview_type: Optional[str] = Query(None, description="Filter by interview type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    from_date: Optional[datetime] = Query(None, description="Filter from date"),
    to_date: Optional[datetime] = Query(None, description="Filter to date"),
    limit: int = Query(50, ge=1, le=100, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
) -> InterviewListResponse:
    """List interviews for the authenticated company"""
    log.info(f"Listing interviews for company_id: {company_id}")
    
    # TODO: Add company_id filter to ListInterviewsQuery
    # For now, we'll filter by company_id in the controller or query handler
    interviews = controller.list_interviews(
        candidate_id=candidate_id,
        job_position_id=job_position_id,
        interview_type=interview_type,
        status=status,
        created_by=None,  # Don't filter by creator in company context
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        offset=offset
    )
    
    # TODO: Filter interviews by company_id (candidates and job positions must belong to company)
    # This should be done in the query handler, not here
    
    return InterviewListResponse(
        interviews=[InterviewManagementResponse.from_dto(interview) for interview in interviews],
        total=len(interviews),
        page=1,
        page_size=limit
    )


@router.get("/stats", response_model=InterviewStatsResponse)
@inject
def get_interview_stats(
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
) -> InterviewStatsResponse:
    """Get interview statistics for the authenticated company"""
    # TODO: Implement company-specific stats
    return InterviewStatsResponse(
        total_interviews=0,
        scheduled_interviews=0,
        in_progress_interviews=0,
        completed_interviews=0,
        average_score=None,
        average_duration_minutes=None
    )


@router.get("/{interview_id}", response_model=InterviewManagementResponse)
@inject
def get_interview(
    interview_id: str,
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
) -> InterviewManagementResponse:
    """Get a specific interview by ID (must belong to the company)"""
    interview = controller.get_interview_by_id(interview_id)
    
    # TODO: Verify that the interview belongs to the company
    # (check candidate.company_id or job_position.company_id)
    
    return InterviewManagementResponse.from_dto(interview)


@router.post("", response_model=InterviewActionResponse)
@inject
def create_interview(
    interview_data: InterviewCreateRequest,
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewActionResponse:
    """Create a new interview for the authenticated company"""
    log.info(f"Creating interview for company_id: {company_id}")
    
    # TODO: Verify that candidate_id and job_position_id belong to the company
    
    result = controller.create_interview(
        candidate_id=interview_data.candidate_id,
        interview_type=interview_data.interview_type,
        job_position_id=interview_data.job_position_id,
        application_id=interview_data.application_id,
        interview_template_id=interview_data.interview_template_id,
        title=interview_data.title,
        description=interview_data.description,
        scheduled_at=interview_data.scheduled_at,
        interviewers=interview_data.interviewers,
        created_by=company_user_id
    )
    
    return InterviewActionResponse(
        message=result["message"],
        status=result["status"],
        interview_id=None
    )


@router.put("/{interview_id}", response_model=InterviewActionResponse)
@inject
def update_interview(
    interview_id: str,
    interview_data: InterviewUpdateRequest,
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewActionResponse:
    """Update an existing interview (must belong to the company)"""
    # TODO: Verify that the interview belongs to the company
    # TODO: Implement update_interview in controller
    return InterviewActionResponse(
        message="Interview updated successfully",
        status="success",
        interview_id=interview_id
    )


@router.post("/{interview_id}/start", response_model=InterviewActionResponse)
@inject
def start_interview(
    interview_id: str,
    start_data: StartInterviewRequest,
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewActionResponse:
    """Start an interview (must belong to the company)"""
    # TODO: Verify that the interview belongs to the company
    
    result = controller.start_interview(
        interview_id=interview_id,
        started_by=start_data.started_by or company_user_id
    )
    
    return InterviewActionResponse(
        message=result["message"],
        status=result["status"],
        interview_id=interview_id
    )


@router.post("/{interview_id}/finish", response_model=InterviewActionResponse)
@inject
def finish_interview(
    interview_id: str,
    finish_data: FinishInterviewRequest,
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
    company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewActionResponse:
    """Finish an interview (must belong to the company)"""
    # TODO: Verify that the interview belongs to the company
    
    result = controller.finish_interview(
        interview_id=interview_id,
        finished_by=finish_data.finished_by or company_user_id
    )
    
    return InterviewActionResponse(
        message=result["message"],
        status=result["status"],
        interview_id=interview_id
    )


@router.get("/candidate/{candidate_id}", response_model=List[InterviewManagementResponse])
@inject
def get_interviews_by_candidate(
    candidate_id: str,
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
    status: Optional[str] = Query(None, description="Filter by status"),
    interview_type: Optional[str] = Query(None, description="Filter by interview type")
) -> List[InterviewManagementResponse]:
    """Get interviews for a specific candidate (must belong to the company)"""
    # TODO: Verify that the candidate belongs to the company
    
    interviews = controller.get_interviews_by_candidate(
        candidate_id=candidate_id,
    )
    
    return [InterviewManagementResponse.from_dto(interview) for interview in interviews]


@router.get("/scheduled", response_model=List[InterviewManagementResponse])
@inject
def get_scheduled_interviews(
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
    from_date: Optional[datetime] = Query(None, description="Filter from date"),
    to_date: Optional[datetime] = Query(None, description="Filter to date"),
    interviewer: Optional[str] = Query(None, description="Filter by interviewer name")
) -> List[InterviewManagementResponse]:
    """Get scheduled interviews for the authenticated company"""
    interviews = controller.get_scheduled_interviews(
        from_date=from_date,
        to_date=to_date,
    )
    
    # TODO: Filter interviews by company_id
    
    return [InterviewManagementResponse.from_dto(interview) for interview in interviews]


@router.get("/{interview_id}/score-summary", response_model=InterviewScoreSummaryResponse)
@inject
def get_interview_score_summary(
    interview_id: str,
    controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
    company_id: str = Depends(get_company_id_from_token),
) -> InterviewScoreSummaryResponse:
    """Get interview score summary (must belong to the company)"""
    # TODO: Verify that the interview belongs to the company
    
    result = controller.get_interview_score_summary(interview_id)
    
    # TODO: Map result to InterviewScoreSummaryResponse
    return InterviewScoreSummaryResponse(
        interview_id=interview_id,
        overall_score=None,
        total_questions=0,
        answered_questions=0,
        average_answer_score=None,
        completion_percentage=0.0
    )

