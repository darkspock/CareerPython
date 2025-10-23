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
    status: Optional[CompanyStatusEnum] = None
    search_term: Optional[str] = None
    limit: int = 10
    offset: int = 0


class ListCompaniesQueryHandler(QueryHandler[ListCompaniesQuery, List[CompanyDto]]):
    """Handler for listing companies - returns list of DTOs"""

    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def handle(self, query: ListCompaniesQuery) -> List[CompanyDto]:
        """Execute the query - returns list of DTOs"""
        # For now, get all and filter in memory
        # TODO: Add filtering methods to repository for better performance
        companies = self.company_repository.list_all()

        # Filter by status if provided
        if query.status:
            companies = [c for c in companies if c.status == query.status]

        # Filter by search term if provided
        if query.search_term:
            search_lower = query.search_term.lower()
            companies = [c for c in companies if
                        search_lower in c.name.lower() or
                        search_lower in c.domain.lower()]

        # Apply pagination
        start = query.offset
        end = start + query.limit
        companies = companies[start:end]

        return [CompanyMapper.entity_to_dto(company) for company in companies]
