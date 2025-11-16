"""
Interview Controller for admin interview management operations
"""
import logging
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException

from adapters.http.company_app.interview.schemas.interview_management import (
    InterviewResource, InterviewFullResource, InterviewListResource, InterviewStatsResource,
    InterviewActionResource, InterviewScoreSummaryResource, InterviewLinkResource
)
from core.config import settings
from src.company_bc.company.domain import CompanyId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.interview_bc.interview.application.commands.create_interview import CreateInterviewCommand
from src.interview_bc.interview.application.commands.finish_interview import FinishInterviewCommand
from src.interview_bc.interview.application.commands.generate_interview_link import GenerateInterviewLinkCommand
from src.interview_bc.interview.application.commands.start_interview import StartInterviewCommand
from src.interview_bc.interview.application.commands.submit_interview_answer_by_token import \
    SubmitInterviewAnswerByTokenCommand
from src.interview_bc.interview.application.commands.update_interview import UpdateInterviewCommand
from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.application.queries.dtos.interview_list_dto import InterviewListDto
from src.interview_bc.interview.application.queries.dtos.interview_statistics_dto import InterviewStatisticsDto
from src.interview_bc.interview.application.queries.get_interview_by_id import GetInterviewByIdQuery
from src.interview_bc.interview.application.queries.get_interview_by_token import GetInterviewByTokenQuery
from src.interview_bc.interview.application.queries.get_interview_questions_by_token import \
    GetInterviewQuestionsByTokenQuery, InterviewQuestionsResponse
from src.interview_bc.interview.application.queries.get_interview_score_summary import GetInterviewScoreSummaryQuery, \
    InterviewScoreSummaryDto
