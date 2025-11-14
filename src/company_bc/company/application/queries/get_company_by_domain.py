from dataclasses import dataclass
from typing import Optional

from src.company_bc.company.application.dtos.company_dto import CompanyDto
from src.company_bc.company.application.mappers.company_mapper import CompanyMapper
from src.company_bc.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetCompanyByDomainQuery(Query):
    """Query to get a company by domain"""
    domain: str


class GetCompanyByDomainQueryHandler(QueryHandler[GetCompanyByDomainQuery, Optional[CompanyDto]]):
    """Handler for getting a company by domain - returns DTO"""

    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def handle(self, query: GetCompanyByDomainQuery) -> Optional[CompanyDto]:
        """Execute the query - returns DTO or None"""
        company = self.company_repository.get_by_domain(query.domain)

        if not company:
            return None

        return CompanyMapper.entity_to_dto(company)
