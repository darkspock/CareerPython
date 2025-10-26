"""
Activate Email Template Command
Phase 7: Command to activate an email template
"""

from dataclasses import dataclass

from src.email_template.domain.value_objects.email_template_id import EmailTemplateId
from src.email_template.domain.repositories.email_template_repository_interface import EmailTemplateRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class ActivateEmailTemplateCommand(Command):
    """Command to activate an email template"""
    template_id: str


class ActivateEmailTemplateCommandHandler(CommandHandler[ActivateEmailTemplateCommand]):
    """Handler for ActivateEmailTemplateCommand"""

    def __init__(self, repository: EmailTemplateRepositoryInterface):
        self._repository = repository

    def execute(self, command: ActivateEmailTemplateCommand) -> None:
        """Execute the activate email template command"""
        template_id = EmailTemplateId.from_string(command.template_id)
        template = self._repository.get_by_id(template_id)

        if not template:
            raise ValueError(f"Email template not found: {command.template_id}")

        # Activate the template
        activated_template = template.activate()

        # Save changes
        self._repository.save(activated_template)
