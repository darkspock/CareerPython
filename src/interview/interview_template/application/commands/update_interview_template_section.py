from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.entities.interview_template_section import InterviewTemplateSection
from src.interview.interview_template.domain.enums import InterviewTemplateSectionEnum
from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException
)
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview.interview_template.infrastructure.repositories.interview_template_section_repository import \
    InterviewTemplateSectionRepository
from src.shared.application.command_bus import Command


@dataclass
class UpdateInterviewTemplateSectionCommand(Command):
    section_id: InterviewTemplateSectionId
    name: Optional[str] = None
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    section: Optional[InterviewTemplateSectionEnum] = None
    updated_by: Optional[str] = None


class UpdateInterviewTemplateSectionCommandHandler:
    def __init__(self, section_repository: InterviewTemplateSectionRepository):
        self.section_repository = section_repository

    def execute(self, command: UpdateInterviewTemplateSectionCommand) -> InterviewTemplateSection:
        """Update an existing interview template section"""

        # Get the existing section
        section = self.section_repository.get_by_id(command.section_id)
        if not section:
            raise InterviewTemplateNotFoundException(f"Section with id {command.section_id.value} not found")

        # Update section properties
        if command.name is not None:
            section.name = command.name

        if command.intro is not None:
            section.intro = command.intro

        if command.prompt is not None:
            section.prompt = command.prompt

        if command.goal is not None:
            section.goal = command.goal

        if command.section is not None:
            section.section = command.section

        # Save and return updated section
        return self.section_repository.update(section)
