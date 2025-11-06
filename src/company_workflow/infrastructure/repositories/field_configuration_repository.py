from typing import Optional, List, Any

from src.company_workflow.domain.entities.field_configuration import FieldConfiguration
from src.company_workflow.domain.enums.field_visibility import FieldVisibility
from src.company_workflow.domain.infrastructure.field_configuration_repository_interface import \
    FieldConfigurationRepositoryInterface
from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.company_workflow.domain.value_objects.field_configuration_id import FieldConfigurationId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.infrastructure.models.field_configuration_model import FieldConfigurationModel


class FieldConfigurationRepository(FieldConfigurationRepositoryInterface):
    """Repository implementation for field configuration operations"""

    def __init__(self, database: Any) -> None:
        self._database = database

    def save(self, field_configuration: FieldConfiguration) -> None:
        """Save a field configuration"""
        model = self._to_model(field_configuration)
        with self._database.get_session() as session:
            existing = session.query(FieldConfigurationModel).filter_by(id=str(field_configuration.id)).first()
            if existing:
                session.merge(model)
            else:
                session.add(model)
            session.commit()

    def get_by_id(self, field_configuration_id: FieldConfigurationId) -> Optional[FieldConfiguration]:
        """Get field configuration by ID"""
        with self._database.get_session() as session:
            model = session.query(FieldConfigurationModel).filter_by(id=str(field_configuration_id)).first()
            if model:
                return self._to_domain(model)
            return None

    def list_by_stage(self, stage_id: WorkflowStageId) -> List[FieldConfiguration]:
        """List all field configurations for a stage"""
        with self._database.get_session() as session:
            models = session.query(FieldConfigurationModel).filter_by(stage_id=str(stage_id)).all()
            return [self._to_domain(model) for model in models]

    def get_by_stage_and_field(self, stage_id: WorkflowStageId, custom_field_id: CustomFieldId) -> Optional[
        FieldConfiguration]:
        """Get a field configuration by stage ID and custom field ID"""
        with self._database.get_session() as session:
            model = session.query(FieldConfigurationModel).filter_by(
                stage_id=str(stage_id),
                custom_field_id=str(custom_field_id)
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def delete(self, field_configuration_id: FieldConfigurationId) -> None:
        """Delete a field configuration"""
        with self._database.get_session() as session:
            session.query(FieldConfigurationModel).filter_by(id=str(field_configuration_id)).delete()
            session.commit()

    def delete_by_stage(self, stage_id: WorkflowStageId) -> None:
        """Delete all field configurations for a stage"""
        with self._database.get_session() as session:
            session.query(FieldConfigurationModel).filter_by(stage_id=str(stage_id)).delete()
            session.commit()

    def _to_domain(self, model: FieldConfigurationModel) -> FieldConfiguration:
        """Convert model to domain entity"""
        return FieldConfiguration(
            id=FieldConfigurationId.from_string(model.id),
            stage_id=WorkflowStageId.from_string(model.stage_id),
            custom_field_id=CustomFieldId.from_string(model.custom_field_id),
            visibility=FieldVisibility(model.visibility),
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: FieldConfiguration) -> FieldConfigurationModel:
        """Convert domain entity to model"""
        return FieldConfigurationModel(
            id=str(entity.id),
            stage_id=str(entity.stage_id),
            custom_field_id=str(entity.custom_field_id),
            visibility=entity.visibility.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
