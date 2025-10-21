from dataclasses import dataclass
from typing import Optional

from src.company.application.dtos.company_user_dto import CompanyUserDto
from src.company.application.mappers.company_user_mapper import CompanyUserMapper
from src.company.domain.value_objects import CompanyId
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.user.domain.value_objects.UserId import UserId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class GetCompanyUserByCompanyAndUserQuery(Query):
    """Query to get a company user by company and user IDs"""
    company_id: str
    user_id: str


class GetCompanyUserByCompanyAndUserQueryHandler(
    QueryHandler[GetCompanyUserByCompanyAndUserQuery, Optional[CompanyUserDto]]
):
    """Handler for getting a company user by company and user - returns DTO"""

    def __init__(self, company_user_repository: CompanyUserRepositoryInterface):
        self.company_user_repository = company_user_repository

    def handle(self, query: GetCompanyUserByCompanyAndUserQuery) -> Optional[CompanyUserDto]:
        """Execute the query - returns DTO or None"""
        company_id = CompanyId.from_string(query.company_id)
        user_id = UserId(query.user_id)
        company_user = self.company_user_repository.get_by_company_and_user(
            company_id, user_id
        )

        if not company_user:
            return None

        return CompanyUserMapper.entity_to_dto(company_user)
