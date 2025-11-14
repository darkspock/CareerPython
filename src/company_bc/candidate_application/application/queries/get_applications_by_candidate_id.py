from dataclasses import dataclass
from typing import Optional, List

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.application.queries.shared.candidate_application_dto import \
    CandidateApplicationDto
from src.company_bc.candidate_application.application.queries.shared.candidate_application_dto_mapper import \
    CandidateApplicationDtoMapper
from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetApplicationsByCandidateIdQuery(Query):
    """Query para obtener todas las aplicaciones de un candidato"""
    candidate_id: str
    status_filter: Optional[str] = None
    limit: Optional[int] = None

    def get_candidate_id(self) -> CandidateId:
        """Convertir string a CandidateId value object"""
        return CandidateId.from_string(self.candidate_id)


class GetApplicationsByCandidateIdQueryHandler(
    QueryHandler[GetApplicationsByCandidateIdQuery, List[CandidateApplicationDto]]):
    """Handler para obtener aplicaciones por candidate ID"""

    def __init__(self, candidate_application_repository: CandidateApplicationRepositoryInterface):
        self._candidate_application_repository = candidate_application_repository

    def handle(self, query: GetApplicationsByCandidateIdQuery) -> List[CandidateApplicationDto]:
        """Obtiene todas las aplicaciones de un candidato"""
        # Convert status filter if provided
        status_filter = None
        if query.status_filter:
            try:
                status_filter = ApplicationStatusEnum(query.status_filter)
            except ValueError:
                pass  # Invalid status, ignore filter

        # Get applications from repository
        applications = self._candidate_application_repository.get_by_candidate_id(
            query.get_candidate_id(),
            status_filter=status_filter,
            limit=query.limit
        )

        # Convert to DTOs
        return [
            CandidateApplicationDtoMapper.from_entity(application)
            for application in applications
        ]
