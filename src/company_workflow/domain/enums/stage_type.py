from enum import Enum


class StageType(str, Enum):
    """Type of workflow stage"""
    INITIAL = "initial"  # First stage of the workflow
    INTERMEDIATE = "intermediate"  # Middle stage
    FINAL = "final"  # Last stage (hired/rejected)
    CUSTOM = "custom"  # Custom stage defined by company
