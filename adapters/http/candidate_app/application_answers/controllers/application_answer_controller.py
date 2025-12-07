"""Controller for Application Question Answer operations."""
from typing import List

from src.framework.application.query_bus import QueryBus
from src.framework.application.command_bus import CommandBus
from src.company_bc.candidate_application.application.queries.question_answer.list_application_answers_query import (
    ListApplicationAnswersQuery
)
from src.company_bc.candidate_application.application.queries.question_answer.application_answer_dto import (
    ApplicationAnswerListDto
)
from src.company_bc.candidate_application.application.commands.question_answer.save_application_answers_command import (
    SaveApplicationAnswersCommand,
    AnswerInput as CommandAnswerInput
)
from src.company_bc.job_position.application.queries.position_question_config.get_enabled_questions_for_position_query import (
    GetEnabledQuestionsForPositionQuery,
    EnabledQuestionsListDto
)
from adapters.http.candidate_app.application_answers.schemas.application_answer_schemas import (
    SaveAnswersRequest,
    ApplicationAnswerListResponse,
    EnabledQuestionsListResponse
)
from adapters.http.candidate_app.application_answers.mappers.application_answer_mapper import (
    ApplicationAnswerMapper
)


class ApplicationAnswerController:
    """Controller for application answer operations."""

    def __init__(self, query_bus: QueryBus, command_bus: CommandBus):
        self.query_bus = query_bus
        self.command_bus = command_bus

    def list_answers(
        self,
        application_id: str
    ) -> ApplicationAnswerListResponse:
        """List all answers for an application."""
        result: ApplicationAnswerListDto = self.query_bus.query(
            ListApplicationAnswersQuery(application_id=application_id)
        )
        return ApplicationAnswerMapper.dto_list_to_response(result)

    def save_answers(
        self,
        application_id: str,
        request: SaveAnswersRequest
    ) -> None:
        """Save answers for an application."""
        # Convert request to command
        answers = [
            CommandAnswerInput(
                question_id=answer.question_id,
                answer_value=answer.answer_value
            )
            for answer in request.answers
        ]

        self.command_bus.execute(
            SaveApplicationAnswersCommand(
                application_id=application_id,
                answers=answers
            )
        )

    def get_enabled_questions(
        self,
        position_id: str
    ) -> EnabledQuestionsListResponse:
        """Get all enabled questions for a job position (for public form)."""
        result: EnabledQuestionsListDto = self.query_bus.query(
            GetEnabledQuestionsForPositionQuery(position_id=position_id)
        )
        return ApplicationAnswerMapper.enabled_questions_to_response(result)
