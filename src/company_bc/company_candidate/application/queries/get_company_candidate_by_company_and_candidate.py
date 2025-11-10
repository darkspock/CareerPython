from dataclasses import dataclass
from typing import Optional

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.company.domain.value_objects import CompanyId
from src.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_candidate.application.mappers.company_candidate_mapper import CompanyCandidateMapper
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import \
    CompanyCandidateRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetCompanyCandidateByCompanyAndCandidateQuery(Query):
    """Query to get a company candidate by company ID and candidate ID"""
    company_id: CompanyId
    candidate_id: CandidateId


class GetCompanyCandidateByCompanyAndCandidateQueryHandler(
    QueryHandler[GetCompanyCandidateByCompanyAndCandidateQuery, Optional[CompanyCandidateDto]]):
    """Handler for getting a company candidate by company and candidate IDs"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetCompanyCandidateByCompanyAndCandidateQuery) -> Optional[CompanyCandidateDto]:
        """Handle the get company candidate by company and candidate query"""
        company_candidate = self._repository.get_by_company_and_candidate(query.company_id, query.candidate_id)

        if not company_candidate:
            return None

        return CompanyCandidateMapper.entity_to_dto(company_candidate)
