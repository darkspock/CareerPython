from dataclasses import dataclass
from typing import Optional

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.application.queries.shared.candidate_application_dto import \
    CandidateApplicationDto
from src.company_bc.candidate_application.application.queries.shared.candidate_application_dto_mapper import \
    CandidateApplicationDtoMapper
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetApplicationByCandidateAndPositionQuery(Query):
    """Query para obtener aplicación por candidato y posición"""
    candidate_id: str
    job_position_id: str

    def get_candidate_id(self) -> CandidateId:
        """Convertir string a CandidateId value object"""
        return CandidateId(self.candidate_id)

    def get_job_position_id(self) -> JobPositionId:
        """Convertir string a JobPositionId value object"""
        return JobPositionId(self.job_position_id)


class GetApplicationByCandidateAndPositionQueryHandler(
    QueryHandler[GetApplicationByCandidateAndPositionQuery, Optional[CandidateApplicationDto]]):
    """Handler para obtener aplicación por candidato y posición"""

    def __init__(self, candidate_application_repository: CandidateApplicationRepositoryInterface):
        self.candidate_application_repository = candidate_application_repository

    def handle(self, query: GetApplicationByCandidateAndPositionQuery) -> Optional[CandidateApplicationDto]:
        """Ejecutar query para obtener aplicación"""
        application = self.candidate_application_repository.get_by_candidate_and_position(
            query.get_candidate_id(),
            query.get_job_position_id()
        )

        if application:
            return CandidateApplicationDtoMapper.from_entity(application)
        return None
