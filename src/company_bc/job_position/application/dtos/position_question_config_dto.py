from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.company_bc.job_position.domain.entities.position_question_config import (
    PositionQuestionConfig
)


@dataclass(frozen=True)
class PositionQuestionConfigDto:
    """DTO for position question config."""
    id: str
    position_id: str
    question_id: str
    enabled: bool
    is_required_override: Optional[bool]
    sort_order_override: Optional[int]
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class PositionQuestionConfigListDto:
    """DTO for list of position question configs."""
    configs: List[PositionQuestionConfigDto]
    total: int


class PositionQuestionConfigDtoMapper:
    """Mapper for PositionQuestionConfig entity to DTO."""

    @staticmethod
    def to_dto(entity: PositionQuestionConfig) -> PositionQuestionConfigDto:
        """Convert entity to DTO."""
        return PositionQuestionConfigDto(
            id=str(entity.id.value),
            position_id=str(entity.position_id.value),
            question_id=str(entity.question_id.value),
            enabled=entity.enabled,
            is_required_override=entity.is_required_override,
            sort_order_override=entity.sort_order_override,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_dto_list(entities: List[PositionQuestionConfig]) -> PositionQuestionConfigListDto:
        """Convert list of entities to DTO."""
        return PositionQuestionConfigListDto(
            configs=[PositionQuestionConfigDtoMapper.to_dto(e) for e in entities],
            total=len(entities)
        )
