import ulid

from src.framework.application.query_bus import QueryBus
from src.framework.application.command_bus import CommandBus
from src.shared_bc.customization.workflow.application.queries.application_question.list_application_questions_query import (
    ListApplicationQuestionsQuery
)
from src.shared_bc.customization.workflow.application.commands.application_question.create_application_question_command import (
    CreateApplicationQuestionCommand
)
from src.shared_bc.customization.workflow.application.commands.application_question.update_application_question_command import (
    UpdateApplicationQuestionCommand
)
from src.shared_bc.customization.workflow.application.commands.application_question.delete_application_question_command import (
    DeleteApplicationQuestionCommand
)
from src.shared_bc.customization.workflow.application.dtos.application_question_dto import (
    ApplicationQuestionListDto
)
from adapters.http.company_app.application_question.schemas.application_question_schemas import (
    ApplicationQuestionListResponse,
    CreateApplicationQuestionRequest,
    UpdateApplicationQuestionRequest
)
from adapters.http.company_app.application_question.mappers.application_question_mapper import (
    ApplicationQuestionMapper
)


class ApplicationQuestionController:
    """Controller for application question operations."""

    def __init__(self, query_bus: QueryBus, command_bus: CommandBus):
        self.query_bus = query_bus
        self.command_bus = command_bus

    def list_questions(
        self,
        workflow_id: str,
        active_only: bool = True
    ) -> ApplicationQuestionListResponse:
        """List application questions for a workflow."""
        result: ApplicationQuestionListDto = self.query_bus.query(
            ListApplicationQuestionsQuery(
                workflow_id=workflow_id,
                active_only=active_only
            )
        )
        return ApplicationQuestionMapper.dto_list_to_response(result)

    def create_question(
        self,
        workflow_id: str,
        company_id: str,
        request: CreateApplicationQuestionRequest
    ) -> str:
        """Create a new application question. Returns the new question ID."""
        question_id = str(ulid.new())
        self.command_bus.execute(
            CreateApplicationQuestionCommand(
                id=question_id,
                workflow_id=workflow_id,
                company_id=company_id,
                field_key=request.field_key,
                label=request.label,
                field_type=request.field_type,
                description=request.description,
                options=request.options,
                is_required_default=request.is_required_default,
                validation_rules=request.validation_rules,
                sort_order=request.sort_order
            )
        )
        return question_id

    def update_question(
        self,
        question_id: str,
        request: UpdateApplicationQuestionRequest
    ) -> None:
        """Update an application question."""
        self.command_bus.execute(
            UpdateApplicationQuestionCommand(
                id=question_id,
                label=request.label,
                description=request.description,
                options=request.options,
                is_required_default=request.is_required_default,
                validation_rules=request.validation_rules,
                sort_order=request.sort_order
            )
        )

    def delete_question(self, question_id: str) -> None:
        """Delete an application question."""
        self.command_bus.execute(
            DeleteApplicationQuestionCommand(id=question_id)
        )
