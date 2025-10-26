from enum import Enum


class ValidationRuleType(str, Enum):
    """Type of validation rule."""

    # Compare candidate field value with position field value
    COMPARE_POSITION_FIELD = "compare_position_field"

    # Value must be within a range
    RANGE = "range"

    # Value must match a pattern (regex)
    PATTERN = "pattern"

    # Custom validation logic
    CUSTOM = "custom"
