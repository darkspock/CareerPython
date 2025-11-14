from typing import Optional, List, Any

from src.shared_bc.customization.entity_customization.domain.entities.entity_customization import EntityCustomization
from src.shared_bc.customization.entity_customization.domain.enums.entity_customization_type_enum import \
    EntityCustomizationTypeEnum
from src.shared_bc.customization.entity_customization.domain.interfaces.entity_customization_repository_interface import \
    EntityCustomizationRepositoryInterface
from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field import CustomField
from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field_id import CustomFieldId
from src.shared_bc.customization.entity_customization.domain.value_objects.entity_customization_id import \
    EntityCustomizationId
from src.shared_bc.customization.entity_customization.infrastructure.models.custom_field_model import CustomFieldModel
from src.shared_bc.customization.entity_customization.infrastructure.models.entity_customization_model import \
    EntityCustomizationModel


class EntityCustomizationRepository(EntityCustomizationRepositoryInterface):
    """Repository implementation for entity customization operations"""

    def __init__(self, database: Any) -> None:
        self._database = database

    def save(self, entity_customization: EntityCustomization) -> None:
        """Save or update an entity customization"""
        with self._database.get_session() as session:
            # First, try to find by ID
            existing = session.query(EntityCustomizationModel).filter_by(id=str(entity_customization.id)).first()

            # If not found by ID, try to find by (entity_type, entity_id) to handle updates
            if not existing:
                existing = session.query(EntityCustomizationModel).filter_by(
                    entity_type=entity_customization.entity_type.value,
                    entity_id=entity_customization.entity_id
                ).first()

            # Use the existing ID if found, otherwise use the entity's ID
            customization_id = existing.id if existing else str(entity_customization.id)

            if existing:
                # Update existing - use the existing ID from the database
                # Update all fields
                existing.entity_type = entity_customization.entity_type.value
                existing.entity_id = entity_customization.entity_id
                existing.validation = entity_customization.validation
                existing.metadata_json = entity_customization.metadata
                existing.updated_at = entity_customization.updated_at
                # Don't update created_at - preserve original creation time
                session.merge(existing)
            else:
                # Create new
                model = self._to_model(entity_customization)
                session.add(model)

            # Save/update custom fields
            # Use the correct customization_id (existing or new)
            # First, delete fields that are no longer in the entity
            if entity_customization.fields:
                existing_field_ids = {str(f.id) for f in entity_customization.fields}
                from sqlalchemy import not_
                session.query(CustomFieldModel).filter_by(
                    entity_customization_id=customization_id
                ).filter(not_(CustomFieldModel.id.in_(existing_field_ids))).delete(synchronize_session=False)
            else:
                # If no fields, delete all existing fields
                session.query(CustomFieldModel).filter_by(
                    entity_customization_id=customization_id
                ).delete(synchronize_session=False)

            # Then, save/update each field
            for field in entity_customization.fields:
                field_model = CustomFieldModel(
                    id=str(field.id),
                    entity_customization_id=customization_id,
                    field_key=field.field_key,
                    field_name=field.field_name,
                    field_type=field.field_type,
                    field_config=field.field_config,
                    order_index=field.order_index,
                    created_at=field.created_at,
                    updated_at=field.updated_at
                )
                session.merge(field_model)

            session.commit()

    def get_by_id(self, id: EntityCustomizationId) -> Optional[EntityCustomization]:
        """Get an entity customization by ID"""
        with self._database.get_session() as session:
            model = session.query(EntityCustomizationModel).filter_by(id=str(id)).first()
            if model:
                return self._to_domain(session, model)
            return None

    def get_by_entity(
            self,
            entity_type: EntityCustomizationTypeEnum,
            entity_id: str
    ) -> Optional[EntityCustomization]:
        """Get an entity customization by entity type and entity ID"""
        with self._database.get_session() as session:
            model = session.query(EntityCustomizationModel).filter_by(
                entity_type=entity_type.value,
                entity_id=entity_id
            ).first()
            if model:
                return self._to_domain(session, model)
            return None

    def list_by_entity_type(
            self,
            entity_type: EntityCustomizationTypeEnum
    ) -> List[EntityCustomization]:
        """List all customizations for a given entity type"""
        with self._database.get_session() as session:
            models = session.query(EntityCustomizationModel).filter_by(
                entity_type=entity_type.value
            ).all()
            return [self._to_domain(session, model) for model in models]

    def delete(self, id: EntityCustomizationId) -> None:
        """Delete an entity customization"""
        with self._database.get_session() as session:
            session.query(EntityCustomizationModel).filter_by(id=str(id)).delete()
            session.commit()

    def _to_domain(self, session: Any, model: EntityCustomizationModel) -> EntityCustomization:
        """Convert model to domain entity"""
        # Load custom fields for this entity customization
        field_models = session.query(CustomFieldModel).filter_by(
            entity_customization_id=str(model.id)
        ).order_by(CustomFieldModel.order_index).all()

        fields = [
            CustomField(
                id=CustomFieldId.from_string(field_model.id),
                field_key=field_model.field_key,
                field_name=field_model.field_name,
                field_type=field_model.field_type,
                field_config=field_model.field_config,
                order_index=field_model.order_index,
                created_at=field_model.created_at,
                updated_at=field_model.updated_at
            )
            for field_model in field_models
        ]

        return EntityCustomization(
            id=EntityCustomizationId.from_string(model.id),
            entity_type=EntityCustomizationTypeEnum(model.entity_type),
            entity_id=model.entity_id,
            fields=fields,
            validation=model.validation,
            created_at=model.created_at,
            updated_at=model.updated_at,
            metadata=model.metadata_json or {}
        )

    def _to_model(self, entity: EntityCustomization) -> EntityCustomizationModel:
        """Convert domain entity to model"""
        return EntityCustomizationModel(
            id=str(entity.id),
            entity_type=entity.entity_type.value,
            entity_id=entity.entity_id,
            validation=entity.validation,
            metadata_json=entity.metadata,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
