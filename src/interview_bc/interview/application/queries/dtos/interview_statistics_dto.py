"""Interview statistics DTO"""
from dataclasses import dataclass


@dataclass
class InterviewStatisticsDto:
    """DTO for interview statistics"""
    pending_to_plan: int  # No scheduled_at or no interviewers
    planned: int  # Has scheduled_at and interviewers
    in_progress: int  # scheduled_at = today
    recently_finished: int  # finished_at in last 30 days
    overdue: int  # deadline_date < now and not finished
    pending_feedback: int  # finished but no score or feedback
