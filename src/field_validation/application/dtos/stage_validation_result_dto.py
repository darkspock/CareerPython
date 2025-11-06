from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ValidationIssueDto:
    """Individual validation issue."""

    field_key: str
    field_name: str
    message: str
    severity: str  # 'error' or 'warning'
    rule_id: str
    should_auto_reject: bool = False
    rejection_reason: str | None = None


@dataclass(frozen=True)
class StageValidationResultDto:
    """Aggregated validation result for a stage transition."""

    is_valid: bool
    has_errors: bool
    has_warnings: bool
    errors: List[ValidationIssueDto]
    warnings: List[ValidationIssueDto]
    should_auto_reject: bool
    auto_reject_reason: str | None

    @staticmethod
    def success() -> "StageValidationResultDto":
        """Create a successful validation result."""
        return StageValidationResultDto(
            is_valid=True,
            has_errors=False,
            has_warnings=False,
            errors=[],
            warnings=[],
            should_auto_reject=False,
            auto_reject_reason=None
        )

    @staticmethod
    def with_issues(
            errors: List[ValidationIssueDto],
            warnings: List[ValidationIssueDto]
    ) -> "StageValidationResultDto":
        """Create validation result with issues."""
        # Check if any error triggers auto-reject
        auto_reject = any(e.should_auto_reject for e in errors)
        auto_reject_reason = None
        if auto_reject:
            # Get the first auto-reject reason
            for error in errors:
                if error.should_auto_reject and error.rejection_reason:
                    auto_reject_reason = error.rejection_reason
                    break

        return StageValidationResultDto(
            is_valid=len(errors) == 0,
            has_errors=len(errors) > 0,
            has_warnings=len(warnings) > 0,
            errors=errors,
            warnings=warnings,
            should_auto_reject=auto_reject,
            auto_reject_reason=auto_reject_reason
        )

    def allows_transition(self) -> bool:
        """Check if transition is allowed (no errors)."""
        return not self.has_errors

    def blocks_transition(self) -> bool:
        """Check if transition is blocked (has errors)."""
        return self.has_errors
