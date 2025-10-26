"""
Update Email Template Command
Phase 7: Command to update an existing email template
"""

from dataclasses import dataclass
from typing import List, Optional

from src.email_template.domain.value_objects.email_template_id import EmailTemplateId
from src.email_template.domain.repositories.email_template_repository_interface import EmailTemplateRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateEmailTemplateCommand(Command):
    """Command to update an email template"""
    template_id: str
    template_name: str
    subject: str
    body_html: str
    available_variables: List[str]
    body_text: Optional[str] = None


class UpdateEmailTemplateCommandHandler(CommandHandler[UpdateEmailTemplateCommand]):
    """Handler for UpdateEmailTemplateCommand"""

    def __init__(self, repository: EmailTemplateRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateEmailTemplateCommand) -> None:
        """Execute the update email template command"""
        # Get existing template
        template_id = EmailTemplateId.from_string(command.template_id)
        template = self._repository.get_by_id(template_id)

        if not template:
            raise ValueError(f"Email template not found: {command.template_id}")

        # Update the template
        updated_template = template.update(
            template_name=command.template_name,
            subject=command.subject,
            body_html=command.body_html,
            available_variables=command.available_variables,
            body_text=command.body_text
        )

        # Save changes
        self._repository.save(updated_template)
