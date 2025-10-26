"""Company Role Controller."""
from typing import List, Optional

from adapters.http.company.mappers.role_response_mapper import RoleResponseMapper
from adapters.http.company.schemas.create_role_request import CreateRoleRequest
from adapters.http.company.schemas.role_response import RoleResponse
from adapters.http.company.schemas.update_role_request import UpdateRoleRequest
from src.company_role.application.commands.create_role_command import CreateRoleCommand
from src.company_role.application.commands.delete_role_command import DeleteRoleCommand
from src.company_role.application.commands.update_role_command import UpdateRoleCommand
from src.company_role.application.dtos.company_role_dto import CompanyRoleDto
from src.company_role.application.queries.get_role_by_id import GetCompanyRoleByIdQuery
from src.company_role.application.queries.list_roles_by_company import ListRolesByCompanyQuery
from src.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus


class CompanyRoleController:
    """Controller for company role operations."""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def create_role(self, company_id: str, request: CreateRoleRequest) -> RoleResponse:
        """Create a new company role."""
        id = CompanyRoleId.generate()
        command = CreateRoleCommand(
            id=id,
            company_id=company_id,
            name=request.name,
            description=request.description
        )
        self.command_bus.execute(command)

        query = GetCompanyRoleByIdQuery(id=id)
        dto: Optional[CompanyRoleDto] = self.query_bus.query(query)

        if not dto:
            raise ValueError("Failed to retrieve created role")

        return RoleResponseMapper.dto_to_response(dto)

    def get_role(self, role_id: CompanyRoleId) -> Optional[RoleResponse]:
        """Get a role by ID."""
        query = GetCompanyRoleByIdQuery(id=role_id)
        dto: Optional[CompanyRoleDto] = self.query_bus.query(query)

        if not dto:
            return None

        return RoleResponseMapper.dto_to_response(dto)

    def list_roles(self, company_id: str, active_only: bool = False) -> List[RoleResponse]:
        """List all roles for a company."""
        query = ListRolesByCompanyQuery(company_id=company_id, active_only=active_only)
        dtos: List[CompanyRoleDto] = self.query_bus.query(query)

        return [RoleResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_role(self, role_id: CompanyRoleId, request: UpdateRoleRequest) -> RoleResponse:
        """Update a company role."""
        command = UpdateRoleCommand(
            id=role_id,
            name=request.name,
            description=request.description
        )
        self.command_bus.execute(command)

        # Query the updated role
        query = GetCompanyRoleByIdQuery(id=role_id)
        dto: Optional[CompanyRoleDto] = self.query_bus.query(query)

        if not dto:
            raise ValueError("Failed to retrieve updated role")

        return RoleResponseMapper.dto_to_response(dto)

    def delete_role(self, role_id: str) -> None:
        """Delete a company role."""
        command = DeleteRoleCommand(id=role_id)
        self.command_bus.execute(command)
