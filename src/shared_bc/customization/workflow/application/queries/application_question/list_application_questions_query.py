from dataclasses import dataclass

from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow.application.dtos.application_question_dto import (
    ApplicationQuestionListDto
)
from src.shared_bc.customization.workflow.application.mappers.application_question_dto_mapper import (
    ApplicationQuestionDtoMapper
)
from src.shared_bc.customization.workflow.domain.interfaces.application_question_repository_interface import (
    ApplicationQuestionRepositoryInterface
)
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass
class ListApplicationQuestionsQuery(Query):
    """Query to list application questions for a workflow."""
    workflow_id: str
    active_only: bool = True


class ListApplicationQuestionsQueryHandler(QueryHandler[ListApplicationQuestionsQuery, ApplicationQuestionListDto]):
    """Handler for ListApplicationQuestionsQuery."""

    def __init__(self, repository: ApplicationQuestionRepositoryInterface):
        self.repository = repository

    def handle(self, query: ListApplicationQuestionsQuery) -> ApplicationQuestionListDto:
        """Handle the query."""
        workflow_id = WorkflowId.from_string(query.workflow_id)
        questions = self.repository.list_by_workflow(workflow_id, query.active_only)
        return ApplicationQuestionDtoMapper.to_dto_list(questions)
