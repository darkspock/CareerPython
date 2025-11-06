from src.customization.application.custom_field_dto import CustomFieldDto
from src.workflow.presentation.schemas.custom_field_response import CustomFieldResponse


class CustomFieldResponseMapper:
    """Mapper for converting CustomFieldDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: CustomFieldDto) -> CustomFieldResponse:
        """Convert DTO to response"""
        return CustomFieldResponse(
            id=dto.id,
            workflow_id=dto.workflow_id,
            field_key=dto.field_key,
            field_name=dto.field_name,
            field_type=dto.field_type,
            field_config=dto.field_config,
            order_index=dto.order_index,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
