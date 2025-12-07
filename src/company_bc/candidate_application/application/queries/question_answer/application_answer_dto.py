from dataclasses import dataclass
from datetime import datetime
from typing import Any, List

from src.company_bc.candidate_application.domain.entities.application_question_answer import (
    ApplicationQuestionAnswer
)


@dataclass(frozen=True)
class ApplicationAnswerDto:
    """DTO for application question answer."""
    id: str
    application_id: str
    question_id: str
    answer_value: Any
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ApplicationAnswerListDto:
    """DTO for list of application answers."""
    answers: List[ApplicationAnswerDto]
    total: int


class ApplicationAnswerDtoMapper:
    """Mapper for ApplicationQuestionAnswer entity to DTO."""

    @staticmethod
    def to_dto(entity: ApplicationQuestionAnswer) -> ApplicationAnswerDto:
        """Convert entity to DTO."""
        return ApplicationAnswerDto(
            id=str(entity.id.value),
            application_id=str(entity.application_id.value),
            question_id=str(entity.question_id.value),
            answer_value=entity.answer_value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_dto_list(entities: List[ApplicationQuestionAnswer]) -> ApplicationAnswerListDto:
        """Convert list of entities to DTO."""
        return ApplicationAnswerListDto(
            answers=[ApplicationAnswerDtoMapper.to_dto(e) for e in entities],
            total=len(entities)
        )
