from dataclasses import dataclass
from typing import Optional

from src.company.application.dtos.company_user_dto import CompanyUserDto
from src.company.application.mappers.company_user_mapper import CompanyUserMapper
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company.domain.value_objects import CompanyUserId
from src.shared.application.query_bus import Query, QueryHandler
from src.user.domain.repositories.user_repository_interface import UserRepositoryInterface


@dataclass
class GetCompanyUserByIdQuery(Query):
    """Query to get a company user by ID"""
    company_user_id: str


class GetCompanyUserByIdQueryHandler(QueryHandler[GetCompanyUserByIdQuery, Optional[CompanyUserDto]]):
    """Handler for getting a company user by ID - returns DTO"""

    def __init__(
            self,
            company_user_repository: CompanyUserRepositoryInterface,
            user_repository: UserRepositoryInterface
    ):
        self.company_user_repository = company_user_repository
        self.user_repository = user_repository

    def handle(self, query: GetCompanyUserByIdQuery) -> Optional[CompanyUserDto]:
        """Execute the query - returns DTO or None"""
        company_user_id = CompanyUserId.from_string(query.company_user_id)
        company_user = self.company_user_repository.get_by_id(company_user_id)

        if not company_user:
            return None

        # Get email and company roles
        user = self.user_repository.get_by_id(company_user.user_id)
        email = user.email if user else None
        company_roles = self.company_user_repository.get_company_role_ids(company_user.id)

        return CompanyUserMapper.entity_to_dto(company_user, email, company_roles)
