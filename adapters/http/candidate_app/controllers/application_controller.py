"""
Application Controller for handling job application operations
"""
import logging
from typing import Any, List, Optional

from fastapi import HTTPException

from adapters.http.candidate_app.schemas.candidate_job_applications import (
    CandidateJobApplicationSummary,
    JobApplicationListFilters
)
from src.company_bc.candidate_application.application.commands.create_candidate_application import \
    CreateCandidateApplicationCommand
from src.company_bc.candidate_application.application.commands.update_application_status import \
    UpdateApplicationStatusCommand
from src.company_bc.candidate_application.application.queries.can_user_process_application_query import \
    CanUserProcessApplicationQuery
from src.company_bc.candidate_application.application.queries.get_applications_by_candidate_id import \
    GetApplicationsByCandidateIdQuery
from src.company_bc.candidate_application.application.queries.shared.candidate_application_dto import \
    CandidateApplicationDto
from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus

logger = logging.getLogger(__name__)


class ApplicationController:
    """Controller for managing candidate job applications"""

    def __init__(
            self,
            command_bus: CommandBus,
            query_bus: QueryBus,
            job_position_repository: Optional[Any] = None
    ):
        self._command_bus = command_bus
        self._query_bus = query_bus
        self._job_position_repository = job_position_repository

    def get_applications_by_candidate(
            self,
            candidate_id: str,
            filters: JobApplicationListFilters
    ) -> List[CandidateJobApplicationSummary]:
        """Get all applications for a candidate with optional filtering"""
        try:
            query = GetApplicationsByCandidateIdQuery(
                candidate_id=candidate_id,
                status_filter=filters.status.value if filters.status else None,
                limit=None  # Don't limit at query level if we need to filter by company
            )

            applications_dto: List[CandidateApplicationDto] = self._query_bus.query(query)

            # Filter by company_id if provided
            if filters.company_id:
                applications_dto = [
                    dto for dto in applications_dto
                    if self._get_company_id_for_position(dto.job_position_id) == filters.company_id
                ]

            # Apply limit after company filtering
            if filters.limit and len(applications_dto) > filters.limit:
                applications_dto = applications_dto[:filters.limit]

            # Convert DTOs to response schema
            return [
                self._dto_to_summary(dto) for dto in applications_dto
            ]

        except Exception as e:
            logger.error(f"Error getting applications for candidate {candidate_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve applications")

    def _get_company_id_for_position(self, job_position_id: str) -> Optional[str]:
        """Get the company ID for a job position"""
        if not self._job_position_repository or not job_position_id:
            return None
        try:
            from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
            job_position = self._job_position_repository.get_by_id(
                JobPositionId.from_string(job_position_id)
            )
            if job_position:
                return str(job_position.company_id) if job_position.company_id else None
        except Exception as e:
            logger.warning(f"Could not fetch company for position {job_position_id}: {e}")
        return None

    def create_application(
            self,
            candidate_id: str,
            job_position_id: str,
            cover_letter: Optional[str] = None
    ) -> str:
        """Create a new job application"""
        try:
            # Generate unique ID for the application
            from src.framework.domain.entities.base import generate_id
            application_id = generate_id()

            # Create command with notes field (cover_letter maps to notes for now)
            command = CreateCandidateApplicationCommand(
                candidate_id=candidate_id,
                job_position_id=job_position_id,
                notes=cover_letter or "",
                application_id=application_id
            )

            self._command_bus.execute(command)
            return application_id  # Return the generated ID

        except Exception as e:
            logger.error(f"Error creating application: {e}")
            raise HTTPException(status_code=500, detail="Failed to create application")

    def update_application_status(
            self,
            application_id: str,
            status: ApplicationStatusEnum,
            notes: Optional[str] = None
    ) -> None:
        """Update application status"""
        try:
            command = UpdateApplicationStatusCommand(
                application_id=application_id,
                status=status,
                notes=notes
            )

            self._command_bus.execute(command)

        except Exception as e:
            logger.error(f"Error updating application status: {e}")
            raise HTTPException(status_code=500, detail="Failed to update application status")

    def _dto_to_summary(self, dto: CandidateApplicationDto) -> CandidateJobApplicationSummary:
        """Convert DTO to summary response"""
        job_title = "Position"
        company_name = "Company"

        # Try to fetch real job position data
        if self._job_position_repository and dto.job_position_id:
            try:
                from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
                job_position = self._job_position_repository.get_by_id(
                    JobPositionId.from_string(dto.job_position_id)
                )
                if job_position:
                    job_title = job_position.title
                    company_name = job_position.company_name or "Company"
            except Exception as e:
                logger.warning(f"Could not fetch job position {dto.job_position_id}: {e}")

        return CandidateJobApplicationSummary(
            id=dto.id,
            job_position_id=dto.job_position_id,
            job_title=job_title,
            company_name=company_name,
            status=dto.application_status,
            task_status=dto.task_status.value if dto.task_status else "pending",
            created_at=dto.applied_at,
            updated_at=dto.updated_at,
            applied_at=dto.applied_at,
            has_customized_content=bool(dto.notes and len(dto.notes) > 0)
        )

    def can_user_process_application(
            self,
            user_id: str,
            application_id: str,
            company_id: str
    ) -> bool:
        """Check if user has permission to process an application at its current stage

        Args:
            user_id: ID of the user
            application_id: ID of the application
            company_id: ID of the company

        Returns:
            True if user can process, False otherwise
        """
        try:
            query = CanUserProcessApplicationQuery(
                user_id=user_id,
                application_id=application_id,
                company_id=company_id
            )
            can_process: bool = self._query_bus.query(query)
            return can_process

        except Exception as e:
            logger.error(f"Error checking permission for user {user_id} on application {application_id}: {e}")
            return False
