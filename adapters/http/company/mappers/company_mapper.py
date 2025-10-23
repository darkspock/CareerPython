from src.company.application.dtos.company_dto import CompanyDto
from adapters.http.company.schemas.company_response import CompanyResponse


class CompanyResponseMapper:
    """Mapper for converting CompanyDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: CompanyDto) -> CompanyResponse:
        """Convert DTO to response"""
        return CompanyResponse(
            id=dto.id,
            name=dto.name,
            domain=dto.domain,
            logo_url=dto.logo_url,
            settings=dto.settings,
            status=dto.status,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
