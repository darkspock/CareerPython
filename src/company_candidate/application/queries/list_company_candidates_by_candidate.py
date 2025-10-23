from dataclasses import dataclass
from typing import List

from src.shared.application.query_bus import Query, QueryHandler
from src.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_candidate.application.mappers.company_candidate_mapper import CompanyCandidateMapper
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId


@dataclass(frozen=True)
class ListCompanyCandidatesByCandidateQuery(Query):
    """Query to list all company candidates for a specific candidate"""
    candidate_id: CandidateId


class ListCompanyCandidatesByCandidateQueryHandler(QueryHandler[ListCompanyCandidatesByCandidateQuery, List[CompanyCandidateDto]]):
    """Handler for listing all company candidates for a specific candidate"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListCompanyCandidatesByCandidateQuery) -> List[CompanyCandidateDto]:
        """Handle the list company candidates by candidate query"""
        company_candidates = self._repository.list_by_candidate(query.candidate_id)

        return [CompanyCandidateMapper.entity_to_dto(cc) for cc in company_candidates]