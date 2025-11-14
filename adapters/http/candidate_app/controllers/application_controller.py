"""
Application Controller for handling job application operations
"""
import logging
from typing import List, Optional

from fastapi import HTTPException

from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.company_bc.candidate_application.application.commands.create_candidate_application import CreateCandidateApplicationCommand
from src.company_bc.candidate_application.application.commands.update_application_status import UpdateApplicationStatusCommand
from src.company_bc.candidate_application.application.queries.get_applications_by_candidate_id import GetApplicationsByCandidateIdQuery
from src.company_bc.candidate_application.application.queries.shared.candidate_application_dto import CandidateApplicationDto
from src.company_bc.candidate_application.application.services.stage_permission_service import StagePermissionService
from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import (
    CandidateApplicationRepositoryInterface
)
from adapters.http.candidate_app.schemas.candidate_job_applications import (
    CandidateJobApplicationSummary,
    JobApplicationListFilters
)

logger = logging.getLogger(__name__)


class ApplicationController:
    """Controller for managing candidate job applications"""

    def __init__(
        self,
        command_bus: CommandBus,
        query_bus: QueryBus,
        stage_permission_service: Optional[StagePermissionService] = None,
        application_repository: Optional[CandidateApplicationRepositoryInterface] = None
    ):
        self._command_bus = command_bus
        self._query_bus = query_bus
        self._stage_permission_service = stage_permission_service
        self._application_repository = application_repository

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
                limit=filters.limit
            )

            applications_dto: List[CandidateApplicationDto] = self._query_bus.query(query)

            # Convert DTOs to response schema
            return [
                self._dto_to_summary(dto) for dto in applications_dto
            ]

        except Exception as e:
            logger.error(f"Error getting applications for candidate {candidate_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve applications")

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
        return CandidateJobApplicationSummary(
            id=dto.id,
            job_title="Position",  # TODO: Fetch from job_position via job_position_id
            company_name="Company",  # TODO: Fetch from company via job_position
            status=dto.application_status,
            created_at=dto.applied_at,  # Use applied_at as created_at
            updated_at=dto.updated_at,
            applied_at=dto.applied_at,
            has_customized_content=bool(dto.notes and len(dto.notes) > 0)  # Use notes as indicator
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
        if not self._stage_permission_service or not self._application_repository:
            logger.warning("Permission service or repository not available, denying access")
            return False

        try:
            # Get application
            application = self._application_repository.get_by_id(
                CandidateApplicationId(application_id)
            )

            if not application:
                logger.error(f"Application {application_id} not found")
                return False

            # Check permission
            can_process = self._stage_permission_service.can_user_process_stage(
                user_id=user_id,
                application=application,
                company_id=company_id
            )

            return can_process

        except Exception as e:
            logger.error(f"Error checking permission for user {user_id} on application {application_id}: {e}")
            return False
