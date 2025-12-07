from typing import List

from adapters.http.company_app.application_question.schemas.application_question_schemas import (
    ApplicationQuestionResponse,
    ApplicationQuestionListResponse
)
from src.shared_bc.customization.workflow.application.dtos.application_question_dto import (
    ApplicationQuestionDto,
    ApplicationQuestionListDto
)


class ApplicationQuestionMapper:
    """Mapper for converting ApplicationQuestion DTOs to response schemas."""

    @staticmethod
    def dto_to_response(dto: ApplicationQuestionDto) -> ApplicationQuestionResponse:
        """Convert ApplicationQuestionDto to ApplicationQuestionResponse."""
        return ApplicationQuestionResponse(
            id=dto.id,
            workflow_id=dto.workflow_id,
            company_id=dto.company_id,
            field_key=dto.field_key,
            label=dto.label,
            description=dto.description,
            field_type=dto.field_type.value,
            options=dto.options,
            is_required_default=dto.is_required_default,
            validation_rules=dto.validation_rules,
            sort_order=dto.sort_order,
            is_active=dto.is_active,
            created_at=dto.created_at.isoformat(),
            updated_at=dto.updated_at.isoformat()
        )

    @staticmethod
    def dto_list_to_response(dto: ApplicationQuestionListDto) -> ApplicationQuestionListResponse:
        """Convert ApplicationQuestionListDto to ApplicationQuestionListResponse."""
        return ApplicationQuestionListResponse(
            questions=[ApplicationQuestionMapper.dto_to_response(q) for q in dto.questions],
            total_count=dto.total_count
        )
