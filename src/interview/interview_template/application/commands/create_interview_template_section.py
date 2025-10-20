from dataclasses import dataclass
from typing import Optional

from src.company.domain.value_objects.company_id import CompanyId
from src.interview.interview_template.domain.entities.interview_template_section import InterviewTemplateSection
from src.interview.interview_template.domain.enums import InterviewTemplateSectionEnum
from src.interview.interview_template.domain.infrastructure.interview_template_section_repository_interface import \
    InterviewTemplateSectionRepositoryInterface
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class CreateInterviewTemplateSectionCommand(Command):
    id: InterviewTemplateSectionId
    company_id: Optional[CompanyId]
    interview_template_id: InterviewTemplateId
    section: Optional[InterviewTemplateSectionEnum]
    name: str
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    sort_order: int = 0
    allow_ai_questions: bool = False
    allow_ai_override_questions: bool = False
    legal_notice: Optional[str] = None
    created_by: str = ""


class CreateInterviewTemplateSectionCommandHandler(CommandHandler[CreateInterviewTemplateSectionCommand]):
    def __init__(self, interview_template_section_repository: InterviewTemplateSectionRepositoryInterface):
        self.interview_template_section_repository = interview_template_section_repository

    def execute(self, command: CreateInterviewTemplateSectionCommand) -> None:
        new_interview_template = InterviewTemplateSection.create(
            id=command.id,
            name=command.name,
            intro=command.intro or "",
            prompt=command.prompt or "",
            goal=command.goal or "",
            interview_template_id=command.interview_template_id,
            section=command.section,
            sort_order=command.sort_order,
            allow_ai_questions=command.allow_ai_questions,
            allow_ai_override_questions=command.allow_ai_override_questions,
            legal_notice=command.legal_notice
        )
        self.interview_template_section_repository.create(new_interview_template)
