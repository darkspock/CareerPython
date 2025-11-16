"""Company Interview Router - For company users to manage their interviews"""
import base64
import json
import logging
from datetime import datetime
from typing import Annotated
from typing import List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, Security
from fastapi.security import OAuth2PasswordBearer

from adapters.http.company_app.interview.controllers.interview_controller import InterviewController
from adapters.http.company_app.interview.schemas.interview_management import (
    InterviewCreateRequest, InterviewUpdateRequest, InterviewManagementResponse,
    InterviewListResponse, InterviewStatsResponse, InterviewActionResponse,
    InterviewScoreSummaryResponse, StartInterviewRequest, FinishInterviewRequest
)
from core.container import Container
from src.framework.application.query_bus import QueryBus

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
        candidate_name: Optional[str] = Query(None, description="Filter by candidate name"),
        job_position_id: Optional[str] = Query(None, description="Filter by job position ID"),
        interview_type: Optional[str] = Query(None, description="Filter by interview type"),
        process_type: Optional[str] = Query(None, description="Filter by process type"),
        status: Optional[str] = Query(None, description="Filter by status"),
        required_role_id: Optional[str] = Query(None, description="Filter by required role ID"),
        interviewer_user_id: Optional[str] = Query(None, description="Filter by interviewer user ID"),
        from_date: Optional[datetime] = Query(None, description="Filter from date"),
        to_date: Optional[datetime] = Query(None, description="Filter to date"),
        filter_by: Optional[str] = Query(
            None,
            description=(
                "Filter by InterviewFilterEnum: 'PENDING_TO_PLAN', 'PLANNED', "
                "'IN_PROGRESS', 'RECENTLY_FINISHED', 'OVERDUE', 'PENDING_FEEDBACK'"
            )
        ),
        limit: int = Query(50, ge=1, le=100, description="Limit results"),
        offset: int = Query(0, ge=0, description="Offset for pagination")
) -> InterviewListResponse:
    """List interviews for the authenticated company"""
    log.info(f"Listing interviews for company_id: {company_id}")

    # TODO: Add company_id filter to ListInterviewsQuery
    # For now, we'll filter by company_id in the controller or query handler
    interviews, total = controller.list_interviews(
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        job_position_id=job_position_id,
        interview_type=interview_type,
        process_type=process_type,
        status=status,
        required_role_id=required_role_id,
        interviewer_user_id=interviewer_user_id,
        created_by=None,  # Don't filter by creator in company context
        from_date=from_date,
        to_date=to_date,
        filter_by=filter_by,
        limit=limit,
        offset=offset
    )

    # TODO: Filter interviews by company_id (candidates and job positions must belong to company)
    # This should be done in the query handler, not here

    # Calculate current page from offset and limit
    current_page = (offset // limit) + 1 if limit > 0 else 1

    return InterviewListResponse(
        interviews=[InterviewManagementResponse.from_list_dto(interview) for interview in interviews],
        total=total,
        page=current_page,
        page_size=limit
    )


@router.get("/statistics", response_model=InterviewStatsResponse)
@inject
def get_interview_stats(
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
) -> InterviewStatsResponse:
    """Get interview statistics for the authenticated company"""
    try:
        stats_dto = controller.get_interview_statistics(company_id=company_id)
        return InterviewStatsResponse(
            total_interviews=0,  # TODO: Calculate from stats_dto if needed
            scheduled_interviews=0,  # TODO: Calculate from stats_dto if needed
            in_progress_interviews=stats_dto.in_progress,
            completed_interviews=0,  # TODO: Calculate from stats_dto if needed
            average_score=None,
            average_duration_minutes=None,
            pending_to_plan=stats_dto.pending_to_plan,
            planned=stats_dto.planned,
            recently_finished=stats_dto.recently_finished,
            overdue=stats_dto.overdue,
            pending_feedback=stats_dto.pending_feedback
        )
    except Exception as e:
        log.error(f"Error getting interview statistics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve interview statistics")


@router.get("/calendar", response_model=List[InterviewManagementResponse])
@inject
def get_interview_calendar(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        company_id: str = Depends(get_company_id_from_token),
        from_date: datetime = Query(..., description="Start date for calendar range"),
        to_date: datetime = Query(..., description="End date for calendar range"),
        filter_by: Optional[str] = Query(
            'scheduled',
            description=(
                "Filter by date field: 'scheduled', 'deadline', "
                "or 'unscheduled' (interviews without scheduled_at or interviewers)"
            )
        )
) -> List[InterviewManagementResponse]:
    """Get interviews within a date range for calendar view"""
    try:
        from src.interview_bc.interview.application.queries.get_interviews_by_date_range import \
            GetInterviewsByDateRangeQuery
        from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto

        query = GetInterviewsByDateRangeQuery(
            from_date=from_date,
            to_date=to_date,
            company_id=company_id,
            filter_by=filter_by
        )
        interviews: List[InterviewDto] = query_bus.query(query)
        return [InterviewManagementResponse.from_dto(interview) for interview in interviews]
    except Exception as e:
        log.error(f"Error getting interview calendar: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve interview calendar")


@router.get("/overdue", response_model=List[InterviewManagementResponse])
@inject
def get_overdue_interviews(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        company_id: str = Depends(get_company_id_from_token),
) -> List[InterviewManagementResponse]:
    """Get overdue interviews for the authenticated company"""
    try:
        from src.interview_bc.interview.application.queries.get_overdue_interviews import GetOverdueInterviewsQuery
        from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto

        query = GetOverdueInterviewsQuery(company_id=company_id)
        interviews: List[InterviewDto] = query_bus.query(query)
        return [InterviewManagementResponse.from_dto(interview) for interview in interviews]
    except Exception as e:
        log.error(f"Error getting overdue interviews: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve overdue interviews")


@router.get("/{interview_id}", response_model=InterviewManagementResponse)
@inject
def get_interview(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
) -> InterviewManagementResponse:
    """Get a specific interview by ID (must belong to the company)"""
    response = controller.get_interview_by_id(interview_id)

    # TODO: Verify that the interview belongs to the company
    # (check candidate.company_id or job_position.company_id)

    return response


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
        required_roles=interview_data.required_roles,
        interview_type=interview_data.interview_type,
        interview_mode=interview_data.interview_mode,
        process_type=interview_data.process_type,
        job_position_id=interview_data.job_position_id,
        application_id=interview_data.application_id,
        interview_template_id=interview_data.interview_template_id,
        title=interview_data.title,
        description=interview_data.description,
        scheduled_at=interview_data.scheduled_at,
        deadline_date=interview_data.deadline_date,
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

    result = controller.update_interview(
        interview_id=interview_id,
        title=interview_data.title,
        description=interview_data.description,
        scheduled_at=interview_data.scheduled_at,
        deadline_date=interview_data.deadline_date,
        process_type=interview_data.process_type,
        interview_type=interview_data.interview_type,
        interview_mode=interview_data.interview_mode,
        required_roles=interview_data.required_roles,
        interviewers=interview_data.interviewers,
        interviewer_notes=interview_data.interviewer_notes,
        feedback=interview_data.feedback,
        score=interview_data.score,
        updated_by=company_user_id
    )

    return InterviewActionResponse(
        message=result["message"],
        status=result["status"],
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


@router.get("/{interview_id}/score-summary", response_model=InterviewScoreSummaryResponse)
@inject
def get_interview_score_summary(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
) -> InterviewScoreSummaryResponse:
    """Get interview score summary (must belong to the company)"""
    # TODO: Verify that the interview belongs to the company
    # TODO: Map result to InterviewScoreSummaryResponse
    controller.get_interview_score_summary(interview_id)
    return InterviewScoreSummaryResponse(
        interview_id=interview_id,
        overall_score=None,
        total_questions=0,
        answered_questions=0,
        average_answer_score=None,
        completion_percentage=0.0
    )


@router.post("/{interview_id}/generate-link", response_model=dict)
@inject
def generate_interview_link(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
        company_user_id: str = Depends(get_company_user_id_from_token),
        expires_in_days: int = Query(30, ge=1, le=365, description="Link expiration in days")
) -> dict:
    """Generate a shareable link for an interview"""
    # TODO: Verify that the interview belongs to the company

    result = controller.generate_interview_link(
        interview_id=interview_id,
        expires_in_days=expires_in_days,
        generated_by=company_user_id
    )

    return result


