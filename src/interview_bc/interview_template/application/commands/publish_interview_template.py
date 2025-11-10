from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.enums.interview_template import InterviewTemplateStatusEnum
from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException,
    InvalidTemplateStateException
)
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository
from src.framework.application.command_bus import Command


@dataclass
class PublishInterviewTemplateCommand(Command):
    template_id: InterviewTemplateId
    published_by: str
    publish_reason: Optional[str] = None


class PublishInterviewTemplateCommandHandler:
    def __init__(
            self,
            template_repository: InterviewTemplateRepository
    ):
        self.template_repository = template_repository

    def execute(self, command: PublishInterviewTemplateCommand) -> None:
        """Publish a template (DRAFT → ENABLED)"""

        # Get the template
        template = self.template_repository.get_by_id(command.template_id)
        if not template:
            raise InterviewTemplateNotFoundException(f"Template with id {command.template_id.value} not found")

        # Validate that template can be published
        if template.status != InterviewTemplateStatusEnum.DRAFT:
            raise InvalidTemplateStateException(
                f"Template {command.template_id.value} must be in DRAFT status to be published. Current status: {template.status.value}"
            )

        # Publish the template using the entity method
        template.enable()
        self.template_repository.update(template)
