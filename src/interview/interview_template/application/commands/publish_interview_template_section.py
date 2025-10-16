from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.enums.interview_template_section import InterviewTemplateSectionStatusEnum
from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException,
    InvalidTemplateStateException
)
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview.interview_template.infrastructure.repositories.interview_template_section_repository import \
    InterviewTemplateSectionRepository
from src.shared.application.command_bus import Command


@dataclass
class PublishInterviewTemplateSectionCommand(Command):
    section_id: InterviewTemplateSectionId
    published_by: str
    publish_reason: Optional[str] = None


class PublishInterviewTemplateSectionCommandHandler:
    def __init__(
            self,
            section_repository: InterviewTemplateSectionRepository
    ):
        self.section_repository = section_repository

    def execute(self, command: PublishInterviewTemplateSectionCommand) -> None:
        """Publish a section (DRAFT → ENABLED)"""

        # Get the section
        section = self.section_repository.get_by_id(command.section_id)
        if not section:
            raise InterviewTemplateNotFoundException(f"Section with id {command.section_id.value} not found")

        # Validate that section can be published
        if section.status != InterviewTemplateSectionStatusEnum.DRAFT:
            raise InvalidTemplateStateException(
                f"Section {command.section_id.value} must be in DRAFT status to be published. Current status: {section.status.value}"
            )

        # Publish the section using the entity method
        section.enable()
        self.section_repository.update(section)
