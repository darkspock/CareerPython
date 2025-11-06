from dataclasses import dataclass

from src.field_validation.domain.infrastructure.validation_rule_repository_interface import \
    ValidationRuleRepositoryInterface
from src.field_validation.domain.value_objects.validation_rule_id import ValidationRuleId
from src.shared.application.command_bus import Command
from src.shared.application.command_bus import CommandHandler


@dataclass(frozen=True)
class DeleteValidationRuleCommand(Command):
    """Command to delete a validation rule."""

    id: ValidationRuleId


class DeleteValidationRuleCommandHandler(CommandHandler[DeleteValidationRuleCommand]):
    """Handler for deleting validation rules."""

    def __init__(self, repository: ValidationRuleRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeleteValidationRuleCommand) -> None:
        """Execute the command."""
        self.repository.delete(command.id)
