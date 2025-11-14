from typing import Optional, List

from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field_id import CustomFieldId
from src.shared_bc.customization.field_validation.domain.entities.validation_rule import ValidationRule
from src.shared_bc.customization.field_validation.domain.value_objects.validation_rule_id import ValidationRuleId
from src.shared_bc.customization.field_validation.domain.infrastructure.validation_rule_repository_interface import ValidationRuleRepositoryInterface
from src.shared_bc.customization.field_validation.domain.enums.validation_rule_type import ValidationRuleType
from src.shared_bc.customization.field_validation.domain.enums.comparison_operator import ComparisonOperator
from src.shared_bc.customization.field_validation.domain.enums.validation_severity import ValidationSeverity
from src.shared_bc.customization.field_validation.infrastructure.models.validation_rule_model import ValidationRuleModel
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from core.database import database


class ValidationRuleRepository(ValidationRuleRepositoryInterface):
    """Repository implementation for validation rules."""

    def __init__(self) -> None:
        self._database = database

    def save(self, validation_rule: ValidationRule) -> None:
        """Save a validation rule."""
        with self._database.get_session() as session:
            model = self._to_model(validation_rule)
            session.merge(model)
            session.commit()

    def get_by_id(self, rule_id: ValidationRuleId) -> Optional[ValidationRule]:
        """Get validation rule by ID."""
        with self._database.get_session() as session:
            model = session.query(ValidationRuleModel).filter_by(id=str(rule_id)).first()
            return self._to_domain(model) if model else None

    def list_by_stage(self, stage_id: WorkflowStageId, active_only: bool = False) -> List[ValidationRule]:
        """List all validation rules for a stage, ordered by creation date."""
        with self._database.get_session() as session:
            query = session.query(ValidationRuleModel).filter_by(stage_id=str(stage_id))

            if active_only:
                query = query.filter_by(is_active=True)

            models = query.order_by(ValidationRuleModel.created_at).all()
            return [self._to_domain(model) for model in models]

    def list_by_custom_field(self, field_id: CustomFieldId, active_only: bool = False) -> List[ValidationRule]:
        """List all validation rules for a custom field."""
        with self._database.get_session() as session:
            query = session.query(ValidationRuleModel).filter_by(custom_field_id=str(field_id))

            if active_only:
                query = query.filter_by(is_active=True)

            models = query.order_by(ValidationRuleModel.created_at).all()
            return [self._to_domain(model) for model in models]

    def delete(self, rule_id: ValidationRuleId) -> None:
        """Delete a validation rule."""
        with self._database.get_session() as session:
            model = session.query(ValidationRuleModel).filter_by(id=str(rule_id)).first()
            if model:
                session.delete(model)
                session.commit()

    def _to_domain(self, model: ValidationRuleModel) -> ValidationRule:
        """Convert model to domain entity."""
        return ValidationRule(
            id=ValidationRuleId.from_string(model.id),
            custom_field_id=CustomFieldId.from_string(model.custom_field_id),
            stage_id=WorkflowStageId.from_string(model.stage_id),
            rule_type=ValidationRuleType(model.rule_type),
            comparison_operator=ComparisonOperator(model.comparison_operator),
            position_field_path=model.position_field_path,
            comparison_value=model.comparison_value,
            severity=ValidationSeverity(model.severity),
            validation_message=model.validation_message,
            auto_reject=model.auto_reject,
            rejection_reason=model.rejection_reason,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: ValidationRule) -> ValidationRuleModel:
        """Convert domain entity to model."""
        return ValidationRuleModel(
            id=str(entity.id),
            custom_field_id=str(entity.custom_field_id),
            stage_id=str(entity.stage_id),
            rule_type=entity.rule_type.value,
            comparison_operator=entity.comparison_operator.value,
            position_field_path=entity.position_field_path,
            comparison_value=entity.comparison_value,
            severity=entity.severity.value,
            validation_message=entity.validation_message,
            auto_reject=entity.auto_reject,
            rejection_reason=entity.rejection_reason,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
