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
from src.framework.application.command_bus import Command


@dataclass
class DraftInterviewTemplateSectionCommand(Command):
    section_id: InterviewTemplateSectionId
    drafted_by: str
    draft_reason: Optional[str] = None


class DraftInterviewTemplateSectionCommandHandler:
    def __init__(
            self,
            section_repository: InterviewTemplateSectionRepository
    ):
        self.section_repository = section_repository

    def execute(self, command: DraftInterviewTemplateSectionCommand) -> None:
        """Move section back to draft (ENABLED/DISABLED → DRAFT)"""

        # Get the section
        section = self.section_repository.get_by_id(command.section_id)
        if not section:
            raise InterviewTemplateNotFoundException(f"Section with id {command.section_id.value} not found")

        # Validate that section can be drafted
        if section.status == InterviewTemplateSectionStatusEnum.DRAFT:
            raise InvalidTemplateStateException(
                f"Section {command.section_id.value} is already in DRAFT status"
            )

        # Draft the section by setting status to DRAFT
        section.status = InterviewTemplateSectionStatusEnum.DRAFT
        self.section_repository.update(section)
