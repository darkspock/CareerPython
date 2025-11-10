from dataclasses import dataclass
from typing import List

from src.company_candidate.domain.read_models.company_candidate_with_candidate_read_model import (
    CompanyCandidateWithCandidateReadModel
)
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import (
    CompanyCandidateRepositoryInterface
)
from src.company_bc.company.domain.value_objects import CompanyId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListCompanyCandidatesWithCandidateInfoQuery(Query):
    """Query to list all company candidates with candidate basic info"""
    company_id: str


class ListCompanyCandidatesWithCandidateInfoQueryHandler(
    QueryHandler[ListCompanyCandidatesWithCandidateInfoQuery, List[CompanyCandidateWithCandidateReadModel]]
):
    """Handler for listing company candidates with candidate info"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListCompanyCandidatesWithCandidateInfoQuery) -> List[CompanyCandidateWithCandidateReadModel]:
        """Handle the query using read model from repository"""
        company_id = CompanyId.from_string(query.company_id)
        return self._repository.list_by_company_with_candidate_info(company_id)
