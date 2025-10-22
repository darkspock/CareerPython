from dataclasses import dataclass
from typing import Optional, List

from src.company.application.dtos.company_dto import CompanyDto
from src.company.application.mappers.company_mapper import CompanyMapper
from src.company.domain.enums import CompanyStatusEnum
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class ListCompaniesQuery(Query):
    """Query to list companies"""
    active_only: bool = False


class ListCompaniesQueryHandler(QueryHandler[ListCompaniesQuery, List[CompanyDto]]):
    """Handler for listing companies - returns list of DTOs"""

    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def handle(self, query: ListCompaniesQuery) -> List[CompanyDto]:
        """Execute the query - returns list of DTOs"""
        if query.active_only:
            companies = self.company_repository.list_active()
        else:
            companies = self.company_repository.list_all()

        return [CompanyMapper.entity_to_dto(company) for company in companies]
