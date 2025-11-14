from enum import Enum


class ComparisonOperator(str, Enum):
    """Comparison operators for validation rules."""

    # Greater than
    GT = "gt"

    # Greater than or equal
    GTE = "gte"

    # Less than
    LT = "lt"

    # Less than or equal
    LTE = "lte"

    # Equal
    EQ = "eq"

    # Not equal
    NEQ = "neq"

    # In range (requires min and max values)
    IN_RANGE = "in_range"

    # Out of range (requires min and max values)
    OUT_RANGE = "out_range"

    # Contains (for strings or arrays)
    CONTAINS = "contains"

    # Not contains (for strings or arrays)
    NOT_CONTAINS = "not_contains"
