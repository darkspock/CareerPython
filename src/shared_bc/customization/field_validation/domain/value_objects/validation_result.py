from dataclasses import dataclass
from typing import Optional
from ..enums.validation_severity import ValidationSeverity


@dataclass(frozen=True)
class ValidationResult:
    """Result of a validation rule evaluation."""

    is_valid: bool
    severity: ValidationSeverity
    message: str
    field_key: str
    rule_id: str
    should_auto_reject: bool = False
    rejection_reason: Optional[str] = None

    @staticmethod
    def passed() -> "ValidationResult":
        """Create a passed validation result."""
        return ValidationResult(
            is_valid=True,
            severity=ValidationSeverity.WARNING,
            message="Validation passed",
            field_key="",
            rule_id=""
        )

    @staticmethod
    def warning(
        field_key: str,
        rule_id: str,
        message: str
    ) -> "ValidationResult":
        """Create a warning validation result."""
        return ValidationResult(
            is_valid=False,
            severity=ValidationSeverity.WARNING,
            message=message,
            field_key=field_key,
            rule_id=rule_id
        )

    @staticmethod
    def error(
        field_key: str,
        rule_id: str,
        message: str,
        auto_reject: bool = False,
        rejection_reason: Optional[str] = None
    ) -> "ValidationResult":
        """Create an error validation result."""
        return ValidationResult(
            is_valid=False,
            severity=ValidationSeverity.ERROR,
            message=message,
            field_key=field_key,
            rule_id=rule_id,
            should_auto_reject=auto_reject,
            rejection_reason=rejection_reason
        )

    def is_error(self) -> bool:
        """Check if this is an error result."""
        return not self.is_valid and self.severity == ValidationSeverity.ERROR

    def is_warning(self) -> bool:
        """Check if this is a warning result."""
        return not self.is_valid and self.severity == ValidationSeverity.WARNING
