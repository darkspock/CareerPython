"""
Create Email Template Command
Phase 7: Command to create a new email template
"""

from dataclasses import dataclass
from typing import List, Optional

from src.email_template.domain.entities.email_template import EmailTemplate
from src.email_template.domain.enums.trigger_event import TriggerEvent
from src.email_template.domain.repositories.email_template_repository_interface import EmailTemplateRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateEmailTemplateCommand(Command):
    """Command to create a new email template"""
    workflow_id: str
    template_name: str
    template_key: str
    subject: str
    body_html: str
    trigger_event: TriggerEvent
    available_variables: List[str]
    stage_id: Optional[str] = None
    body_text: Optional[str] = None
    is_active: bool = True


class CreateEmailTemplateCommandHandler(CommandHandler[CreateEmailTemplateCommand]):
    """Handler for CreateEmailTemplateCommand"""

    def __init__(self, repository: EmailTemplateRepositoryInterface):
        self._repository = repository

    def execute(self, command: CreateEmailTemplateCommand) -> None:
        """Execute the create email template command"""
        # Check if template already exists for this workflow+stage+trigger
        if self._repository.exists(
                workflow_id=command.workflow_id,
                stage_id=command.stage_id,
                trigger_event=command.trigger_event
        ):
            raise ValueError(
                f"Email template already exists for workflow {command.workflow_id}, "
                f"stage {command.stage_id}, trigger {command.trigger_event.value}"
            )

        # Create the template entity
        template = EmailTemplate.create(
            workflow_id=command.workflow_id,
            template_name=command.template_name,
            template_key=command.template_key,
            subject=command.subject,
            body_html=command.body_html,
            trigger_event=command.trigger_event,
            available_variables=command.available_variables,
            stage_id=command.stage_id,
            body_text=command.body_text,
            is_active=command.is_active
        )

        # Save to repository
        self._repository.save(template)
