from src.shared_bc.customization.field_validation.application.dtos.validation_rule_dto import ValidationRuleDto
from src.shared_bc.customization.field_validation.application.dtos.stage_validation_result_dto import StageValidationResultDto, ValidationIssueDto
from src.shared_bc.customization.field_validation.presentation.schemas.validation_rule_response import ValidationRuleResponse
from src.shared_bc.customization.field_validation.presentation.schemas.validation_result_response import ValidationResultResponse, ValidationIssueResponse


class ValidationRuleResponseMapper:
    """Mapper for ValidationRule DTO to Response schema."""

    @staticmethod
    def dto_to_response(dto: ValidationRuleDto) -> ValidationRuleResponse:
        """Convert DTO to response schema."""
        return ValidationRuleResponse(
            id=dto.id,
            custom_field_id=dto.custom_field_id,
            stage_id=dto.stage_id,
            rule_type=dto.rule_type,
            comparison_operator=dto.comparison_operator,
            position_field_path=dto.position_field_path,
            comparison_value=dto.comparison_value,
            severity=dto.severity,
            validation_message=dto.validation_message,
            auto_reject=dto.auto_reject,
            rejection_reason=dto.rejection_reason,
            is_active=dto.is_active,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )


class ValidationResultResponseMapper:
    """Mapper for StageValidationResult DTO to Response schema."""

    @staticmethod
    def dto_to_response(dto: StageValidationResultDto) -> ValidationResultResponse:
        """Convert DTO to response schema."""
        return ValidationResultResponse(
            is_valid=dto.is_valid,
            has_errors=dto.has_errors,
            has_warnings=dto.has_warnings,
            errors=[ValidationResultResponseMapper._issue_dto_to_response(e) for e in dto.errors],
            warnings=[ValidationResultResponseMapper._issue_dto_to_response(w) for w in dto.warnings],
            should_auto_reject=dto.should_auto_reject,
            auto_reject_reason=dto.auto_reject_reason
        )

    @staticmethod
    def _issue_dto_to_response(dto: ValidationIssueDto) -> ValidationIssueResponse:
        """Convert ValidationIssueDto to response schema."""
        return ValidationIssueResponse(
            field_key=dto.field_key,
            field_name=dto.field_name,
            message=dto.message,
            severity=dto.severity,
            rule_id=dto.rule_id,
            should_auto_reject=dto.should_auto_reject,
            rejection_reason=dto.rejection_reason
        )
