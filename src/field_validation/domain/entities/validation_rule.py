from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any, Dict

from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from ..enums.comparison_operator import ComparisonOperator
from ..enums.validation_rule_type import ValidationRuleType
from ..enums.validation_severity import ValidationSeverity
from ..value_objects.validation_result import ValidationResult
from ..value_objects.validation_rule_id import ValidationRuleId


@dataclass(frozen=True)
class ValidationRule:
    """Validation rule entity - defines validation logic for custom fields."""

    id: ValidationRuleId
    custom_field_id: CustomFieldId
    stage_id: WorkflowStageId
    rule_type: ValidationRuleType
    comparison_operator: ComparisonOperator
    position_field_path: Optional[str]  # e.g., "salary.max", "location.city"
    comparison_value: Optional[Any]  # Static comparison value (for non-position comparisons)
    severity: ValidationSeverity
    validation_message: str  # Supports variables: {field_name}, {candidate_value}, {position_value}
    auto_reject: bool
    rejection_reason: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
            id: ValidationRuleId,
            custom_field_id: CustomFieldId,
            stage_id: WorkflowStageId,
            rule_type: ValidationRuleType,
            comparison_operator: ComparisonOperator,
            severity: ValidationSeverity,
            validation_message: str,
            position_field_path: Optional[str] = None,
            comparison_value: Optional[Any] = None,
            auto_reject: bool = False,
            rejection_reason: Optional[str] = None,
            is_active: bool = True
    ) -> "ValidationRule":
        """Factory method to create a new validation rule."""
        # Validation
        if not validation_message:
            raise ValueError("Validation message cannot be empty")

        if rule_type == ValidationRuleType.COMPARE_POSITION_FIELD and not position_field_path:
            raise ValueError("Position field path is required for COMPARE_POSITION_FIELD rule type")

        if rule_type in [ValidationRuleType.RANGE, ValidationRuleType.PATTERN, ValidationRuleType.CUSTOM]:
            if comparison_value is None:
                raise ValueError(f"Comparison value is required for {rule_type.value} rule type")

        if auto_reject and not rejection_reason:
            raise ValueError("Rejection reason is required when auto_reject is enabled")

        if auto_reject and severity != ValidationSeverity.ERROR:
            raise ValueError("Auto-reject can only be enabled for ERROR severity")

        now = datetime.utcnow()
        return ValidationRule(
            id=id,
            custom_field_id=custom_field_id,
            stage_id=stage_id,
            rule_type=rule_type,
            comparison_operator=comparison_operator,
            position_field_path=position_field_path,
            comparison_value=comparison_value,
            severity=severity,
            validation_message=validation_message,
            auto_reject=auto_reject,
            rejection_reason=rejection_reason,
            is_active=is_active,
            created_at=now,
            updated_at=now
        )

    def update(
            self,
            comparison_operator: ComparisonOperator,
            severity: ValidationSeverity,
            validation_message: str,
            position_field_path: Optional[str] = None,
            comparison_value: Optional[Any] = None,
            auto_reject: bool = False,
            rejection_reason: Optional[str] = None,
            is_active: bool = True
    ) -> "ValidationRule":
        """Update validation rule."""
        if not validation_message:
            raise ValueError("Validation message cannot be empty")

        if auto_reject and not rejection_reason:
            raise ValueError("Rejection reason is required when auto_reject is enabled")

        if auto_reject and severity != ValidationSeverity.ERROR:
            raise ValueError("Auto-reject can only be enabled for ERROR severity")

        return ValidationRule(
            id=self.id,
            custom_field_id=self.custom_field_id,
            stage_id=self.stage_id,
            rule_type=self.rule_type,
            comparison_operator=comparison_operator,
            position_field_path=position_field_path,
            comparison_value=comparison_value,
            severity=severity,
            validation_message=validation_message,
            auto_reject=auto_reject,
            rejection_reason=rejection_reason,
            is_active=is_active,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def activate(self) -> "ValidationRule":
        """Activate validation rule."""
        return ValidationRule(
            id=self.id,
            custom_field_id=self.custom_field_id,
            stage_id=self.stage_id,
            rule_type=self.rule_type,
            comparison_operator=self.comparison_operator,
            position_field_path=self.position_field_path,
            comparison_value=self.comparison_value,
            severity=self.severity,
            validation_message=self.validation_message,
            auto_reject=self.auto_reject,
            rejection_reason=self.rejection_reason,
            is_active=True,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def deactivate(self) -> "ValidationRule":
        """Deactivate validation rule."""
        return ValidationRule(
            id=self.id,
            custom_field_id=self.custom_field_id,
            stage_id=self.stage_id,
            rule_type=self.rule_type,
            comparison_operator=self.comparison_operator,
            position_field_path=self.position_field_path,
            comparison_value=self.comparison_value,
            severity=self.severity,
            validation_message=self.validation_message,
            auto_reject=self.auto_reject,
            rejection_reason=self.rejection_reason,
            is_active=False,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def evaluate(
            self,
            field_name: str,
            candidate_value: Any,
            position: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Evaluate the validation rule against a candidate's field value.

        Args:
            field_name: Display name of the field
            candidate_value: The candidate's value for this field
            position: Position data (if rule type is COMPARE_POSITION_FIELD)

        Returns:
            ValidationResult
        """
        if not self.is_active:
            return ValidationResult.passed()

        # Get comparison target value
        comparison_target = self._get_comparison_target(position)

        # Perform comparison
        is_valid = self._perform_comparison(candidate_value, comparison_target)

        # If validation passed, return success
        if is_valid:
            return ValidationResult.passed()

        # Build message with variable substitution
        message = self._build_message(field_name, candidate_value, comparison_target)

        # Return result based on severity
        if self.severity == ValidationSeverity.ERROR:
            return ValidationResult.error(
                field_key=str(self.custom_field_id),
                rule_id=str(self.id),
                message=message,
                auto_reject=self.auto_reject,
                rejection_reason=self.rejection_reason
            )
        else:
            return ValidationResult.warning(
                field_key=str(self.custom_field_id),
                rule_id=str(self.id),
                message=message
            )

    def _get_comparison_target(self, position: Optional[Dict[str, Any]]) -> Any:
        """Get the target value for comparison."""
        if self.rule_type == ValidationRuleType.COMPARE_POSITION_FIELD:
            if not position or not self.position_field_path:
                return None
            return self._get_nested_value(position, self.position_field_path)
        else:
            return self.comparison_value

    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get nested value from dict using dot notation path."""
        keys = path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value

    def _perform_comparison(self, candidate_value: Any, comparison_target: Any) -> bool:
        """Perform the comparison operation."""
        # Handle None values
        if candidate_value is None or comparison_target is None:
            is_neq_op: bool = self.comparison_operator == ComparisonOperator.NEQ
            return is_neq_op

        try:
            if self.comparison_operator == ComparisonOperator.GT:
                result: bool = float(candidate_value) > float(comparison_target)
                return result

            elif self.comparison_operator == ComparisonOperator.GTE:
                result = float(candidate_value) >= float(comparison_target)
                return result

            elif self.comparison_operator == ComparisonOperator.LT:
                result = float(candidate_value) < float(comparison_target)
                return result

            elif self.comparison_operator == ComparisonOperator.LTE:
                result = float(candidate_value) <= float(comparison_target)
                return result

            elif self.comparison_operator == ComparisonOperator.EQ:
                result = bool(candidate_value == comparison_target)
                return result

            elif self.comparison_operator == ComparisonOperator.NEQ:
                result = bool(candidate_value != comparison_target)
                return result

            elif self.comparison_operator == ComparisonOperator.IN_RANGE:
                if isinstance(comparison_target, dict):
                    min_val = comparison_target.get('min')
                    max_val = comparison_target.get('max')
                    if min_val is not None and max_val is not None:
                        result = float(min_val) <= float(candidate_value) <= float(max_val)
                        return result
                return False

            elif self.comparison_operator == ComparisonOperator.OUT_RANGE:
                if isinstance(comparison_target, dict):
                    min_val = comparison_target.get('min')
                    max_val = comparison_target.get('max')
                    if min_val is not None and max_val is not None:
                        result = not (float(min_val) <= float(candidate_value) <= float(max_val))
                        return result
                return False

            elif self.comparison_operator == ComparisonOperator.CONTAINS:
                result = bool(str(comparison_target) in str(candidate_value))
                return result

            elif self.comparison_operator == ComparisonOperator.NOT_CONTAINS:
                result = bool(str(comparison_target) not in str(candidate_value))
                return result

            # Default case - should not reach here
            return False  # type: ignore[unreachable]

        except (ValueError, TypeError):
            # If comparison fails (e.g., non-numeric values for numeric comparison), treat as invalid
            return False

    def _build_message(
            self,
            field_name: str,
            candidate_value: Any,
            comparison_target: Any
    ) -> str:
        """Build validation message with variable substitution."""
        message = self.validation_message

        # Replace variables
        message = message.replace('{field_name}', str(field_name))
        message = message.replace('{candidate_value}', str(candidate_value) if candidate_value is not None else 'N/A')
        message = message.replace('{position_value}',
                                  str(comparison_target) if comparison_target is not None else 'N/A')
        message = message.replace('{comparison_value}',
                                  str(comparison_target) if comparison_target is not None else 'N/A')

        return message
