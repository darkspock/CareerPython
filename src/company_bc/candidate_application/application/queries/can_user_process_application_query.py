"""Query to check if a user can process an application at its current stage"""
from dataclasses import dataclass

from src.company_bc.candidate_application.application.services.stage_permission_service import StagePermissionService
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class CanUserProcessApplicationQuery(Query):
    """Query to check if user can process an application"""
    user_id: str
    application_id: str
    company_id: str


class CanUserProcessApplicationQueryHandler(QueryHandler[CanUserProcessApplicationQuery, bool]):
    """Handler for CanUserProcessApplicationQuery"""

    def __init__(
            self,
            application_repository: CandidateApplicationRepositoryInterface,
            stage_permission_service: StagePermissionService
    ):
        self.application_repository = application_repository
        self.stage_permission_service = stage_permission_service

    def handle(self, query: CanUserProcessApplicationQuery) -> bool:
        """Check if user can process the application at its current stage"""
        try:
            # Get application
            application = self.application_repository.get_by_id(
                CandidateApplicationId(query.application_id)
            )

            if not application:
                return False

            # Check permission using the service
            return self.stage_permission_service.can_user_process_stage(
                user_id=query.user_id,
                application=application,
                company_id=query.company_id
            )

        except Exception:
            # On any error, return False for security
            return False
