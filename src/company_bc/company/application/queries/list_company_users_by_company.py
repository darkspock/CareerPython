from dataclasses import dataclass
from typing import List

from src.company_bc.company.application.dtos.company_user_dto import CompanyUserDto
from src.company_bc.company.application.mappers.company_user_mapper import CompanyUserMapper
from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface


@dataclass
class ListCompanyUsersByCompanyQuery(Query):
    """Query to list company users by company"""
    company_id: str
    active_only: bool = False


class ListCompanyUsersByCompanyQueryHandler(
    QueryHandler[ListCompanyUsersByCompanyQuery, List[CompanyUserDto]]
):
    """Handler for listing company users by company - returns list of DTOs"""

    def __init__(
        self, 
        company_user_repository: CompanyUserRepositoryInterface,
        user_repository: UserRepositoryInterface
    ):
        self.company_user_repository = company_user_repository
        self.user_repository = user_repository

    def handle(self, query: ListCompanyUsersByCompanyQuery) -> List[CompanyUserDto]:
        """Execute the query - returns list of DTOs"""
        company_id = CompanyId.from_string(query.company_id)

        if query.active_only:
            company_users = self.company_user_repository.list_active_by_company(company_id)
        else:
            company_users = self.company_user_repository.list_by_company(company_id)

        # Get emails and company roles for all users
        dtos = []
        for company_user in company_users:
            user = self.user_repository.get_by_id(company_user.user_id)
            email = user.email if user else None
            company_roles = self.company_user_repository.get_company_role_ids(company_user.id)
            dto = CompanyUserMapper.entity_to_dto(company_user, email, company_roles)
            dtos.append(dto)

        return dtos
