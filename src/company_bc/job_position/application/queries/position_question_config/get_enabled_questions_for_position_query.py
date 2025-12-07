from dataclasses import dataclass
from typing import List, Optional, Any
from datetime import datetime

from src.framework.application.query_bus import Query, QueryHandler
from src.company_bc.job_position.domain.repositories.position_question_config_repository_interface import (
    PositionQuestionConfigRepositoryInterface
)
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import (
    JobPositionRepository
)
from src.shared_bc.customization.workflow.domain.interfaces.application_question_repository_interface import (
    ApplicationQuestionRepositoryInterface
)
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.enums.application_question_field_type import (
    ApplicationQuestionFieldType
)


@dataclass(frozen=True)
class EnabledQuestionDto:
    """
    DTO for a question that is enabled for a position.

    Combines the workflow-level question definition with any position-level overrides.
    """
    id: str
    workflow_id: str
    field_key: str
    label: str
    field_type: ApplicationQuestionFieldType
    description: Optional[str]
    options: Optional[List[Any]]
    is_required: bool  # Effective required state (position override or workflow default)
    sort_order: int  # Effective sort order (position override or workflow default)
    validation_rules: Optional[dict]


@dataclass(frozen=True)
class EnabledQuestionsListDto:
    """DTO for list of enabled questions for a position."""
    questions: List[EnabledQuestionDto]
    total: int
    position_id: str
    workflow_id: Optional[str]


@dataclass
class GetEnabledQuestionsForPositionQuery(Query):
    """
    Query to get all enabled questions for a job position.

    This combines:
    1. Active questions from the position's workflow
    2. Position-level configurations (enabled/disabled, overrides)

    Returns only questions that are enabled for this position.
    """
    position_id: str


class GetEnabledQuestionsForPositionQueryHandler(
    QueryHandler[GetEnabledQuestionsForPositionQuery, EnabledQuestionsListDto]
):
    """Handler for GetEnabledQuestionsForPositionQuery."""

    def __init__(
        self,
        job_position_repository: JobPositionRepository,
        application_question_repository: ApplicationQuestionRepositoryInterface,
        position_question_config_repository: PositionQuestionConfigRepositoryInterface
    ):
        self.job_position_repository = job_position_repository
        self.application_question_repository = application_question_repository
        self.position_question_config_repository = position_question_config_repository

    def handle(self, query: GetEnabledQuestionsForPositionQuery) -> EnabledQuestionsListDto:
        """Handle the query - returns list of enabled questions for the position."""
        position_id = JobPositionId(query.position_id)

        # Get the job position to find its workflow
        position = self.job_position_repository.get_by_id(position_id)
        if not position:
            return EnabledQuestionsListDto(
                questions=[],
                total=0,
                position_id=query.position_id,
                workflow_id=None
            )

        job_position_workflow_id = position.job_position_workflow_id
        if not job_position_workflow_id:
            return EnabledQuestionsListDto(
                questions=[],
                total=0,
                position_id=query.position_id,
                workflow_id=None
            )

        # Convert JobPositionWorkflowId to WorkflowId
        workflow_id = WorkflowId(job_position_workflow_id.value)

        # Get all active questions from the workflow
        workflow_questions = self.application_question_repository.list_by_workflow(
            workflow_id=workflow_id,
            active_only=True
        )

        if not workflow_questions:
            return EnabledQuestionsListDto(
                questions=[],
                total=0,
                position_id=query.position_id,
                workflow_id=str(workflow_id)
            )

        # Get position-level configs
        position_configs = self.position_question_config_repository.list_by_position(
            position_id=position_id,
            enabled_only=False  # Get all configs to check disabled ones
        )

        # Build a map of question_id -> config for quick lookup
        config_map = {str(config.question_id.value): config for config in position_configs}

        # Build the list of enabled questions with effective values
        enabled_questions: List[EnabledQuestionDto] = []

        for question in workflow_questions:
            question_id = str(question.id.value)
            config = config_map.get(question_id)

            # Determine if question is enabled
            # If no config exists, question is enabled by default
            # If config exists, use its enabled state
            if config is not None and not config.enabled:
                # Question is explicitly disabled for this position
                continue

            # Determine effective is_required
            is_required = question.is_required_default
            if config is not None and config.is_required_override is not None:
                is_required = config.is_required_override

            # Determine effective sort_order
            sort_order = question.sort_order
            if config is not None and config.sort_order_override is not None:
                sort_order = config.sort_order_override

            enabled_questions.append(EnabledQuestionDto(
                id=question_id,
                workflow_id=str(question.workflow_id.value),
                field_key=question.field_key,
                label=question.label,
                field_type=question.field_type,
                description=question.description,
                options=question.options,
                is_required=is_required,
                sort_order=sort_order,
                validation_rules=question.validation_rules
            ))

        # Sort by effective sort_order
        enabled_questions.sort(key=lambda q: q.sort_order)

        return EnabledQuestionsListDto(
            questions=enabled_questions,
            total=len(enabled_questions),
            position_id=query.position_id,
            workflow_id=str(workflow_id)
        )
