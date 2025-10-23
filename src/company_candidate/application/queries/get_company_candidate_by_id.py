from dataclasses import dataclass
from typing import Optional

from src.shared.application.query_bus import Query, QueryHandler
from src.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_candidate.application.mappers.company_candidate_mapper import CompanyCandidateMapper
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId


@dataclass(frozen=True)
class GetCompanyCandidateByIdQuery(Query):
    """Query to get a company candidate by ID"""
    id: CompanyCandidateId


class GetCompanyCandidateByIdQueryHandler(QueryHandler[GetCompanyCandidateByIdQuery, Optional[CompanyCandidateDto]]):
    """Handler for getting a company candidate by ID"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetCompanyCandidateByIdQuery) -> Optional[CompanyCandidateDto]:
        """Handle the get company candidate by ID query"""
        company_candidate = self._repository.get_by_id(query.id)

        if not company_candidate:
            return None

        return CompanyCandidateMapper.entity_to_dto(company_candidate)