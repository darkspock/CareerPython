from dataclasses import dataclass
from typing import Optional

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.job_position.domain.exceptions import JobPositionNotFoundException
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import \
    JobPositionRepositoryInterface
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.entities.base import generate_id
from src.interview_bc.interview_template.domain.entities.interview_template import InterviewTemplate
from src.interview_bc.interview_template.domain.enums import (
    InterviewTemplateStatusEnum,
    InterviewTemplateTypeEnum,
    InterviewTemplateScopeEnum
)
from src.interview_bc.interview_template.domain.infrastructure.interview_template_repository_interface import \
    InterviewTemplateRepositoryInterface
from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateId


@dataclass
class CreateInlineScreeningTemplateCommand(Command):
    """Create a screening template inline and link it to a job position"""
    position_id: JobPositionId
    company_id: CompanyId
    name: Optional[str] = None  # If not provided, uses position title
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    created_by: Optional[str] = None


@dataclass
class CreateInlineScreeningTemplateResult:
    """Result of creating inline screening template"""
    template_id: str
    position_id: str
    success: bool
    message: str


class CreateInlineScreeningTemplateCommandHandler(CommandHandler[CreateInlineScreeningTemplateCommand]):
    def __init__(
        self,
        job_position_repository: JobPositionRepositoryInterface,
        interview_template_repository: InterviewTemplateRepositoryInterface
    ):
        self.job_position_repository = job_position_repository
        self.interview_template_repository = interview_template_repository

    def execute(self, command: CreateInlineScreeningTemplateCommand) -> None:
        # Get the job position
        job_position = self.job_position_repository.get_by_id(command.position_id)
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.position_id.value} not found"
            )

        # Create the screening template
        template_id = InterviewTemplateId.from_string(generate_id())
        template_name = command.name or f"Screening - {job_position.title}"

        new_template = InterviewTemplate.create(
            id=template_id,
            company_id=command.company_id,
            name=template_name,
            intro=command.intro or f"Screening interview for {job_position.title}",
            prompt=command.prompt or "",
            goal=command.goal or "Evaluate candidate fit for the position",
            status=InterviewTemplateStatusEnum.DRAFT,
            template_type=InterviewTemplateTypeEnum.SCREENING,
            scope=InterviewTemplateScopeEnum.APPLICATION,
            job_category=job_position.job_category,
            allow_ai_questions=False,
            use_conversational_mode=False,
            scoring_mode=None,
            legal_notice=None,
            tags=["screening", "inline"],
            metadata={
                "created_for_position_id": command.position_id.value,
                "created_by": command.created_by
            }
        )

        # Save the template
        self.interview_template_repository.create(new_template)

        # Update job position with the new screening template
        job_position.set_screening_template(template_id.value)
        self.job_position_repository.save(job_position)
