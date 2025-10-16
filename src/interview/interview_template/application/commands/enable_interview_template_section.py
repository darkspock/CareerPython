from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.application.commands.enable_interview_template_question import (
    EnableInterviewTemplateQuestionCommand,
    EnableInterviewTemplateQuestionCommandHandler
)
from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException
)
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.interview.interview_template.infrastructure.repositories.interview_template_section_repository import \
    InterviewTemplateSectionRepository
from src.shared.application.command_bus import Command


@dataclass
class EnableInterviewTemplateSectionCommand(Command):
    section_id: InterviewTemplateSectionId
    enabled_by: str
    enable_reason: Optional[str] = None


class EnableInterviewTemplateSectionCommandHandler:
    def __init__(
            self,
            section_repository: InterviewTemplateSectionRepository,
            question_repository: InterviewTemplateQuestionRepository
    ):
        self.section_repository = section_repository
        self.question_repository = question_repository

    def execute(self, command: EnableInterviewTemplateSectionCommand) -> None:
        """Enable a previously disabled interview template section and all its questions"""

        # Get the section
        section = self.section_repository.get_by_id(command.section_id)
        if not section:
            raise InterviewTemplateNotFoundException(f"Section with id {command.section_id.value} not found")

        # Enable the section using the entity method
        section.enable()
        self.section_repository.update(section)

        # Get all questions for this section
        questions = self.question_repository.get_by_section_id(command.section_id)

        # Enable all questions in this section
        question_enable_handler = EnableInterviewTemplateQuestionCommandHandler(self.question_repository)

        for question in questions:
            try:
                enable_question_command = EnableInterviewTemplateQuestionCommand(
                    question_id=question.id,
                    enabled_by=command.enabled_by,
                    enable_reason=f"Enabled automatically when section {command.section_id} was enabled"
                )
                question_enable_handler.execute(enable_question_command)
            except Exception as e:
                # Log error but continue with other questions
                # In a real implementation, you might want to use proper logging
                print(f"Warning: Could not enable question {question.id.value}: {str(e)}")
