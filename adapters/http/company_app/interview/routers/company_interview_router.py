"""Company Interview Router - For company users to manage their interviews"""
import base64
import json
import logging
from datetime import datetime
from typing import Annotated
from typing import List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, Security
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer

from adapters.http.company_app.interview.controllers.interview_controller import InterviewController
from adapters.http.company_app.interview.mappers.interview_mapper import InterviewMapper
from adapters.http.company_app.interview.schemas.interview_management import (
    InterviewCreateRequest, InterviewUpdateRequest,
    InterviewResource, InterviewFullResource, InterviewListResource, InterviewStatsResource,
    InterviewActionResource, InterviewScoreSummaryResource, InterviewLinkResource,
    StartInterviewRequest, FinishInterviewRequest
)
from core.containers import Container
from src.framework.application.query_bus import QueryBus
from src.framework.infrastructure.services.calendar import ICSService, ICSEvent
from src.interview_bc.interview.application.queries.dtos.interview_list_dto import InterviewListDto
from src.interview_bc.interview.application.queries.list_interviews import ListInterviewsQuery

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


@router.get("", response_model=InterviewListResource)
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
) -> InterviewListResource:
    """List interviews for the authenticated company"""
    return controller.list_interviews(
        company_id=company_id,
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        job_position_id=job_position_id,
        interview_type=interview_type,
        process_type=process_type,
        status=status,
        required_role_id=required_role_id,
        interviewer_user_id=interviewer_user_id,
        created_by=None,
        from_date=from_date,
        to_date=to_date,
        filter_by=filter_by,
        limit=limit,
        offset=offset
    )


@router.get("/statistics", response_model=InterviewStatsResource)
@inject
def get_interview_stats(
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
) -> InterviewStatsResource:
    """Get interview statistics for the authenticated company"""
    return controller.get_interview_statistics(company_id=company_id)


@router.get("/calendar", response_model=List[InterviewFullResource])
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
) -> List[InterviewFullResource]:
    """Get interviews within a date range for calendar view"""
    from src.interview_bc.interview.application.queries.get_interviews_by_date_range import \
        GetInterviewsByDateRangeQuery
    from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto

    # Use ListInterviewsQuery which returns denormalized data
    query = ListInterviewsQuery(
        from_date=from_date,
        to_date=to_date,
        filter_by=filter_by,
        limit=100,
        offset=0
    )
    interviews: List[InterviewListDto] = query_bus.query(query)
    return InterviewMapper.list_dtos_to_full_responses(interviews)


@router.get("/overdue", response_model=List[InterviewFullResource])
@inject
def get_overdue_interviews(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        company_id: str = Depends(get_company_id_from_token),
) -> List[InterviewFullResource]:
    """Get overdue interviews for the authenticated company"""
    from datetime import datetime as dt

    # Use ListInterviewsQuery with OVERDUE filter which returns denormalized data
    query = ListInterviewsQuery(
        filter_by='OVERDUE',
        to_date=dt.utcnow(),
        limit=100,
        offset=0
    )
    interviews: List[InterviewListDto] = query_bus.query(query)
    return InterviewMapper.list_dtos_to_full_responses(interviews)


@router.get("/{interview_id}", response_model=InterviewResource)
@inject
def get_interview(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
) -> InterviewResource:
    """Get a specific interview by ID for editing (must belong to the company)"""
    return controller.get_interview_by_id(interview_id)


@router.get("/{interview_id}/view", response_model=InterviewFullResource)
@inject
def get_interview_view(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
) -> InterviewFullResource:
    """Get a specific interview by ID with full denormalized information for viewing (must belong to the company)"""
    return controller.get_interview_view(interview_id)


