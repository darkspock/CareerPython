from typing import Optional

from src.shared.application.query import QueryHandler
from src.company_candidate.application.queries.get_company_candidate_by_company_and_candidate import GetCompanyCandidateByCompanyAndCandidateQuery
from src.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_candidate.application.mappers.company_candidate_mapper import CompanyCandidateMapper
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company.domain.value_objects.company_id import CompanyId
from src.candidate.domain.value_objects.candidate_id import CandidateId


class GetCompanyCandidateByCompanyAndCandidateQueryHandler(QueryHandler[GetCompanyCandidateByCompanyAndCandidateQuery, Optional[CompanyCandidateDto]]):
    """Handler for getting a company candidate by company and candidate IDs"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetCompanyCandidateByCompanyAndCandidateQuery) -> Optional[CompanyCandidateDto]:
        """Handle the get company candidate by company and candidate query"""
        company_id = CompanyId.from_string(query.company_id)
        candidate_id = CandidateId.from_string(query.candidate_id)

        company_candidate = self._repository.get_by_company_and_candidate(company_id, candidate_id)

        if not company_candidate:
            return None

        return CompanyCandidateMapper.entity_to_dto(company_candidate)
