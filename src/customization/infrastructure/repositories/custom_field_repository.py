from typing import Optional, List, Any

from src.workflow.domain.entities.custom_field import CustomField
from src.workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.infrastructure.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.workflow.infrastructure.models.custom_field_model import CustomFieldModel
from src.workflow.domain.enums.field_type import FieldType


class CustomFieldRepository(CustomFieldRepositoryInterface):
    """Repository implementation for custom field operations"""

    def __init__(self, database: Any) -> None:
        self._database = database

    def save(self, custom_field: CustomField) -> None:
        """Save a custom field"""
        model = self._to_model(custom_field)
        with self._database.get_session() as session:
            existing = session.query(CustomFieldModel).filter_by(id=str(custom_field.id)).first()
            if existing:
                session.merge(model)
            else:
                session.add(model)
            session.commit()

    def get_by_id(self, custom_field_id: CustomFieldId) -> Optional[CustomField]:
        """Get custom field by ID"""
        with self._database.get_session() as session:
            model = session.query(CustomFieldModel).filter_by(id=str(custom_field_id)).first()
            if model:
                return self._to_domain(model)
            return None

    def list_by_workflow(self, workflow_id: WorkflowId) -> List[CustomField]:
        """List all custom fields for a workflow, ordered by order_index"""
        with self._database.get_session() as session:
            models = session.query(CustomFieldModel).filter_by(
                workflow_id=str(workflow_id)
            ).order_by(CustomFieldModel.order_index).all()
            return [self._to_domain(model) for model in models]

    def get_by_workflow_and_key(self, workflow_id: WorkflowId, field_key: str) -> Optional[CustomField]:
        """Get a custom field by workflow ID and field key"""
        with self._database.get_session() as session:
            model = session.query(CustomFieldModel).filter_by(
                workflow_id=str(workflow_id),
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
            workflow_id=WorkflowId.from_string(model.workflow_id),
            field_key=model.field_key,
            field_name=model.field_name,
            field_type=FieldType(model.field_type),
            field_config=model.field_config,
            order_index=model.order_index,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: CustomField) -> CustomFieldModel:
        """Convert domain entity to model"""
        return CustomFieldModel(
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
