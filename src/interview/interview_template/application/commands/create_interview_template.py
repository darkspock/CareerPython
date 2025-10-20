from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from src.company.domain.value_objects.company_id import CompanyId
from src.interview.interview_template.domain.entities.interview_template import InterviewTemplate
from src.interview.interview_template.domain.enums import InterviewTemplateStatusEnum, InterviewTemplateTypeEnum
from src.interview.interview_template.domain.infrastructure.interview_template_repository_interface import \
    InterviewTemplateRepositoryInterface
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.shared.application.command_bus import Command, CommandHandler
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class CreateInterviewTemplateCommand(Command):
    id: InterviewTemplateId
    company_id: Optional[CompanyId]
    name: str
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    template_type: InterviewTemplateTypeEnum = InterviewTemplateTypeEnum.EXTENDED_PROFILE
    job_category: Optional[JobCategoryEnum] = None
    allow_ai_questions: bool = False
    legal_notice: Optional[str] = None
    created_by: str = ""
    tags: Optional[List[str]] = None
    template_metadata: Optional[Dict[str, Any]] = None


class CreateInterviewTemplateCommandHandler(CommandHandler[CreateInterviewTemplateCommand]):
    def __init__(self, interview_template_repository: InterviewTemplateRepositoryInterface):
        self.interview_template_repository = interview_template_repository

    def execute(self, command: CreateInterviewTemplateCommand) -> None:
        new_interview_template = InterviewTemplate.create(
            id=command.id,
            name=command.name,
            intro=command.intro or "",
            prompt=command.prompt or "",
            goal=command.goal or "",
            status=InterviewTemplateStatusEnum.DRAFT,  # New templates start as DRAFT
            template_type=command.template_type,
            job_category=command.job_category,
            allow_ai_questions=command.allow_ai_questions,
            legal_notice=command.legal_notice,
            tags=command.tags or [],
            metadata=command.template_metadata or {},
            company_id=command.company_id  # Company association can be set later
        )
        self.interview_template_repository.create(new_interview_template)
