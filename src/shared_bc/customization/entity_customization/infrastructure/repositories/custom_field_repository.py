from typing import Optional, List, Any

from src.shared_bc.customization.entity_customization.domain.interfaces.custom_field_repository_interface import \
    CustomFieldRepositoryInterface
from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field import CustomField
from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field_id import CustomFieldId
from src.shared_bc.customization.entity_customization.domain.value_objects.entity_customization_id import \
    EntityCustomizationId
from src.shared_bc.customization.entity_customization.infrastructure.models.custom_field_model import CustomFieldModel


class CustomFieldRepository(CustomFieldRepositoryInterface):
    """Repository implementation for custom field operations"""

    def __init__(self, database: Any) -> None:
        self._database = database

    def save(self, custom_field: CustomField, entity_customization_id: EntityCustomizationId) -> None:
        """Save or update a custom field"""
        model = self._to_model(custom_field, entity_customization_id)
        with self._database.get_session() as session:
            existing = session.query(CustomFieldModel).filter_by(id=str(custom_field.id)).first()
            if existing:
                session.merge(model)
            else:
                session.add(model)
            session.commit()

    def get_by_id(self, custom_field_id: CustomFieldId) -> Optional[CustomField]:
        """Get a custom field by ID"""
        with self._database.get_session() as session:
            model = session.query(CustomFieldModel).filter_by(id=str(custom_field_id)).first()
            if model:
                return self._to_domain(model)
            return None

    def list_by_entity_customization(
            self,
            entity_customization_id: EntityCustomizationId
    ) -> List[CustomField]:
        """List all custom fields for an entity customization, ordered by order_index"""
        with self._database.get_session() as session:
            models = session.query(CustomFieldModel).filter_by(
                entity_customization_id=str(entity_customization_id)
            ).order_by(CustomFieldModel.order_index).all()
            return [self._to_domain(model) for model in models]

    def get_by_entity_customization_and_key(
            self,
            entity_customization_id: EntityCustomizationId,
            field_key: str
    ) -> Optional[CustomField]:
        """Get a custom field by entity customization ID and field key"""
        with self._database.get_session() as session:
            model = session.query(CustomFieldModel).filter_by(
                entity_customization_id=str(entity_customization_id),
                field_key=field_key
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def delete(self, custom_field_id: CustomFieldId) -> None:
        """Delete a custom field"""
        with self._database.get_session() as session:
            session.query(CustomFieldModel).filter_by(id=str(custom_field_id)).delete()
            session.commit()

    def _to_domain(self, model: CustomFieldModel) -> CustomField:
        """Convert model to domain entity"""
        return CustomField(
            id=CustomFieldId.from_string(model.id),
            field_key=model.field_key,
            field_name=model.field_name,
            field_type=model.field_type,
            field_config=model.field_config,
            order_index=model.order_index,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: CustomField, entity_customization_id: EntityCustomizationId) -> CustomFieldModel:
        """Convert domain entity to model"""
        return CustomFieldModel(
            id=str(entity.id),
            entity_customization_id=str(entity_customization_id),
            field_key=entity.field_key,
            field_name=entity.field_name,
            field_type=entity.field_type,
            field_config=entity.field_config,
            order_index=entity.order_index,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
