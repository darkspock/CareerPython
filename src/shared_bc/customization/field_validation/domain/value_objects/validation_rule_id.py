from dataclasses import dataclass
import ulid


@dataclass(frozen=True)
class ValidationRuleId:
    """Value object for validation rule ID."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ValidationRuleId cannot be empty")

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def generate() -> "ValidationRuleId":
        """Generate a new validation rule ID."""
        return ValidationRuleId(str(ulid.new()))

    @staticmethod
    def from_string(value: str) -> "ValidationRuleId":
        """Create from string."""
        return ValidationRuleId(value)
