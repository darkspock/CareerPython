"""Get interview statistics query"""
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.application.queries.dtos.interview_statistics_dto import InterviewStatisticsDto
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface


@dataclass
class GetInterviewStatisticsQuery(Query):
    """Query to get interview statistics for dashboard header"""
    company_id: str  # Filter by company


class GetInterviewStatisticsQueryHandler(QueryHandler[GetInterviewStatisticsQuery, InterviewStatisticsDto]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetInterviewStatisticsQuery) -> InterviewStatisticsDto:
        """
        Get interview statistics by fetching all interviews from the last month
        and calculating statistics in Python for consistency with filters.
        """
        now = datetime.utcnow()
        thirty_days_ago = now - timedelta(days=30)
        today_start = datetime(now.year, now.month, now.day)
        today_end = datetime(now.year, now.month, now.day, 23, 59, 59)

        recently_finished = self.interview_repository.find_finished_recent(days=30)

        # Get all interviews from the last month (created_at >= 30 days ago)
        # This ensures consistency between statistics and filters
        # For a typical company, this should be a manageable number of interviews
        # We use created_at as the date field to get all interviews from the period
        all_interviews = self.interview_repository.find_by_filters(
            filter_by=None,  # No specific date filter, get all from the period (uses created_at as fallback)
            limit=10000  # Large limit to get all interviews from the period
        )

        # Filter by company if needed (through job_position_id or candidate)
        # TODO: Add proper company filtering through job_position or candidate
        # For now, we'll calculate statistics on all interviews

        # Count interviews pending to plan (no scheduled_at or no interviewers or no required_roles)
        pending_to_plan = sum(
            1 for i in all_interviews
            if not i.scheduled_at or not i.interviewers or not i.required_roles
        )

        # Count planned interviews (have scheduled_at, interviewers, and required_roles)
        planned = sum(
            1 for i in all_interviews
            if i.scheduled_at and i.interviewers and i.required_roles
        )

        # Count in progress (scheduled_at = today)
        in_progress = sum(
            1 for i in all_interviews
            if i.scheduled_at and today_start <= i.scheduled_at <= today_end
        )

        # Count overdue (deadline_date < now and not finished)
        overdue = sum(
            1 for i in all_interviews
            if i.deadline_date and i.deadline_date < now and not i.finished_at
        )

        # Count pending feedback/scoring (finished but no score or feedback)
        pending_feedback = sum(
            1 for i in all_interviews
            if i.finished_at and (i.score is None or not i.feedback)
        )

        return InterviewStatisticsDto(
            pending_to_plan=pending_to_plan,
            planned=planned,
            in_progress=in_progress,
            recently_finished=len(recently_finished),
            overdue=overdue,
            pending_feedback=pending_feedback
        )
