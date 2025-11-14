"""Company Role Mapper."""
from src.company_bc.company_role.application.dtos.company_role_dto import CompanyRoleDto
from src.company_bc.company_role.domain.entities.company_role import CompanyRole


class CompanyRoleMapper:
    """Mapper for converting CompanyRole entities to DTOs."""

    @staticmethod
    def entity_to_dto(entity: CompanyRole) -> CompanyRoleDto:
        """Convert entity to DTO."""
        return CompanyRoleDto(
            id=str(entity.id),
            company_id=str(entity.company_id),
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
