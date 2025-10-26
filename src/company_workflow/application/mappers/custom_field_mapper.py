from src.company_workflow.application.dtos.custom_field_dto import CustomFieldDto
from src.company_workflow.domain.entities.custom_field import CustomField


class CustomFieldMapper:
    """Mapper for converting CustomField entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: CustomField) -> CustomFieldDto:
        """Convert entity to DTO"""
        return CustomFieldDto(
            id=str(entity.id),
            workflow_id=str(entity.workflow_id),
            field_key=entity.field_key,
            field_name=entity.field_name,
            field_type=entity.field_type.value,
            field_config=entity.field_config,
            order_index=entity.order_index,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
