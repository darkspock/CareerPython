"""Company role application module - exports queries and commands"""

# Commands
from .commands.create_role_command import CreateRoleCommand, CreateRoleCommandHandler
from .commands.delete_role_command import DeleteRoleCommand, DeleteRoleCommandHandler
from .commands.update_role_command import UpdateRoleCommand, UpdateRoleCommandHandler
# Queries
from .queries.get_role_by_id import GetCompanyRoleByIdQuery, GetCompanyRoleByIdQueryHandler
from .queries.list_roles_by_company import (
    ListRolesByCompanyQuery,
    ListRolesByCompanyQueryHandler,
)

__all__ = [
    # Queries
    "GetCompanyRoleByIdQuery",
    "GetCompanyRoleByIdQueryHandler",
    "ListRolesByCompanyQuery",
    "ListRolesByCompanyQueryHandler",
    # Commands
    "CreateRoleCommand",
    "CreateRoleCommandHandler",
    "DeleteRoleCommand",
    "DeleteRoleCommandHandler",
    "UpdateRoleCommand",
    "UpdateRoleCommandHandler",
]
