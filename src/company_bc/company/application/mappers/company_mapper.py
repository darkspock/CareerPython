from src.company_bc.company.application.dtos.company_dto import CompanyDto
from src.company_bc.company.domain.entities.company import Company


class CompanyMapper:
    """Mapper for converting Company entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: Company) -> CompanyDto:
        """Convert entity to DTO"""
        return CompanyDto(
            id=str(entity.id),
            name=entity.name,
            domain=entity.domain,
            slug=entity.slug,
            logo_url=entity.logo_url,
            settings=entity.settings.to_dict(),
            status=entity.status.value if hasattr(entity.status, 'value') else entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            company_type=entity.company_type,
        )
