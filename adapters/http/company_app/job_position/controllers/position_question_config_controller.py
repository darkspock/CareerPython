"""Controller for Position Question Config operations."""
from src.framework.application.query_bus import QueryBus
from src.framework.application.command_bus import CommandBus
from src.company_bc.job_position.application.queries.position_question_config.list_position_question_configs_query import (
    ListPositionQuestionConfigsQuery
)
from src.company_bc.job_position.application.commands.position_question_config.configure_position_question_command import (
    ConfigurePositionQuestionCommand
)
from src.company_bc.job_position.application.commands.position_question_config.remove_position_question_config_command import (
    RemovePositionQuestionConfigCommand
)
from src.company_bc.job_position.application.dtos.position_question_config_dto import (
    PositionQuestionConfigListDto
)
from adapters.http.company_app.job_position.schemas.position_question_config_schemas import (
    ConfigurePositionQuestionRequest,
    PositionQuestionConfigListResponse
)
from adapters.http.company_app.job_position.mappers.position_question_config_mapper import (
    PositionQuestionConfigMapper
)


class PositionQuestionConfigController:
    """Controller for position question config operations."""

    def __init__(self, query_bus: QueryBus, command_bus: CommandBus):
        self.query_bus = query_bus
        self.command_bus = command_bus

    def list_configs(
        self,
        position_id: str,
        enabled_only: bool = False
    ) -> PositionQuestionConfigListResponse:
        """List all question configs for a position."""
        result: PositionQuestionConfigListDto = self.query_bus.query(
            ListPositionQuestionConfigsQuery(
                position_id=position_id,
                enabled_only=enabled_only
            )
        )
        return PositionQuestionConfigMapper.dto_list_to_response(result)

    def configure_question(
        self,
        position_id: str,
        request: ConfigurePositionQuestionRequest
    ) -> None:
        """Configure a question for a position (create or update)."""
        self.command_bus.execute(
            ConfigurePositionQuestionCommand(
                position_id=position_id,
                question_id=request.question_id,
                enabled=request.enabled,
                is_required_override=request.is_required_override,
                sort_order_override=request.sort_order_override
            )
        )

    def remove_config(
        self,
        position_id: str,
        question_id: str
    ) -> None:
        """Remove a question config from a position."""
        self.command_bus.execute(
            RemovePositionQuestionConfigCommand(
                position_id=position_id,
                question_id=question_id
            )
        )
