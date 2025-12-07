"""Mapper for Application Answer DTOs to Response schemas."""
from src.company_bc.candidate_application.application.queries.question_answer.application_answer_dto import (
    ApplicationAnswerDto,
    ApplicationAnswerListDto
)
from src.company_bc.job_position.application.queries.position_question_config.get_enabled_questions_for_position_query import (
    EnabledQuestionDto,
    EnabledQuestionsListDto
)
from adapters.http.candidate_app.application_answers.schemas.application_answer_schemas import (
    ApplicationAnswerResponse,
    ApplicationAnswerListResponse,
    EnabledQuestionResponse,
    EnabledQuestionsListResponse
)


class ApplicationAnswerMapper:
    """Mapper for ApplicationAnswer DTO to Response schema."""

    @staticmethod
    def dto_to_response(dto: ApplicationAnswerDto) -> ApplicationAnswerResponse:
        """Convert DTO to response schema."""
        return ApplicationAnswerResponse(
            id=dto.id,
            application_id=dto.application_id,
            question_id=dto.question_id,
            answer_value=dto.answer_value,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def dto_list_to_response(dto: ApplicationAnswerListDto) -> ApplicationAnswerListResponse:
        """Convert DTO list to response schema."""
        return ApplicationAnswerListResponse(
            answers=[ApplicationAnswerMapper.dto_to_response(a) for a in dto.answers],
            total=dto.total
        )

    @staticmethod
    def enabled_question_to_response(dto: EnabledQuestionDto) -> EnabledQuestionResponse:
        """Convert enabled question DTO to response schema."""
        return EnabledQuestionResponse(
            id=dto.id,
            workflow_id=dto.workflow_id,
            field_key=dto.field_key,
            label=dto.label,
            field_type=dto.field_type.value,
            description=dto.description,
            options=dto.options,
            is_required=dto.is_required,
            sort_order=dto.sort_order,
            validation_rules=dto.validation_rules
        )

    @staticmethod
    def enabled_questions_to_response(dto: EnabledQuestionsListDto) -> EnabledQuestionsListResponse:
        """Convert enabled questions list DTO to response schema."""
        return EnabledQuestionsListResponse(
            questions=[ApplicationAnswerMapper.enabled_question_to_response(q) for q in dto.questions],
            total=dto.total,
            position_id=dto.position_id,
            workflow_id=dto.workflow_id
        )
