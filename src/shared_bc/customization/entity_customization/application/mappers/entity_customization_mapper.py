from src.shared_bc.customization.entity_customization.domain.entities.entity_customization import EntityCustomization
from src.shared_bc.customization.entity_customization.application.dtos.entity_customization_dto import EntityCustomizationDto
from src.shared_bc.customization.entity_customization.application.mappers.custom_field_mapper import CustomFieldMapper


class EntityCustomizationMapper:
    """Mapper for converting EntityCustomization entity to DTO"""

    @staticmethod
    def entity_to_dto(entity: EntityCustomization) -> EntityCustomizationDto:
        """Convert EntityCustomization entity to DTO"""
        return EntityCustomizationDto(
            id=str(entity.id),
            entity_type=entity.entity_type.value,
            entity_id=entity.entity_id,
            fields=[CustomFieldMapper.entity_to_dto(field, str(entity.id)) for field in entity.fields],
            validation=entity.validation,
            metadata=entity.metadata,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

