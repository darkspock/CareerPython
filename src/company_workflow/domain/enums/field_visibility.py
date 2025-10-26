from enum import Enum


class FieldVisibility(str, Enum):
    """Visibility options for custom fields in workflow stages"""
    VISIBLE = "VISIBLE"  # Field is visible and can be edited
    HIDDEN = "HIDDEN"  # Field is not shown in this stage
    READ_ONLY = "READ_ONLY"  # Field is visible but cannot be edited
    REQUIRED = "REQUIRED"  # Field is visible and must be filled
