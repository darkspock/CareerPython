from typing import List

from src.shared_bc.customization.workflow.application.dtos.application_question_dto import (
    ApplicationQuestionDto,
    ApplicationQuestionListDto
)
from src.shared_bc.customization.workflow.domain.entities.application_question import (
    ApplicationQuestion
)


class ApplicationQuestionDtoMapper:
    """Mapper for converting ApplicationQuestion entities to DTOs."""

    @staticmethod
    def to_dto(entity: ApplicationQuestion) -> ApplicationQuestionDto:
        """Convert ApplicationQuestion entity to DTO."""
        return ApplicationQuestionDto(
            id=str(entity.id.value),
            workflow_id=str(entity.workflow_id.value),
            company_id=str(entity.company_id.value),
            field_key=entity.field_key,
            label=entity.label,
            description=entity.description,
            field_type=entity.field_type,
            options=entity.options,
            is_required_default=entity.is_required_default,
            validation_rules=entity.validation_rules,
            sort_order=entity.sort_order,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_dto_list(entities: List[ApplicationQuestion]) -> ApplicationQuestionListDto:
        """Convert list of ApplicationQuestion entities to DTO list."""
        return ApplicationQuestionListDto(
            questions=[ApplicationQuestionDtoMapper.to_dto(e) for e in entities],
            total_count=len(entities)
        )
