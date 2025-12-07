from dataclasses import dataclass

from src.framework.application.query_bus import Query, QueryHandler
from src.company_bc.candidate_application.domain.repositories.application_question_answer_repository_interface import (
    ApplicationQuestionAnswerRepositoryInterface
)
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import (
    CandidateApplicationId
)
from src.company_bc.candidate_application.application.queries.question_answer.application_answer_dto import (
    ApplicationAnswerListDto,
    ApplicationAnswerDtoMapper
)


@dataclass
class ListApplicationAnswersQuery(Query):
    """Query to list all question answers for an application."""
    application_id: str


class ListApplicationAnswersQueryHandler(
    QueryHandler[ListApplicationAnswersQuery, ApplicationAnswerListDto]
):
    """Handler for ListApplicationAnswersQuery."""

    def __init__(self, repository: ApplicationQuestionAnswerRepositoryInterface):
        self.repository = repository

    def handle(self, query: ListApplicationAnswersQuery) -> ApplicationAnswerListDto:
        """Handle the query - returns list of answers for the application."""
        application_id = CandidateApplicationId(query.application_id)

        answers = self.repository.list_by_application(application_id)

        return ApplicationAnswerDtoMapper.to_dto_list(answers)
