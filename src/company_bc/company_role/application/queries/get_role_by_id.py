"""Get Role by ID Query."""
from dataclasses import dataclass
from typing import Optional

from src.company_bc.company_role.application.dtos.company_role_dto import CompanyRoleDto
from src.company_bc.company_role.application.mappers.company_role_mapper import CompanyRoleMapper
from src.company_bc.company_role.domain.infrastructure.company_role_repository_interface import \
    CompanyRoleRepositoryInterface
from src.company_bc.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetCompanyRoleByIdQuery(Query):
    """Query to get a role by ID."""
    id: CompanyRoleId


class GetCompanyRoleByIdQueryHandler(QueryHandler[GetCompanyRoleByIdQuery, Optional[CompanyRoleDto]]):
    """Handler for getting a role by ID."""

    def __init__(self, repository: CompanyRoleRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetCompanyRoleByIdQuery) -> Optional[CompanyRoleDto]:
        """Handle the get role by ID query."""
        role_id = query.id
        role = self.repository.get_by_id(role_id)

        if not role:
            return None

        return CompanyRoleMapper.entity_to_dto(role)
