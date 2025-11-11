from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

from src.interview_bc.interview_template.domain.entities.interview_template import InterviewTemplate
from src.interview_bc.interview_template.domain.enums import InterviewTemplateTypeEnum
from src.interview_bc.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException,
    InvalidTemplateStateException
)
from src.interview_bc.interview_template.domain.infrastructure.interview_template_repository_interface import \
    InterviewTemplateRepositoryInterface
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class UpdateInterviewTemplateCommand(Command):
    template_id: InterviewTemplateId
    name: Optional[str] = None
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    type: Optional[InterviewTemplateTypeEnum] = None
    job_category: Optional[JobCategoryEnum] = None
    allow_ai_questions: Optional[bool] = None
    legal_notice: Optional[str] = None
    tags: Optional[List[str]] = None
    template_metadata: Optional[Dict[str, Any]] = None
    updated_by: Optional[str] = None


class UpdateInterviewTemplateCommandHandler(CommandHandler[UpdateInterviewTemplateCommand]):
    def __init__(self, template_repository: InterviewTemplateRepository):
        self.template_repository = template_repository

    def execute(self, command: UpdateInterviewTemplateCommand) -> None:
        """Update an existing interview template"""

        # Get the existing template
        template = self.template_repository.get_by_id(command.template_id)
        if not template:
            raise InterviewTemplateNotFoundException(f"Template with id {command.template_id.value} not found")

        # Validate template can be updated
        if not self._can_update_template(template):
            raise InvalidTemplateStateException(f"Template {command.template_id} cannot be updated in current state")

        # Update template properties (all fields except status)
        if command.name is not None:
            template.name = command.name

        if command.intro is not None:
            template.intro = command.intro

        if command.prompt is not None:
            template.prompt = command.prompt

        if command.goal is not None:
            template.goal = command.goal

        if command.type is not None:
            template.template_type = command.type

        if command.job_category is not None:
            template.job_category = command.job_category

        if command.allow_ai_questions is not None:
            template.allow_ai_questions = command.allow_ai_questions

        if command.legal_notice is not None:
            template.legal_notice = command.legal_notice

        if command.tags is not None:
            template.tags = command.tags

        if command.template_metadata:
            # Merge metadata
            if hasattr(template, 'metadata') and template.metadata:
                template.metadata.update(command.template_metadata)
            else:
                template.metadata = command.template_metadata

        if command.updated_by:
            if not hasattr(template, 'metadata') or not template.metadata:
                template.metadata = {}
            template.metadata["last_updated_by"] = command.updated_by

        self.template_repository.update(template)

    def _can_update_template(self, template: InterviewTemplate) -> bool:
        """Check if template can be updated"""
        # Templates can be updated unless they are in use by active interviews
        # This would need to check for active interviews using this template
        return True  # Simplified for now


@dataclass
class DeactivateInterviewTemplateCommand(Command):
    template_id: InterviewTemplateId
    deactivated_by: str
    deactivation_reason: Optional[str] = None


class DeactivateInterviewTemplateCommandHandler(CommandHandler[DeactivateInterviewTemplateCommand]):
    def __init__(self, template_repository: InterviewTemplateRepositoryInterface):
        self.template_repository = template_repository

    def execute(self, command: DeactivateInterviewTemplateCommand) -> None:
        """Deactivate an interview template"""

        # Get the template
        template = self.template_repository.get_by_id(command.template_id)
        if not template:
            raise InterviewTemplateNotFoundException(f"Template with id {command.template_id} not found")

        # Add deactivation metadata
        deactivation_metadata = {
            "deactivated_by": command.deactivated_by,
            "deactivation_timestamp": datetime.utcnow().isoformat(),
            "deactivation_reason": command.deactivation_reason or "Manual deactivation"
        }

        if template.metadata:
            template.metadata.update(deactivation_metadata)
        else:
            template.metadata = deactivation_metadata

        self.template_repository.update(template)
