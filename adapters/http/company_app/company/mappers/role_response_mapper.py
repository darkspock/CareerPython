"""Role Response Mapper."""
from adapters.http.company_app.company.schemas.role_response import RoleResponse
from src.company_bc.company_role.application.dtos.company_role_dto import CompanyRoleDto


class RoleResponseMapper:
    """Mapper for converting CompanyRoleDto to RoleResponse."""

    @staticmethod
    def dto_to_response(dto: CompanyRoleDto) -> RoleResponse:
        """Convert CompanyRoleDto to RoleResponse schema."""
        return RoleResponse(
            id=str(dto.id),
            company_id=str(dto.company_id),
            name=dto.name,
            description=dto.description,
            is_active=dto.is_active,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
