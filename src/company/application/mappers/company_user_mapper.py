from src.company.application.dtos.company_user_dto import CompanyUserDto
from src.company.domain.entities.company_user import CompanyUser


class CompanyUserMapper:
    """Mapper for converting CompanyUser entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: CompanyUser) -> CompanyUserDto:
        """Convert entity to DTO"""
        return CompanyUserDto(
            id=str(entity.id),
            company_id=str(entity.company_id),
            user_id=str(entity.user_id),
            role=entity.role.value,
            permissions=entity.permissions.to_dict(),
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
