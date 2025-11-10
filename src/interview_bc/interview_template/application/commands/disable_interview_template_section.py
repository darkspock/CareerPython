from dataclasses import dataclass
from typing import Optional

from src.interview_bc.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException
)
from src.interview_bc.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_section_repository import \
    InterviewTemplateSectionRepository
from src.framework.application.command_bus import Command


@dataclass
class DisableInterviewTemplateSectionCommand(Command):
    section_id: InterviewTemplateSectionId
    disabled_by: str
    disable_reason: Optional[str] = None


class DisableInterviewTemplateSectionCommandHandler:
    def __init__(
            self,
            section_repository: InterviewTemplateSectionRepository
    ):
        self.section_repository = section_repository

    def execute(self, command: DisableInterviewTemplateSectionCommand) -> None:
        """Disable an interview template section"""

        # Get the section
        section = self.section_repository.get_by_id(command.section_id)
        if not section:
            raise InterviewTemplateNotFoundException(f"Section with id {command.section_id.value} not found")

        # Disable the section using the entity method
        section.disable()
        self.section_repository.update(section)
