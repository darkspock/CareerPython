from dataclasses import dataclass
from typing import Optional

from src.interview_bc.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateSectionNotFoundException
)
from src.interview_bc.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_section_repository import \
    InterviewTemplateSectionRepository
from src.framework.application.command_bus import Command


@dataclass
class DeleteInterviewTemplateSectionCommand(Command):
    section_id: InterviewTemplateSectionId
    deleted_by: str
    delete_reason: Optional[str] = None
    force_delete: bool = False  # Force delete even if section has questions


class DeleteInterviewTemplateSectionCommandHandler:
    def __init__(
            self,
            section_repository: InterviewTemplateSectionRepository,
    ):
        self.section_repository = section_repository

    def execute(self, command: DeleteInterviewTemplateSectionCommand) -> None:
        """Physically delete an interview template section"""

        # Get the section
        section = self.section_repository.get_by_id(command.section_id)
        if not section:
            raise InterviewTemplateSectionNotFoundException(f"Section with id {command.section_id.value} not found")

        # Check if section is disabled (business rule: only disabled sections can be deleted)
        if section.status.value != 'DISABLED' and not command.force_delete:
            raise ValueError(
                "Only disabled sections can be deleted. Disable the section first or use force_delete=True.")

        # Delete the section physically
        self.section_repository.delete(command.section_id)