@router.post("", response_model=InterviewActionResource)
@inject
def create_interview(
        interview_data: InterviewCreateRequest,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
        company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewActionResource:
    """Create a new interview for the authenticated company"""
    return controller.create_interview(
        candidate_id=interview_data.candidate_id,
        required_roles=interview_data.required_roles,
        interview_type=interview_data.interview_type,
        interview_mode=interview_data.interview_mode,
        process_type=interview_data.process_type,
        job_position_id=interview_data.job_position_id,
        stage_id=interview_data.workflow_stage_id,
        application_id=interview_data.application_id,
        interview_template_id=interview_data.interview_template_id,
        title=interview_data.title,
        description=interview_data.description,
        scheduled_at=interview_data.scheduled_at,
        deadline_date=interview_data.deadline_date,
        interviewers=interview_data.interviewers,
        created_by=company_user_id
    )


@router.put("/{interview_id}", response_model=InterviewActionResource)
@inject
def update_interview(
        interview_id: str,
        interview_data: InterviewUpdateRequest,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
        company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewActionResource:
    """Update an existing interview (must belong to the company)"""
    return controller.update_interview(
        interview_id=interview_id,
        title=interview_data.title,
        description=interview_data.description,
        scheduled_at=interview_data.scheduled_at,
        deadline_date=interview_data.deadline_date,
        process_type=interview_data.process_type,
        interview_type=interview_data.interview_type,
        interview_mode=interview_data.interview_mode,
        status=interview_data.status,
        required_roles=interview_data.required_roles,
        interviewers=interview_data.interviewers,
        interviewer_notes=interview_data.interviewer_notes,
        feedback=interview_data.feedback,
        score=interview_data.score,
        updated_by=company_user_id
    )


@router.post("/{interview_id}/start", response_model=InterviewActionResource)
@inject
def start_interview(
        interview_id: str,
        start_data: StartInterviewRequest,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
        company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewActionResource:
    """Start an interview (must belong to the company)"""
    return controller.start_interview(
        interview_id=interview_id,
        started_by=start_data.started_by or company_user_id
    )


@router.post("/{interview_id}/finish", response_model=InterviewActionResource)
@inject
def finish_interview(
        interview_id: str,
        finish_data: FinishInterviewRequest,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
        company_user_id: str = Depends(get_company_user_id_from_token),
) -> InterviewActionResource:
    """Finish an interview (must belong to the company)"""
    return controller.finish_interview(
        interview_id=interview_id,
        finished_by=finish_data.finished_by or company_user_id
    )


@router.get("/{interview_id}/score-summary", response_model=InterviewScoreSummaryResource)
@inject
def get_interview_score_summary(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
) -> InterviewScoreSummaryResource:
    """Get interview score summary (must belong to the company)"""
    return controller.get_interview_score_summary(interview_id)


@router.post("/{interview_id}/generate-link", response_model=InterviewLinkResource)
@inject
def generate_interview_link(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
        company_user_id: str = Depends(get_company_user_id_from_token),
        expires_in_days: int = Query(30, ge=1, le=365, description="Link expiration in days")
) -> InterviewLinkResource:
    """Generate a shareable link for an interview"""
    return controller.generate_interview_link(
        interview_id=interview_id,
        expires_in_days=expires_in_days,
        generated_by=company_user_id
    )


# ============================================================================
# Calendar Export Endpoints
# ============================================================================

@router.get("/{interview_id}/calendar.ics")
@inject
def download_interview_ics(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
) -> Response:
    """Download a single interview as an .ics calendar file"""
    try:
        # Get interview details
        interview = controller.get_interview_view(interview_id)

        if not interview.scheduled_at:
            raise HTTPException(
                status_code=400,
                detail="Interview is not scheduled yet"
            )

        # Build event description
        description_parts = []
        if interview.description:
            description_parts.append(interview.description)
        if interview.candidate_name:
            description_parts.append(f"Candidate: {interview.candidate_name}")
        if interview.job_position_title:
            description_parts.append(f"Position: {interview.job_position_title}")
        if interview.interview_type:
            description_parts.append(f"Type: {interview.interview_type}")

        # Create ICS event
        event = ICSEvent(
            uid=f"interview-{interview_id}@careerpython.com",
            summary=interview.title or f"Interview - {interview.candidate_name or 'Candidate'}",
            start=interview.scheduled_at,
            end=interview.deadline_date,  # Use deadline as end if available
            description="\n".join(description_parts) if description_parts else None,
        )

        # Generate ICS content
        ics_service = ICSService()
        ics_content = ics_service.generate_event(event)

        # Return as downloadable file
        filename = f"interview-{interview_id}.ics"
        return Response(
            content=ics_content,
            media_type="text/calendar",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "text/calendar; charset=utf-8"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error generating ICS for interview {interview_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate calendar file")


@router.get("/{interview_id}/calendar-links")
@inject
def get_interview_calendar_links(
        interview_id: str,
        controller: Annotated[InterviewController, Depends(Provide[Container.interview_controller])],
        company_id: str = Depends(get_company_id_from_token),
) -> dict:
    """Get calendar links for an interview (Google Calendar, Outlook, etc.)"""
    try:
        # Get interview details
        interview = controller.get_interview_view(interview_id)

        if not interview.scheduled_at:
            raise HTTPException(
                status_code=400,
                detail="Interview is not scheduled yet"
            )

        # Build event description
        description_parts = []
        if interview.description:
            description_parts.append(interview.description)
        if interview.candidate_name:
            description_parts.append(f"Candidate: {interview.candidate_name}")
        if interview.job_position_title:
            description_parts.append(f"Position: {interview.job_position_title}")

        # Create ICS event for URL generation
        event = ICSEvent(
            uid=f"interview-{interview_id}@careerpython.com",
            summary=interview.title or f"Interview - {interview.candidate_name or 'Candidate'}",
            start=interview.scheduled_at,
            end=interview.deadline_date,
            description="\n".join(description_parts) if description_parts else None,
        )

        # Generate calendar URLs
        ics_service = ICSService()

        return {
            "google_calendar_url": ics_service.generate_google_calendar_url(event),
            "outlook_url": ics_service.generate_outlook_url(event),
            "ics_download_url": f"/api/company/interviews/{interview_id}/calendar.ics",
            "interview_id": interview_id,
            "scheduled_at": interview.scheduled_at.isoformat() if interview.scheduled_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error generating calendar links for interview {interview_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate calendar links")


