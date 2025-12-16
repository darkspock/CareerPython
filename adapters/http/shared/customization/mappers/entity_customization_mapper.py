from adapters.http.shared.customization.mappers.custom_field_mapper import CustomFieldResponseMapper
from adapters.http.shared.customization.schemas.entity_customization_response import EntityCustomizationResponse
from src.shared_bc.customization.entity_customization.application.dtos.entity_customization_dto import \
    EntityCustomizationDto


class EntityCustomizationResponseMapper:
    """Mapper for converting EntityCustomization DTO to Response"""

    @staticmethod
    def dto_to_response(dto: EntityCustomizationDto) -> EntityCustomizationResponse:
        """Convert EntityCustomization DTO to Response"""
        return EntityCustomizationResponse(
            id=dto.id,
            entity_type=dto.entity_type,
            entity_id=dto.entity_id,
            fields=[CustomFieldResponseMapper.dto_to_response(field_dto) for field_dto in dto.fields],
            validation=dto.validation,
            metadata=dto.metadata,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            exists=True
        )
