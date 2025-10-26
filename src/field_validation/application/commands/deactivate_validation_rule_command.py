from dataclasses import dataclass

from src.shared.application.command_bus import Command
from src.shared.application.command_bus import CommandHandler
from src.field_validation.domain.value_objects.validation_rule_id import ValidationRuleId
from src.field_validation.domain.infrastructure.validation_rule_repository_interface import ValidationRuleRepositoryInterface


@dataclass(frozen=True)
class DeactivateValidationRuleCommand(Command):
    """Command to deactivate a validation rule."""

    id: ValidationRuleId


class DeactivateValidationRuleCommandHandler(CommandHandler[DeactivateValidationRuleCommand]):
    """Handler for deactivating validation rules."""

    def __init__(self, repository: ValidationRuleRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeactivateValidationRuleCommand) -> None:
        """Execute the command."""
        validation_rule = self.repository.get_by_id(command.id)
        if not validation_rule:
            raise ValueError(f"Validation rule {command.id} not found")

        deactivated_rule = validation_rule.deactivate()
        self.repository.save(deactivated_rule)
