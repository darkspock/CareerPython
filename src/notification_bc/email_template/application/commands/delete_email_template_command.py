"""
Delete Email Template Command
Phase 7: Command to delete an email template
"""

from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.notification_bc.email_template.domain.repositories.email_template_repository_interface import \
    EmailTemplateRepositoryInterface
from src.notification_bc.email_template.domain.value_objects.email_template_id import EmailTemplateId


@dataclass(frozen=True)
class DeleteEmailTemplateCommand(Command):
    """Command to delete an email template"""
    template_id: str


class DeleteEmailTemplateCommandHandler(CommandHandler[DeleteEmailTemplateCommand]):
    """Handler for DeleteEmailTemplateCommand"""

    def __init__(self, repository: EmailTemplateRepositoryInterface):
        self._repository = repository

    def execute(self, command: DeleteEmailTemplateCommand) -> None:
        """Execute the delete email template command"""
        template_id = EmailTemplateId.from_string(command.template_id)

        deleted = self._repository.delete(template_id)

        if not deleted:
            raise ValueError(f"Email template not found: {command.template_id}")
