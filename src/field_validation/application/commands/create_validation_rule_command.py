from dataclasses import dataclass
from typing import Optional, Any

from src.shared.application.command_bus import Command
from src.shared.application.command_bus import CommandHandler
from src.field_validation.domain.entities.validation_rule import ValidationRule
from src.field_validation.domain.value_objects.validation_rule_id import ValidationRuleId
from src.field_validation.domain.infrastructure.validation_rule_repository_interface import ValidationRuleRepositoryInterface
from src.field_validation.domain.enums.validation_rule_type import ValidationRuleType
from src.field_validation.domain.enums.comparison_operator import ComparisonOperator
from src.field_validation.domain.enums.validation_severity import ValidationSeverity
from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass(frozen=True)
class CreateValidationRuleCommand(Command):
    """Command to create a validation rule."""

    id: ValidationRuleId
    custom_field_id: CustomFieldId
    stage_id: WorkflowStageId
    rule_type: ValidationRuleType
    comparison_operator: ComparisonOperator
    severity: ValidationSeverity
    validation_message: str
    position_field_path: Optional[str] = None
    comparison_value: Optional[Any] = None
    auto_reject: bool = False
    rejection_reason: Optional[str] = None
    is_active: bool = True


class CreateValidationRuleCommandHandler(CommandHandler[CreateValidationRuleCommand]):
    """Handler for creating validation rules."""

    def __init__(self, repository: ValidationRuleRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreateValidationRuleCommand) -> None:
        """Execute the command."""
        validation_rule = ValidationRule.create(
            id=command.id,
            custom_field_id=command.custom_field_id,
            stage_id=command.stage_id,
            rule_type=command.rule_type,
            comparison_operator=command.comparison_operator,
            severity=command.severity,
            validation_message=command.validation_message,
            position_field_path=command.position_field_path,
            comparison_value=command.comparison_value,
            auto_reject=command.auto_reject,
            rejection_reason=command.rejection_reason,
            is_active=command.is_active
        )

        self.repository.save(validation_rule)
