from adapters.http.shared.customization.schemas.custom_field_response import CustomFieldResponse
from src.shared_bc.customization.entity_customization.application.dtos.custom_field_dto import CustomFieldDto


class CustomFieldResponseMapper:
    """Mapper for converting CustomField DTO to Response"""

    @staticmethod
    def dto_to_response(dto: CustomFieldDto) -> CustomFieldResponse:
        """Convert CustomField DTO to Response"""
        return CustomFieldResponse(
            id=dto.id,
            entity_customization_id=dto.entity_customization_id,
            field_key=dto.field_key,
            field_name=dto.field_name,
            field_type=dto.field_type,
            field_config=dto.field_config,
            order_index=dto.order_index,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
