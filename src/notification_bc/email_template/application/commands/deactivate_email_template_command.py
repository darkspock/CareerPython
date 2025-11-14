"""
Deactivate Email Template Command
Phase 7: Command to deactivate an email template
"""

from dataclasses import dataclass

from src.notification_bc.email_template.domain.repositories.email_template_repository_interface import EmailTemplateRepositoryInterface
from src.notification_bc.email_template.domain.value_objects.email_template_id import EmailTemplateId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeactivateEmailTemplateCommand(Command):
    """Command to deactivate an email template"""
    template_id: str


class DeactivateEmailTemplateCommandHandler(CommandHandler[DeactivateEmailTemplateCommand]):
    """Handler for DeactivateEmailTemplateCommand"""

    def __init__(self, repository: EmailTemplateRepositoryInterface):
        self._repository = repository

    def execute(self, command: DeactivateEmailTemplateCommand) -> None:
        """Execute the deactivate email template command"""
        template_id = EmailTemplateId.from_string(command.template_id)
        template = self._repository.get_by_id(template_id)

        if not template:
            raise ValueError(f"Email template not found: {command.template_id}")

            # Deactivate the template
        template.deactivate()

        # Save changes
        self._repository.save(template)
