"""
Talent Pool Mapper
Phase 8: Mapper for converting DTOs to response schemas
"""

from src.company_bc.talent_pool.application.dtos.talent_pool_entry_dto import TalentPoolEntryDto
from adapters.http.company_app.talent_pool.schemas.talent_pool_schemas import TalentPoolEntryResponse


class TalentPoolMapper:
    """Mapper for talent pool DTOs to response schemas"""

    @staticmethod
    def dto_to_response(dto: TalentPoolEntryDto) -> TalentPoolEntryResponse:
        """
        Convert TalentPoolEntryDto to TalentPoolEntryResponse.

        Args:
            dto: The DTO to convert

        Returns:
            Response schema
        """
        return TalentPoolEntryResponse(
            id=dto.id,
            company_id=dto.company_id,
            candidate_id=dto.candidate_id,
            source_application_id=dto.source_application_id,
            source_position_id=dto.source_position_id,
            added_reason=dto.added_reason,
            tags=dto.tags,
            rating=dto.rating,
            notes=dto.notes,
            status=dto.status,
            added_by_user_id=dto.added_by_user_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
