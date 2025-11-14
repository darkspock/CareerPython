from dataclasses import dataclass
from typing import Optional

from src.interview_bc.interview_template.domain.enums.interview_template import InterviewTemplateStatusEnum
from src.interview_bc.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException,
    InvalidTemplateStateException
)
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository
from src.framework.application.command_bus import Command


@dataclass
class DraftInterviewTemplateCommand(Command):
    template_id: InterviewTemplateId
    drafted_by: str
    draft_reason: Optional[str] = None


class DraftInterviewTemplateCommandHandler:
    def __init__(
            self,
            template_repository: InterviewTemplateRepository
    ):
        self.template_repository = template_repository

    def execute(self, command: DraftInterviewTemplateCommand) -> None:
        """Move template back to draft (ENABLED/DISABLED → DRAFT)"""

        # Get the template
        template = self.template_repository.get_by_id(command.template_id)
        if not template:
            raise InterviewTemplateNotFoundException(f"Template with id {command.template_id.value} not found")

        # Validate that template can be drafted
        if template.status == InterviewTemplateStatusEnum.DRAFT:
            raise InvalidTemplateStateException(
                f"Template {command.template_id.value} is already in DRAFT status"
            )

        # Draft the template using the entity method
        template.draft()
        self.template_repository.update(template)
