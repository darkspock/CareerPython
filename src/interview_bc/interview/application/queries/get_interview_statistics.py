"""Get interview statistics query"""
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.company_bc.company.domain import CompanyId
from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.application.queries.dtos.interview_statistics_dto import InterviewStatisticsDto
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface


@dataclass
class GetInterviewStatisticsQuery(Query):
    """Query to get interview statistics for dashboard header"""
    company_id: CompanyId  # Filter by company


class GetInterviewStatisticsQueryHandler(QueryHandler[GetInterviewStatisticsQuery, InterviewStatisticsDto]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetInterviewStatisticsQuery) -> InterviewStatisticsDto:
        """
        Find the stats for all pending interviews, and finished interviews in the last 30 days
        do not use several queries for each stats, as we the volume of data is low and is faster
        to calculate in python
        """
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        today_end = datetime(now.year, now.month, now.day, 23, 59, 59)

        recently_finished = self.interview_repository.find_finished_recent(days=30,company_id=query.company_id)

        pending_interviews = self.interview_repository.find_not_finished(company_id=query.company_id)


        # Count interviews pending to plan (no scheduled_at or no interviewers or no required_roles)
        pending_to_plan = sum(
            1 for i in pending_interviews
            if not i.scheduled_at or not i.interviewers or not i.required_roles
        )

        # Count planned interviews (have scheduled_at, interviewers, and required_roles)
        planned = sum(
            1 for i in pending_interviews
            if i.scheduled_at and i.interviewers and i.required_roles
        )

        # Count in progress (scheduled_at = today)
        in_progress = sum(
            1 for i in pending_interviews
            if i.scheduled_at and today_start <= i.scheduled_at <= today_end
        )

        # Count overdue (deadline_date < now and not finished)
        overdue = sum(
            1 for i in pending_interviews
            if i.deadline_date and i.deadline_date < now and not i.finished_at
        )

        # Count pending feedback/scoring (finished but no score or feedback)
        pending_feedback = sum(
            1 for i in pending_interviews
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
