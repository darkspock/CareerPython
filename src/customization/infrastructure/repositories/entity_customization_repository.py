from typing import Optional, List, Any

from src.customization.domain.entities.entity_customization import EntityCustomization
from src.customization.domain.value_objects.entity_customization_id import EntityCustomizationId
from src.customization.domain.enums.entity_customization_type_enum import EntityCustomizationTypeEnum
from src.customization.domain.interfaces.entity_customization_repository_interface import EntityCustomizationRepositoryInterface
from src.customization.infrastructure.models.entity_customization_model import EntityCustomizationModel
from src.customization.infrastructure.models.custom_field_model import CustomFieldModel
from src.customization.domain.value_objects.custom_field import CustomField
from src.customization.domain.value_objects.custom_field_id import CustomFieldId


class EntityCustomizationRepository(EntityCustomizationRepositoryInterface):
    """Repository implementation for entity customization operations"""

    def __init__(self, database: Any) -> None:
        self._database = database

    def save(self, entity_customization: EntityCustomization) -> None:
        """Save or update an entity customization"""
        model = self._to_model(entity_customization)
        with self._database.get_session() as session:
            existing = session.query(EntityCustomizationModel).filter_by(id=str(entity_customization.id)).first()
            if existing:
                # Update existing
                for key, value in model.__dict__.items():
                    if not key.startswith('_') and key != 'id':
                        setattr(existing, key, value)
                session.merge(existing)
            else:
                session.add(model)
            
            # Save/update custom fields
            # First, delete fields that are no longer in the entity
            if entity_customization.fields:
                existing_field_ids = {str(f.id) for f in entity_customization.fields}
                from sqlalchemy import not_
                session.query(CustomFieldModel).filter_by(
                    entity_customization_id=str(entity_customization.id)
                ).filter(not_(CustomFieldModel.id.in_(existing_field_ids))).delete(synchronize_session=False)
            else:
                # If no fields, delete all existing fields
                session.query(CustomFieldModel).filter_by(
                    entity_customization_id=str(entity_customization.id)
                ).delete(synchronize_session=False)
            
            # Then, save/update each field
            for field in entity_customization.fields:
                field_model = CustomFieldModel(
                    id=str(field.id),
                    entity_customization_id=str(entity_customization.id),
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
            metadata=model.metadata or {}
        )

    def _to_model(self, entity: EntityCustomization) -> EntityCustomizationModel:
        """Convert domain entity to model"""
        return EntityCustomizationModel(
            id=str(entity.id),
            entity_type=entity.entity_type.value,
            entity_id=entity.entity_id,
            validation=entity.validation,
            metadata=entity.metadata,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

