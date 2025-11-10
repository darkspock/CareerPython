"""
Interview Controller for admin interview management operations
"""
import logging
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException

from src.interview.interview.application.commands.create_interview import CreateInterviewCommand
from src.interview.interview.application.commands.finish_interview import FinishInterviewCommand
from src.interview.interview.application.commands.start_interview import StartInterviewCommand
from src.interview.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview.interview.application.queries.get_interview_by_id import GetInterviewByIdQuery
from src.interview.interview.application.queries.get_interview_score_summary import GetInterviewScoreSummaryQuery, \
    InterviewScoreSummaryDto
from src.interview.interview.application.queries.get_interviews_by_candidate import GetInterviewsByCandidateQuery
from src.interview.interview.application.queries.get_scheduled_interviews import GetScheduledInterviewsQuery
from src.interview.interview.application.queries.list_interviews import ListInterviewsQuery
from src.interview.interview.domain.enums.interview_enums import InterviewTypeEnum
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus

logger = logging.getLogger(__name__)


class InterviewController:
    """Controller for managing interviews in the admin panel"""

    def __init__(
            self,
            command_bus: CommandBus,
            query_bus: QueryBus,
    ):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def list_interviews(
            self,
            candidate_id: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[str] = None,
            status: Optional[str] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            limit: int = 50,
            offset: int = 0
    ) -> List[InterviewDto]:
        """List interviews with optional filtering"""
        try:
            query = ListInterviewsQuery(
                candidate_id=candidate_id,
                job_position_id=job_position_id,
                interview_type=interview_type,
                status=status,
                created_by=created_by,
                from_date=from_date,
                to_date=to_date,
                limit=limit,
                offset=offset
            )

            interviews: List[InterviewDto] = self._query_bus.query(query)
            return interviews

        except Exception as e:
            logger.error(f"Error listing interviews: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve interviews")

    def get_interview_by_id(self, interview_id: str) -> InterviewDto:
        """Get interview by ID"""
        try:
            query = GetInterviewByIdQuery(interview_id=interview_id)
            interview: InterviewDto = self._query_bus.query(query)

            if not interview:
                raise HTTPException(status_code=404, detail="Interview not found")

            return interview

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting interview {interview_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve interview")

    def get_interviews_by_candidate(
            self,
            candidate_id: str,
    ) -> List[InterviewDto]:
        """Get interviews for a specific candidate"""
        try:
            query = GetInterviewsByCandidateQuery(
                candidate_id=candidate_id,
            )

            interviews: List[InterviewDto] = self._query_bus.query(query)
            return interviews

        except Exception as e:
            logger.error(f"Error getting interviews for candidate {candidate_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve candidate interviews")

    def get_scheduled_interviews(
            self,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
    ) -> List[InterviewDto]:
        """Get scheduled interviews"""
        try:
            query = GetScheduledInterviewsQuery(
                from_date=from_date if from_date else datetime(2000, 1, 1),
                to_date=to_date if to_date else datetime.now(),
            )

            interviews: List[InterviewDto] = self._query_bus.query(query)
            return interviews

        except Exception as e:
            logger.error(f"Error getting scheduled interviews: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve scheduled interviews")

    def create_interview(
            self,
            candidate_id: str,
            interview_type: str = InterviewTypeEnum.JOB_POSITION.value,
            job_position_id: Optional[str] = None,
            application_id: Optional[str] = None,
            interview_template_id: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            scheduled_at: Optional[str] = None,
            interviewers: Optional[List[str]] = None,
            created_by: Optional[str] = None
    ) -> dict:
        """Create a new interview"""
        try:
            command = CreateInterviewCommand(
                candidate_id=candidate_id,
                interview_type=interview_type,
                job_position_id=job_position_id,
                application_id=application_id,
                interview_template_id=interview_template_id,
                title=title,
                description=description,
                scheduled_at=scheduled_at,
                interviewers=interviewers,
                created_by=created_by
            )

            self._command_bus.execute(command)

            return {
                "message": "Interview created successfully",
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error creating interview: {e}")
            raise HTTPException(status_code=500, detail="Failed to create interview")

    def start_interview(
            self,
            interview_id: str,
            started_by: str
    ) -> dict:
        """Start an interview"""
        try:
            command = StartInterviewCommand(
                interview_id=interview_id,
                started_by=started_by
            )

            self._command_bus.execute(command)

            return {
                "message": "Interview started successfully",
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error starting interview {interview_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to start interview")

    def finish_interview(
            self,
            interview_id: str,
            finished_by: str
    ) -> dict:
        """Finish an interview"""
        try:
            command = FinishInterviewCommand(
                interview_id=interview_id,
                finished_by=finished_by
            )

            self._command_bus.execute(command)

            return {
                "message": "Interview finished successfully",
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error finishing interview {interview_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to finish interview")

    def get_interview_score_summary(self, interview_id: str) -> dict:
        """Get interview score summary"""
        try:
            query = GetInterviewScoreSummaryQuery(interview_id=interview_id)
            score_summary: InterviewScoreSummaryDto = self._query_bus.query(query)

            return {
                "interview_id": interview_id,
                "score_summary": score_summary,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error getting score summary for interview {interview_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve interview score summary")
