from dataclasses import dataclass
from typing import Optional

from src.company_bc.company_candidate.domain.infrastructure.company_candidate_repository_interface import \
    CompanyCandidateRepositoryInterface
from src.company_bc.company_candidate.domain.read_models.company_candidate_with_candidate_read_model import \
    CompanyCandidateWithCandidateReadModel
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetCompanyCandidateByIdWithCandidateInfoQuery(Query):
    """Query to get a company candidate by ID with candidate info"""
    id: CompanyCandidateId


class GetCompanyCandidateByIdWithCandidateInfoQueryHandler(
    QueryHandler[GetCompanyCandidateByIdWithCandidateInfoQuery, Optional[CompanyCandidateWithCandidateReadModel]]):
    """Handler for getting a company candidate by ID with candidate info"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetCompanyCandidateByIdWithCandidateInfoQuery) -> Optional[
        CompanyCandidateWithCandidateReadModel]:
        """Handle the get company candidate by ID with candidate info query"""
        return self._repository.get_by_id_with_candidate_info(query.id)