from src.interview_bc.interview.application.queries.get_interview_statistics import GetInterviewStatisticsQuery
from src.interview_bc.interview.application.queries.get_interviews_by_candidate import GetInterviewsByCandidateQuery
from src.interview_bc.interview.application.queries.get_scheduled_interviews import GetScheduledInterviewsQuery
from src.interview_bc.interview.application.queries.list_interviews import ListInterviewsQuery

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
            company_id: str,
            candidate_id: Optional[str] = None,
            candidate_name: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[str] = None,
            process_type: Optional[str] = None,
            status: Optional[str] = None,
            required_role_id: Optional[str] = None,
            interviewer_user_id: Optional[str] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            filter_by: Optional[str] = None,
            limit: int = 50,
            offset: int = 0
    ) -> InterviewListResource:
        """List interviews with optional filtering. Returns InterviewListResource"""
        try:
            from src.interview_bc.interview.domain.enums.interview_enums import (
                InterviewStatusEnum,
                InterviewTypeEnum,
                InterviewProcessTypeEnum
            )
            from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import \
                InterviewRepositoryInterface
            from core.container import Container

            # Convert string enums to enum values for count query
            interview_type_enum = None
            if interview_type:
                try:
                    interview_type_enum = InterviewTypeEnum(interview_type)
                except ValueError:
                    interview_type_enum = None

            process_type_enum = None
            if process_type:
                try:
                    process_type_enum = InterviewProcessTypeEnum(process_type)
                except ValueError:
                    process_type_enum = None

            status_enum = None
            has_scheduled_filter = False  # Special filter for "SCHEDULED" status
            if status:
                status_upper = status.upper()
                # Handle "SCHEDULED" as a special case - means interviews with scheduled_at and interviewers
                if status_upper == "SCHEDULED":
                    has_scheduled_filter = True
                    status_enum = None  # Don't filter by status enum, use scheduled filter instead
                else:
                    try:
                        # Try direct conversion first (works for "PENDING", "IN_PROGRESS", etc.)
                        status_enum = InterviewStatusEnum(status_upper)
                    except ValueError:
                        # Handle legacy or mismatched values
                        # Map "ENABLED" to ENABLED enum (which has value "PENDING")
                        if status_upper == "ENABLED":
                            status_enum = InterviewStatusEnum.PENDING
                        elif status_upper == "DISABLED":
                            status_enum = InterviewStatusEnum.DISCARDED
                        elif status_upper == "PENDING":
                            status_enum = InterviewStatusEnum.PENDING  # PENDING maps to ENABLED enum
                        else:
                            # Try to find enum member by name
                            try:
                                status_enum = InterviewStatusEnum[status_upper]
                            except (KeyError, ValueError):
                                status_enum = None  # Invalid status, ignore filter

            # Get total count
            container = Container()
            interview_repository: InterviewRepositoryInterface = container.interview_repository()
            total = interview_repository.count_by_filters(
                candidate_id=candidate_id,
                candidate_name=candidate_name,
                job_position_id=job_position_id,
                interview_type=interview_type_enum,
                process_type=process_type_enum,
                status=status_enum,
                required_role_id=required_role_id,
                interviewer_user_id=interviewer_user_id,
                created_by=created_by,
                from_date=from_date,
                to_date=to_date,
                filter_by=filter_by,
                has_scheduled_at_and_interviewers=has_scheduled_filter
            )

            # Get paginated results
            query = ListInterviewsQuery(
                candidate_id=candidate_id,
                candidate_name=candidate_name,
                job_position_id=job_position_id,
                interview_type=interview_type,
                process_type=process_type,
                status=status,
                required_role_id=required_role_id,
                interviewer_user_id=interviewer_user_id,
                created_by=created_by,
                from_date=from_date,
                to_date=to_date,
                filter_by=filter_by,
                limit=limit,
                offset=offset
            )

            interviews: List[InterviewListDto] = self._query_bus.query(query)
            
            # Calculate current page from offset and limit
            current_page = (offset // limit) + 1 if limit > 0 else 1
            
            return InterviewListResource(
                interviews=[InterviewFullResource.from_list_dto(dto) for dto in interviews],
                total=total,
                page=current_page,
                page_size=limit
            )

        except Exception as e:
            logger.error(f"Error listing interviews: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve interviews")

    def get_interview_by_id(self, interview_id: str) -> InterviewResource:
        """Get interview by ID (for editing - only interview fields)"""
        try:
            query = GetInterviewByIdQuery(interview_id=interview_id)
            interview: InterviewDto = self._query_bus.query(query)

            if not interview:
                raise HTTPException(status_code=404, detail="Interview not found")

            return InterviewResource.from_dto(interview)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting interview {interview_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve interview")

    def get_interview_view(self, interview_id: str) -> InterviewFullResource:
        """Get interview by ID with full denormalized information (for viewing)"""
        try:
            query = GetInterviewByIdQuery(interview_id=interview_id)
            interview: InterviewDto = self._query_bus.query(query)

            if not interview:
                raise HTTPException(status_code=404, detail="Interview not found")

            return InterviewFullResource.from_dto(self._query_bus, interview)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting interview view {interview_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve interview")

    def get_interviews_by_candidate(
            self,
            candidate_id: str,
    ) -> List[InterviewFullResource]:
        """Get interviews for a specific candidate"""
        try:
            query = GetInterviewsByCandidateQuery(
                candidate_id=candidate_id,
            )

            interviews: List[InterviewDto] = self._query_bus.query(query)
            return [InterviewFullResource.from_dto(self._query_bus, dto) for dto in interviews]

        except Exception as e:
            logger.error(f"Error getting interviews for candidate {candidate_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve candidate interviews")

    def get_scheduled_interviews(
            self,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
    ) -> List[InterviewFullResource]:
        """Get scheduled interviews"""
        try:
            query = GetScheduledInterviewsQuery(
                from_date=from_date if from_date else datetime(2000, 1, 1),
                to_date=to_date if to_date else datetime.now(),
            )

            interviews: List[InterviewDto] = self._query_bus.query(query)
            return [InterviewFullResource.from_dto(self._query_bus, dto) for dto in interviews]

        except Exception as e:
            logger.error(f"Error getting scheduled interviews: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve scheduled interviews")

    def create_interview(
            self,
            candidate_id: str,
            required_roles: List[str],
            interview_mode: str,
            interview_type: str,
            stage_id: str,
            job_position_id: str,
            process_type: Optional[str] = None,
            application_id: Optional[str] = None,
            interview_template_id: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            scheduled_at: Optional[str] = None,
            deadline_date: Optional[str] = None,
            interviewers: Optional[List[str]] = None,
            created_by: Optional[str] = None
    ) -> InterviewActionResource:
        """Create a new interview"""
        try:
            command = CreateInterviewCommand(
                candidate_id=candidate_id,
                required_roles=required_roles,
                interview_mode=interview_mode,
                interview_type=interview_type,
                process_type=process_type,
                workflow_stage_id=stage_id,
                job_position_id=job_position_id,
                application_id=application_id,
                interview_template_id=interview_template_id,
                title=title,
                description=description,
                scheduled_at=scheduled_at,
                deadline_date=deadline_date,
                interviewers=interviewers,
                created_by=created_by
            )

            self._command_bus.execute(command)

            return InterviewActionResource(
                message="Interview created successfully",
                status="success",
                interview_id=None
            )

        except Exception as e:
            logger.error(f"Error creating interview: {e}", exc_info=True)
            error_message = str(e) if str(e) else "Failed to create interview"
            raise HTTPException(status_code=500, detail=error_message)

    def update_interview(
            self,
            interview_id: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            scheduled_at: Optional[str] = None,
            deadline_date: Optional[str] = None,
            process_type: Optional[str] = None,
            interview_type: Optional[str] = None,
            interview_mode: Optional[str] = None,
            required_roles: Optional[List[str]] = None,
            interviewers: Optional[List[str]] = None,
            interviewer_notes: Optional[str] = None,
            feedback: Optional[str] = None,
            score: Optional[float] = None,
            updated_by: Optional[str] = None
    ) -> InterviewActionResource:
        """Update an existing interview"""
        try:
            command = UpdateInterviewCommand(
                interview_id=interview_id,
                title=title,
                description=description,
                scheduled_at=scheduled_at,
                deadline_date=deadline_date,
                process_type=process_type,
                interview_type=interview_type,
                interview_mode=interview_mode,
                required_roles=required_roles,
                interviewers=interviewers,
                interviewer_notes=interviewer_notes,
                feedback=feedback,
                score=score,
                updated_by=updated_by
            )

            self._command_bus.execute(command)

            return InterviewActionResource(
                message="Interview updated successfully",
                status="success",
                interview_id=interview_id
            )

        except Exception as e:
            logger.error(f"Error updating interview: {e}", exc_info=True)
            error_message = str(e) if str(e) else "Failed to update interview"
            raise HTTPException(status_code=500, detail=error_message)

    def start_interview(
            self,
            interview_id: str,
            started_by: str
    ) -> InterviewActionResource:
        """Start an interview"""
        try:
            command = StartInterviewCommand(
                interview_id=interview_id,
                started_by=started_by
            )

            self._command_bus.execute(command)

            return InterviewActionResource(
                message="Interview started successfully",
                status="success",
                interview_id=interview_id
            )

        except Exception as e:
            logger.error(f"Error starting interview {interview_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to start interview")

    def finish_interview(
            self,
            interview_id: str,
            finished_by: str
    ) -> InterviewActionResource:
        """Finish an interview"""
        try:
            command = FinishInterviewCommand(
                interview_id=interview_id,
                finished_by=finished_by
            )

            self._command_bus.execute(command)

            return InterviewActionResource(
                message="Interview finished successfully",
                status="success",
                interview_id=interview_id
            )

        except Exception as e:
            logger.error(f"Error finishing interview {interview_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to finish interview")

    def get_interview_score_summary(self, interview_id: str) -> InterviewScoreSummaryResource:
        """Get interview score summary"""
        try:
            query = GetInterviewScoreSummaryQuery(interview_id=interview_id)
            score_summary: InterviewScoreSummaryDto = self._query_bus.query(query)

            return InterviewScoreSummaryResource.from_dto(score_summary)

        except Exception as e:
            logger.error(f"Error getting score summary for interview {interview_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve interview score summary")

    def generate_interview_link(
            self,
            interview_id: str,
            expires_in_days: int = 30,
            generated_by: Optional[str] = None
    ) -> InterviewLinkResource:
        """Generate a shareable link for an interview"""
        try:
            command = GenerateInterviewLinkCommand(
                interview_id=interview_id,
                expires_in_days=expires_in_days,
                generated_by=generated_by
            )

            self._command_bus.execute(command)

            # Get the updated interview to retrieve the link
            interview_dto: InterviewDto = self._query_bus.query(GetInterviewByIdQuery(interview_id=interview_id))
            interview = InterviewResource.from_dto(interview_dto)

            return InterviewLinkResource(
                message="Interview link generated successfully",
                status="success",
                interview_id=interview_id,
                link=interview.shareable_link,
                link_token=interview.link_token,
                expires_in_days=expires_in_days,
                expires_at=interview.link_expires_at.isoformat() if interview.link_expires_at else None
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error generating link for interview {interview_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to generate interview link: {str(e)}")

    def get_interview_by_token(
            self,
            interview_id: str,
            token: str
    ) -> InterviewFullResource:
        """Get interview by ID and token for secure link access (with full denormalized information)"""
        try:
            query = GetInterviewByTokenQuery(
                interview_id=interview_id,
                token=token
            )

            interview: InterviewDto = self._query_bus.query(query)
            return InterviewFullResource.from_dto(self._query_bus, interview)

        except Exception as e:
            logger.error(f"Error getting interview {interview_id} by token: {e}")
            raise HTTPException(status_code=404, detail="Interview not found or token is invalid/expired")

    def get_interview_statistics(
            self,
            company_id: str
    ) -> InterviewStatsResource:
        """Get interview statistics for a company"""
        try:
            query = GetInterviewStatisticsQuery(company_id=CompanyId(company_id))
            stats: InterviewStatisticsDto = self._query_bus.query(query)
            return InterviewStatsResource.from_dto(stats)
        except Exception as e:
            logger.error(f"Error getting interview statistics: {e}", exc_info=True)
            error_message = str(e) if str(e) else "Failed to retrieve interview statistics"
            raise HTTPException(status_code=500, detail=error_message)

    def get_interview_questions_by_token(
            self,
            interview_id: str,
            token: str
    ) -> InterviewQuestionsResponse:
        """Get interview questions by token for public access"""
        try:
            query = GetInterviewQuestionsByTokenQuery(
                interview_id=interview_id,
                token=token
            )
            result: InterviewQuestionsResponse = self._query_bus.query(query)
            return result

        except Exception as e:
            logger.error(f"Error getting interview questions for interview {interview_id} by token: {e}")
            raise HTTPException(status_code=404, detail="Interview not found or token is invalid/expired")

    def submit_interview_answer_by_token(
            self,
            interview_id: str,
            token: str,
            question_id: str,
            answer_text: Optional[str] = None,
            question_text: Optional[str] = None
    ) -> dict:
        """Submit interview answer by token for public access"""
        try:
            command = SubmitInterviewAnswerByTokenCommand(
                interview_id=interview_id,
                token=token,
                question_id=question_id,
                answer_text=answer_text,
                question_text=question_text
            )
            self._command_bus.dispatch(command)
            return {"message": "Answer submitted successfully", "status": "success"}

        except Exception as e:
            logger.error(f"Error submitting answer for interview {interview_id} by token: {e}")
            raise HTTPException(status_code=400, detail=str(e))
