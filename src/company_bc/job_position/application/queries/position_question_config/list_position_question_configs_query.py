from dataclasses import dataclass

from src.framework.application.query_bus import Query, QueryHandler
from src.company_bc.job_position.domain.repositories.position_question_config_repository_interface import (
    PositionQuestionConfigRepositoryInterface
)
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.application.dtos.position_question_config_dto import (
    PositionQuestionConfigListDto,
    PositionQuestionConfigDtoMapper
)


@dataclass
class ListPositionQuestionConfigsQuery(Query):
    """Query to list all question configs for a position."""
    position_id: str
    enabled_only: bool = False


class ListPositionQuestionConfigsQueryHandler(
    QueryHandler[ListPositionQuestionConfigsQuery, PositionQuestionConfigListDto]
):
    """Handler for ListPositionQuestionConfigsQuery."""

    def __init__(self, repository: PositionQuestionConfigRepositoryInterface):
        self.repository = repository

    def handle(self, query: ListPositionQuestionConfigsQuery) -> PositionQuestionConfigListDto:
        """Handle the query - returns list of configs for the position."""
        position_id = JobPositionId(query.position_id)

        configs = self.repository.list_by_position(
            position_id=position_id,
            enabled_only=query.enabled_only
        )

        return PositionQuestionConfigDtoMapper.to_dto_list(configs)
