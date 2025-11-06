from dataclasses import dataclass

from src.field_validation.domain.infrastructure.validation_rule_repository_interface import \
    ValidationRuleRepositoryInterface
from src.field_validation.domain.value_objects.validation_rule_id import ValidationRuleId
from src.shared.application.command_bus import Command
from src.shared.application.command_bus import CommandHandler


@dataclass(frozen=True)
class ActivateValidationRuleCommand(Command):
    """Command to activate a validation rule."""

    id: ValidationRuleId


class ActivateValidationRuleCommandHandler(CommandHandler[ActivateValidationRuleCommand]):
    """Handler for activating validation rules."""

    def __init__(self, repository: ValidationRuleRepositoryInterface):
        self.repository = repository

    def execute(self, command: ActivateValidationRuleCommand) -> None:
        """Execute the command."""
        validation_rule = self.repository.get_by_id(command.id)
        if not validation_rule:
            raise ValueError(f"Validation rule {command.id} not found")

        activated_rule = validation_rule.activate()
        self.repository.save(activated_rule)
