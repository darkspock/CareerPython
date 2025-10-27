from enum import Enum


class StageType(str, Enum):
    """Type of workflow stage"""
    INITIAL = "initial"  # First stage of the workflow
    STANDARD = "standard"  # Standard middle stage
    SUCCESS = "success"  # Success terminal stage (can trigger phase transition)
    FAIL = "fail"  # Failure terminal stage (can trigger phase transition)
