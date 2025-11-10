from dataclasses import dataclass

from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateSectionNotFoundException
)
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview.interview_template.infrastructure.repositories.interview_template_section_repository import \
    InterviewTemplateSectionRepository
from src.framework.application.command_bus import Command


@dataclass
class MoveSectionDownCommand(Command):
    section_id: InterviewTemplateSectionId
    moved_by: str


class MoveSectionDownCommandHandler:
    def __init__(
            self,
            section_repository: InterviewTemplateSectionRepository,
    ):
        self.section_repository = section_repository

    def execute(self, command: MoveSectionDownCommand) -> None:
        """Move a section down in the order (increase sort_order)"""

        # Get the section to move
        section = self.section_repository.get_by_id(command.section_id)
        if not section:
            raise InterviewTemplateSectionNotFoundException(f"Section with id {command.section_id.value} not found")

        # Get all sections for the same template, ordered by sort_order
        all_sections = self.section_repository.get_by_template_id(section.interview_template_id)

        # Find the current section index
        current_index = -1
        for i, s in enumerate(all_sections):
            if s.id.value == section.id.value:
                current_index = i
                break

        if current_index == -1:
            raise InterviewTemplateSectionNotFoundException(
                f"Section with id {command.section_id.value} not found in template")

        # If already at the bottom, do nothing
        if current_index == len(all_sections) - 1:
            return

        # Swap sort orders with the next section
        next_section = all_sections[current_index + 1]
        current_sort_order = section.sort_order
        next_sort_order = next_section.sort_order

        # Update sort orders
        section.update_sort_order(next_sort_order)
        next_section.update_sort_order(current_sort_order)

        # Save both sections
        self.section_repository.update(section)
        self.section_repository.update(next_section)
