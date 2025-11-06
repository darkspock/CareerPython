"""List Roles by Company Query."""
from dataclasses import dataclass
from typing import List

from src.company.domain.value_objects.company_id import CompanyId
from src.company_role.application.dtos.company_role_dto import CompanyRoleDto
from src.company_role.application.mappers.company_role_mapper import CompanyRoleMapper
from src.company_role.domain.infrastructure.company_role_repository_interface import CompanyRoleRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListRolesByCompanyQuery(Query):
    """Query to list all roles for a company."""
    company_id: str
    active_only: bool = False


class ListRolesByCompanyQueryHandler(QueryHandler[ListRolesByCompanyQuery, List[CompanyRoleDto]]):
    """Handler for listing roles by company."""

    def __init__(self, repository: CompanyRoleRepositoryInterface):
        self.repository = repository

    def handle(self, query: ListRolesByCompanyQuery) -> List[CompanyRoleDto]:
        """Handle the list roles by company query."""
        company_id = CompanyId(query.company_id)
        roles = self.repository.list_by_company(company_id, query.active_only)

        return [CompanyRoleMapper.entity_to_dto(role) for role in roles]
