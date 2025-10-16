from dataclasses import dataclass
from typing import Optional, List

from src.company.domain.entities.company import Company
from src.company.domain.enums import CompanyStatusEnum
from src.company.infrastructure.repositories.company_repository import CompanyRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class ListCompaniesQuery(Query):
    status: Optional[CompanyStatusEnum] = None
    sector: Optional[str] = None
    location: Optional[str] = None
    search_term: Optional[str] = None
    limit: int = 50
    offset: int = 0


class ListCompaniesQueryHandler(QueryHandler[ListCompaniesQuery, List[Company]]):
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def handle(self, query: ListCompaniesQuery) -> List[Company]:
        return self.company_repository.find_by_filters(
            status=query.status,
            sector=query.sector,
            location=query.location,
            search_term=query.search_term,
            limit=query.limit,
            offset=query.offset
        )
