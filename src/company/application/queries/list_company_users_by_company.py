from dataclasses import dataclass
from typing import List

from src.company.application.dtos.company_user_dto import CompanyUserDto
from src.company.application.mappers.company_user_mapper import CompanyUserMapper
from src.company.domain.value_objects import CompanyId
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class ListCompanyUsersByCompanyQuery(Query):
    """Query to list company users by company"""
    company_id: str
    active_only: bool = False


class ListCompanyUsersByCompanyQueryHandler(
    QueryHandler[ListCompanyUsersByCompanyQuery, List[CompanyUserDto]]
):
    """Handler for listing company users by company - returns list of DTOs"""

    def __init__(self, company_user_repository: CompanyUserRepositoryInterface):
        self.company_user_repository = company_user_repository

    def handle(self, query: ListCompanyUsersByCompanyQuery) -> List[CompanyUserDto]:
        """Execute the query - returns list of DTOs"""
        company_id = CompanyId.from_string(query.company_id)

        if query.active_only:
            company_users = self.company_user_repository.list_active_by_company(company_id)
        else:
            company_users = self.company_user_repository.list_by_company(company_id)

        return [CompanyUserMapper.entity_to_dto(user) for user in company_users]
