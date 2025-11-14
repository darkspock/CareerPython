"""List interviews query"""
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.domain.enums.interview_enums import (
    InterviewStatusEnum,
    InterviewTypeEnum,
    InterviewProcessTypeEnum
)
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface

logger = logging.getLogger(__name__)


@dataclass
class ListInterviewsQuery(Query):
    """Query to list interviews with advanced filters"""
    candidate_id: Optional[str] = None
    candidate_name: Optional[str] = None  # Search by candidate name
    job_position_id: Optional[str] = None
    interview_type: Optional[str] = None
    process_type: Optional[str] = None  # InterviewProcessTypeEnum
    status: Optional[str] = None
    required_role_id: Optional[str] = None  # Filter by CompanyRole ID (using JSON operators)
    interviewer_user_id: Optional[str] = None  # Filter by interviewer (CompanyUserId)
    created_by: Optional[str] = None
    from_date: Optional[datetime] = None  # Filter by scheduled_at or deadline_date
    to_date: Optional[datetime] = None  # Filter by scheduled_at or deadline_date
    filter_by: Optional[str] = None  # 'scheduled' or 'deadline' - which date field to filter
    limit: int = 50
    offset: int = 0


class ListInterviewsQueryHandler(QueryHandler[ListInterviewsQuery, List[InterviewDto]]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: ListInterviewsQuery) -> List[InterviewDto]:
        # Convert string enums to actual enum values
        interview_type = None
        if query.interview_type:
            try:
                interview_type = InterviewTypeEnum(query.interview_type)
            except ValueError:
                interview_type = None

        process_type = None
        if query.process_type:
            try:
                process_type = InterviewProcessTypeEnum(query.process_type)
            except ValueError:
                process_type = None

        status = None
        use_scheduled_filter = False  # Special filter for "SCHEDULED" status
        if query.status:
            status_upper = query.status.upper()
            # Handle "SCHEDULED" as a special case - means interviews with scheduled_at and interviewers
            if status_upper == "SCHEDULED":
                use_scheduled_filter = True
                status = None  # Don't filter by status enum, use scheduled filter instead
            else:
                try:
                    # Try direct conversion first (works for "PENDING", "IN_PROGRESS", etc.)
                    status = InterviewStatusEnum(status_upper)
                except ValueError:
                    # Handle legacy or mismatched values
                    # Map "ENABLED" to ENABLED enum (which has value "PENDING")
                    if status_upper == "ENABLED":
                        status = InterviewStatusEnum.ENABLED
                    elif status_upper == "DISABLED":
                        status = InterviewStatusEnum.DISCARDED
                    elif status_upper == "PENDING":
                        status = InterviewStatusEnum.ENABLED  # PENDING maps to ENABLED enum
                    else:
                        # Try to find enum member by name
                        try:
                            status = InterviewStatusEnum[status_upper]
                        except (KeyError, ValueError):
                            status = None  # Invalid status, ignore filter

        interviews = self.interview_repository.find_by_filters(
            candidate_id=query.candidate_id,
            candidate_name=query.candidate_name,
            job_position_id=query.job_position_id,
            interview_type=interview_type,
            process_type=process_type,
            status=status,
            required_role_id=query.required_role_id,
            interviewer_user_id=query.interviewer_user_id,
            created_by=query.created_by,
            from_date=query.from_date,
            to_date=query.to_date,
            filter_by=query.filter_by,
            has_scheduled_at_and_interviewers=use_scheduled_filter,  # Special filter for "SCHEDULED" status
            limit=query.limit,
            offset=query.offset
        )

        return [InterviewDto.from_entity(interview) for interview in interviews]
