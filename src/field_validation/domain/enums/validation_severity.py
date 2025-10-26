from enum import Enum


class ValidationSeverity(str, Enum):
    """Severity level of validation results."""

    # Warning - allow proceeding with acknowledgment
    WARNING = "warning"

    # Error - block proceeding
    ERROR = "error"
