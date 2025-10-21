from typing import List

from src.shared.application.query import QueryHandler
from src.company_candidate.application.queries.list_company_candidates_by_candidate import ListCompanyCandidatesByCandidateQuery
from src.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_candidate.application.mappers.company_candidate_mapper import CompanyCandidateMapper
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId


class ListCompanyCandidatesByCandidateQueryHandler(QueryHandler[ListCompanyCandidatesByCandidateQuery, List[CompanyCandidateDto]]):
    """Handler for listing all company candidates for a specific candidate"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListCompanyCandidatesByCandidateQuery) -> List[CompanyCandidateDto]:
        """Handle the list company candidates by candidate query"""
        candidate_id = CandidateId.from_string(query.candidate_id)
        company_candidates = self._repository.list_by_candidate(candidate_id)

        return [CompanyCandidateMapper.entity_to_dto(cc) for cc in company_candidates]
