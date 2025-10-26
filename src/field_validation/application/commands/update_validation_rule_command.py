from dataclasses import dataclass
from typing import Optional, Any

from src.shared.application.command_bus import Command
from src.shared.application.command_bus import CommandHandler
from src.field_validation.domain.value_objects.validation_rule_id import ValidationRuleId
from src.field_validation.domain.infrastructure.validation_rule_repository_interface import ValidationRuleRepositoryInterface
from src.field_validation.domain.enums.comparison_operator import ComparisonOperator
from src.field_validation.domain.enums.validation_severity import ValidationSeverity


@dataclass(frozen=True)
class UpdateValidationRuleCommand(Command):
    """Command to update a validation rule."""

    id: ValidationRuleId
    comparison_operator: ComparisonOperator
    severity: ValidationSeverity
    validation_message: str
    position_field_path: Optional[str] = None
    comparison_value: Optional[Any] = None
    auto_reject: bool = False
    rejection_reason: Optional[str] = None
    is_active: bool = True


class UpdateValidationRuleCommandHandler(CommandHandler[UpdateValidationRuleCommand]):
    """Handler for updating validation rules."""

    def __init__(self, repository: ValidationRuleRepositoryInterface):
        self.repository = repository

    def execute(self, command: UpdateValidationRuleCommand) -> None:
        """Execute the command."""
        validation_rule = self.repository.get_by_id(command.id)
        if not validation_rule:
            raise ValueError(f"Validation rule {command.id} not found")

        updated_rule = validation_rule.update(
            comparison_operator=command.comparison_operator,
            severity=command.severity,
            validation_message=command.validation_message,
            position_field_path=command.position_field_path,
            comparison_value=command.comparison_value,
            auto_reject=command.auto_reject,
            rejection_reason=command.rejection_reason,
            is_active=command.is_active
        )

        self.repository.save(updated_rule)
