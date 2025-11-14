from dataclasses import dataclass
from typing import Optional

from src.framework.application.command_bus import Command
from src.interview_bc.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException
)
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_section_repository import \
    InterviewTemplateSectionRepository


@dataclass
class DeleteInterviewTemplateCommand(Command):
    template_id: InterviewTemplateId
    deleted_by: str
    delete_reason: Optional[str] = None
    force_delete: bool = False  # Force delete even if template has sections


class DeleteInterviewTemplateCommandHandler:
    def __init__(
            self,
            template_repository: InterviewTemplateRepository,
            section_repository: InterviewTemplateSectionRepository,
    ):
        self.template_repository = template_repository
        self.section_repository = section_repository

    def execute(self, command: DeleteInterviewTemplateCommand) -> None:
        """Physically delete an interview template"""

        # Get the template
        template = self.template_repository.get_by_id(command.template_id)
        if not template:
            raise InterviewTemplateNotFoundException(f"Template with id {command.template_id.value} not found")

        # Check if template is disabled (business rule: only disabled templates can be deleted)
        if template.status.value != 'DISABLED' and not command.force_delete:
            raise ValueError(
                "Only disabled templates can be deleted. Disable the template first or use force_delete=True.")

        # Check if template has sections
        sections = self.section_repository.get_by_template_id(command.template_id)
        if sections and not command.force_delete:
            raise ValueError(
                "Cannot delete template with sections. Delete all sections first or use force_delete=True.")

        # If force_delete is True, delete all sections first
        if command.force_delete and sections:
            for section in sections:
                self.section_repository.delete(section.id)

        # Delete the template physically (hard delete)
        self.template_repository.delete(command.template_id.value, soft_delete=False)
