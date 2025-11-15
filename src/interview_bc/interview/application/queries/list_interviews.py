"""List interviews query"""
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.application.queries.dtos.interview_list_dto import InterviewListDto
from src.interview_bc.interview.domain.enums.interview_enums import (
    InterviewStatusEnum,
    InterviewTypeEnum,
    InterviewProcessTypeEnum,
    InterviewFilterEnum
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
    filter_by: Optional[str] = None  # InterviewFilterEnum value - filter name (e.g., 'PENDING_TO_PLAN', 'OVERDUE')
    limit: int = 50
    offset: int = 0


class ListInterviewsQueryHandler(QueryHandler[ListInterviewsQuery, List[InterviewListDto]]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: ListInterviewsQuery) -> List[InterviewListDto]:
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
                        status = InterviewStatusEnum.PENDING
                    elif status_upper == "DISABLED":
                        status = InterviewStatusEnum.DISCARDED
                    elif status_upper == "PENDING":
                        status = InterviewStatusEnum.PENDING  # PENDING maps to ENABLED enum
                    else:
                        # Try to find enum member by name
                        try:
                            status = InterviewStatusEnum[status_upper]
                        except (KeyError, ValueError):
                            status = None  # Invalid status, ignore filter

        # Handle filter_by using InterviewFilterEnum
        filter_by_str = None
        has_scheduled_at_and_interviewers_flag = False
        effective_from_date = query.from_date
        effective_to_date = query.to_date
        
        if query.filter_by:
            try:
                filter_enum = InterviewFilterEnum(query.filter_by.upper())
                # Map filter enum to repository filter parameters
                if filter_enum == InterviewFilterEnum.PENDING_TO_PLAN:
                    filter_by_str = 'unscheduled'
                elif filter_enum == InterviewFilterEnum.PLANNED:
                    has_scheduled_at_and_interviewers_flag = True
                elif filter_enum == InterviewFilterEnum.OVERDUE:
                    filter_by_str = 'deadline'
                    # Set to_date to now for overdue filter if not specified
                    if not effective_to_date:
                        effective_to_date = datetime.utcnow()
                elif filter_enum == InterviewFilterEnum.IN_PROGRESS:
                    # Filter for today's interviews
                    today_start = datetime(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day)
                    today_end = datetime(datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day, 23, 59, 59)
                    effective_from_date = today_start
                    effective_to_date = today_end
                    filter_by_str = 'scheduled'
                # For RECENTLY_FINISHED and PENDING_FEEDBACK, we'll filter in Python after fetching
            except ValueError:
                # Invalid filter enum, use as-is (backward compatibility)
                filter_by_str = query.filter_by

        # Use the new method with JOINs that returns ReadModels
        read_models = self.interview_repository.find_by_filters_with_joins(
            candidate_id=query.candidate_id,
            candidate_name=query.candidate_name,
            job_position_id=query.job_position_id,
            interview_type=interview_type,
            process_type=process_type,
            status=status,
            required_role_id=query.required_role_id,
            interviewer_user_id=query.interviewer_user_id,
            created_by=query.created_by,
            from_date=effective_from_date,
            to_date=effective_to_date,
            filter_by=filter_by_str,
            has_scheduled_at_and_interviewers=has_scheduled_at_and_interviewers_flag or use_scheduled_filter,
            limit=query.limit,
            offset=query.offset
        )

        # Convert ReadModels to DTOs
        interview_dtos = [InterviewListDto.from_read_model(read_model) for read_model in read_models]

        # Apply additional filters that need to be done in Python
        if query.filter_by:
            try:
                filter_enum = InterviewFilterEnum(query.filter_by.upper())
                from datetime import timedelta
                now = datetime.utcnow()
                thirty_days_ago = now - timedelta(days=30)

                if filter_enum == InterviewFilterEnum.RECENTLY_FINISHED:
                    interview_dtos = [
                        dto for dto in interview_dtos
                        if dto.finished_at and dto.finished_at >= thirty_days_ago
                    ]
                elif filter_enum == InterviewFilterEnum.PENDING_FEEDBACK:
                    interview_dtos = [
                        dto for dto in interview_dtos
                        if dto.finished_at and (dto.score is None or not dto.feedback)
                    ]
            except ValueError:
                pass  # Invalid filter enum, return all

        return interview_dtos
