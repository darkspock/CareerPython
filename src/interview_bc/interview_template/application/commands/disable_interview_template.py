from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException
)
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository
from src.framework.application.command_bus import Command


@dataclass
class DisableInterviewTemplateCommand(Command):
    template_id: InterviewTemplateId
    disabled_by: str
    disable_reason: Optional[str] = None
    force_disable: bool = False  # Force disable even if template is in use


class DisableInterviewTemplateCommandHandler:
    def __init__(
            self,
            template_repository: InterviewTemplateRepository,

    ):
        self.template_repository = template_repository

    def execute(self, command: DisableInterviewTemplateCommand) -> None:
        """Disable an interview template instead of deleting it"""

        # Get the template
        template = self.template_repository.get_by_id(command.template_id)
        if not template:
            raise InterviewTemplateNotFoundException(f"Template with id {command.template_id.value} not found")

        # Disable the template using the entity method
        template.disable()
        self.template_repository.update(template)
