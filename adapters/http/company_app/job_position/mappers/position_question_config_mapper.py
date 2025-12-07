"""Mapper for Position Question Config DTOs to Response schemas."""
from src.company_bc.job_position.application.dtos.position_question_config_dto import (
    PositionQuestionConfigDto,
    PositionQuestionConfigListDto
)
from adapters.http.company_app.job_position.schemas.position_question_config_schemas import (
    PositionQuestionConfigResponse,
    PositionQuestionConfigListResponse
)


class PositionQuestionConfigMapper:
    """Mapper for PositionQuestionConfig DTO to Response schema."""

    @staticmethod
    def dto_to_response(dto: PositionQuestionConfigDto) -> PositionQuestionConfigResponse:
        """Convert DTO to response schema."""
        return PositionQuestionConfigResponse(
            id=dto.id,
            position_id=dto.position_id,
            question_id=dto.question_id,
            enabled=dto.enabled,
            is_required_override=dto.is_required_override,
            sort_order_override=dto.sort_order_override,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def dto_list_to_response(dto: PositionQuestionConfigListDto) -> PositionQuestionConfigListResponse:
        """Convert DTO list to response schema."""
        return PositionQuestionConfigListResponse(
            configs=[PositionQuestionConfigMapper.dto_to_response(c) for c in dto.configs],
            total=dto.total
        )
