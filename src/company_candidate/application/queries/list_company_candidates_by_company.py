from dataclasses import dataclass
from typing import List

from src.company.domain.value_objects.company_id import CompanyId
from src.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_candidate.application.mappers.company_candidate_mapper import CompanyCandidateMapper
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import \
    CompanyCandidateRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListCompanyCandidatesByCompanyQuery(Query):
    """Query to list all company candidates for a specific company"""
    company_id: CompanyId


class ListCompanyCandidatesByCompanyQueryHandler(
    QueryHandler[ListCompanyCandidatesByCompanyQuery, List[CompanyCandidateDto]]):
    """Handler for listing all company candidates for a specific company"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListCompanyCandidatesByCompanyQuery) -> List[CompanyCandidateDto]:
        """Handle the list company candidates by company query"""
        company_candidates = self._repository.list_by_company(query.company_id)

        return [CompanyCandidateMapper.entity_to_dto(cc) for cc in company_candidates]
