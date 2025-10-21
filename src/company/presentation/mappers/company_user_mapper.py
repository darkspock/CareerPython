from src.company.application.dtos.company_user_dto import CompanyUserDto
from src.company.presentation.schemas.company_user_response import CompanyUserResponse


class CompanyUserResponseMapper:
    """Mapper for converting CompanyUserDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: CompanyUserDto) -> CompanyUserResponse:
        """Convert DTO to response"""
        return CompanyUserResponse(
            id=dto.id,
            company_id=dto.company_id,
            user_id=dto.user_id,
            role=dto.role,
            permissions=dto.permissions,
            status=dto.status,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
