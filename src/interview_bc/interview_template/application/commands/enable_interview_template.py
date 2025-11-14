from dataclasses import dataclass
from typing import Optional

from src.framework.application.command_bus import Command
from src.interview_bc.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException
)
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository


@dataclass
class EnableInterviewTemplateCommand(Command):
    template_id: InterviewTemplateId
    enabled_by: str
    enable_reason: Optional[str] = None


class EnableInterviewTemplateCommandHandler:
    def __init__(
            self,
            template_repository: InterviewTemplateRepository
    ):
        self.template_repository = template_repository

    def execute(self, command: EnableInterviewTemplateCommand) -> None:
        """Enable a previously disabled interview template"""

        # Get the template
        template = self.template_repository.get_by_id(command.template_id)
        if not template:
            raise InterviewTemplateNotFoundException(f"Template with id {command.template_id.value} not found")

        # Enable the template using the entity method
        template.enable()
        self.template_repository.update(template)
