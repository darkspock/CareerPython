from src.customization.old.application.field_configuration_dto import FieldConfigurationDto
from src.customization.old.field_configuration_response import FieldConfigurationResponse


class FieldConfigurationResponseMapper:
    """Mapper for converting FieldConfigurationDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: FieldConfigurationDto) -> FieldConfigurationResponse:
        """Convert DTO to response"""
        return FieldConfigurationResponse(
            id=dto.id,
            stage_id=dto.stage_id,
            custom_field_id=dto.custom_field_id,
            visibility=dto.visibility,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
