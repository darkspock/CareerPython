from src.company_workflow.application.dtos.field_configuration_dto import FieldConfigurationDto
from src.company_workflow.domain.entities.field_configuration import FieldConfiguration


class FieldConfigurationMapper:
    """Mapper for converting FieldConfiguration entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: FieldConfiguration) -> FieldConfigurationDto:
        """Convert entity to DTO"""
        return FieldConfigurationDto(
            id=str(entity.id),
            stage_id=str(entity.stage_id),
            custom_field_id=str(entity.custom_field_id),
            visibility=entity.visibility.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
