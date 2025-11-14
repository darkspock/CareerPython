from src.company_bc.company.application.dtos.company_user_dto import CompanyUserDto
from src.company_bc.company.domain.entities.company_user import CompanyUser


class CompanyUserMapper:
    """Mapper for converting CompanyUser entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: CompanyUser, email: str | None = None,
                      company_roles: list[str] | None = None) -> CompanyUserDto:
        """Convert entity to DTO"""
        return CompanyUserDto(
            id=str(entity.id),
            company_id=str(entity.company_id),
            user_id=str(entity.user_id),
            email=email,
            role=entity.role.value,
            permissions=entity.permissions.to_dict(),
            status=entity.status.value,
            company_roles=company_roles or [],
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
