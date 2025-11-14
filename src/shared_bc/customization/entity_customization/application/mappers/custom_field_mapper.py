from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field import CustomField
from src.shared_bc.customization.entity_customization.application.dtos.custom_field_dto import CustomFieldDto


class CustomFieldMapper:
    """Mapper for converting CustomField value object to DTO"""

    @staticmethod
    def entity_to_dto(field: CustomField, entity_customization_id: str) -> CustomFieldDto:
        """Convert CustomField value object to DTO"""
        return CustomFieldDto(
            id=str(field.id),
            entity_customization_id=entity_customization_id,
            field_key=field.field_key,
            field_name=field.field_name,
            field_type=field.field_type,
            field_config=field.field_config,
            order_index=field.order_index,
            created_at=field.created_at,
            updated_at=field.updated_at
        )

