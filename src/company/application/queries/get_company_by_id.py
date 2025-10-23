from dataclasses import dataclass
from typing import Optional

from src.company.application.dtos.company_dto import CompanyDto
from src.company.application.mappers.company_mapper import CompanyMapper
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.value_objects import CompanyId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class GetCompanyByIdQuery(Query):
    """Query to get a company by ID"""
    company_id: CompanyId


class GetCompanyByIdQueryHandler(QueryHandler[GetCompanyByIdQuery, Optional[CompanyDto]]):
    """Handler for getting a company by ID - returns DTO"""

    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def handle(self, query: GetCompanyByIdQuery) -> Optional[CompanyDto]:
        """Execute the query - returns DTO or None"""
        company_id = query.company_id
        company = self.company_repository.get_by_id(company_id)

        if not company:
            return None

        return CompanyMapper.entity_to_dto(company)
