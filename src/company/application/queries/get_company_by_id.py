from dataclasses import dataclass
from typing import Optional

from src.company.domain.entities.company import Company
from src.company.infrastructure.repositories.company_repository import CompanyRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class GetCompanyByIdQuery(Query):
    company_id: str


class GetCompanyByIdQueryHandler(QueryHandler[GetCompanyByIdQuery, Optional[Company]]):
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def handle(self, query: GetCompanyByIdQuery) -> Optional[Company]:
        return self.company_repository.get_by_id(query.company_id)
