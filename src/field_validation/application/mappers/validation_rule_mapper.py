from src.field_validation.domain.entities.validation_rule import ValidationRule
from src.field_validation.application.dtos.validation_rule_dto import ValidationRuleDto


class ValidationRuleMapper:
    """Mapper for ValidationRule entity to DTO."""

    @staticmethod
    def entity_to_dto(entity: ValidationRule) -> ValidationRuleDto:
        """Convert entity to DTO."""
        return ValidationRuleDto(
            id=str(entity.id),
            custom_field_id=str(entity.custom_field_id),
            stage_id=str(entity.stage_id),
            rule_type=entity.rule_type.value,
            comparison_operator=entity.comparison_operator.value,
            position_field_path=entity.position_field_path,
            comparison_value=entity.comparison_value,
            severity=entity.severity.value,
            validation_message=entity.validation_message,
            auto_reject=entity.auto_reject,
            rejection_reason=entity.rejection_reason,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
