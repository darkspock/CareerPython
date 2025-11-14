"""Get interview statistics query"""
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.interview_bc.interview.application.queries.dtos.interview_statistics_dto import InterviewStatisticsDto
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetInterviewStatisticsQuery(Query):
    """Query to get interview statistics for dashboard header"""
    company_id: str  # Filter by company


class GetInterviewStatisticsQueryHandler(QueryHandler[GetInterviewStatisticsQuery, InterviewStatisticsDto]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetInterviewStatisticsQuery) -> InterviewStatisticsDto:
        """Get interview statistics"""
        from src.interview_bc.interview.domain.enums.interview_enums import InterviewStatusEnum
        
        now = datetime.utcnow()
        thirty_days_ago = now - timedelta(days=30)
        today_start = datetime(now.year, now.month, now.day)
        today_end = datetime(now.year, now.month, now.day, 23, 59, 59)
        
        # Get all interviews for the company (we'll filter by company_id in repository if needed)
        # For now, we'll get all interviews and filter in memory
        # TODO: Add company_id filter to repository if needed
        
        all_interviews = self.interview_repository.find_by_filters(limit=10000)
        
        # Filter by company if we have job_position_id (which has company_id)
        # For now, we'll assume all interviews belong to the company
        # TODO: Add proper company filtering through job_position or candidate
        
        # Count interviews pending to plan (no scheduled_at or no interviewers)
        pending_to_plan = sum(
            1 for i in all_interviews
            if not i.scheduled_at or not i.interviewers
        )
        
        # Count planned interviews (have scheduled_at and interviewers)
        planned = sum(
            1 for i in all_interviews
            if i.scheduled_at and i.interviewers
        )
        
        # Count in progress (scheduled_at = today)
        in_progress = sum(
            1 for i in all_interviews
            if i.scheduled_at and today_start <= i.scheduled_at <= today_end
        )
        
        # Count recently finished (finished_at in last 30 days)
        recently_finished = sum(
            1 for i in all_interviews
            if i.finished_at and i.finished_at >= thirty_days_ago
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
            recently_finished=recently_finished,
            overdue=overdue,
            pending_feedback=pending_feedback
        )

