from enum import Enum


class WorkflowTypeEnum(str, Enum):
    """Type of job position workflow"""
    STANDARD = "standard"  # Standard recruitment workflow
    FAST_TRACK = "fast_track"  # Fast-track hiring process
    EXECUTIVE = "executive"  # Executive-level hiring
    INTERNSHIP = "internship"  # Internship program
    TEMPORARY = "temporary"  # Temporary positions

