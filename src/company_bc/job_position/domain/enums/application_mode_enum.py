from enum import Enum


class ApplicationModeEnum(str, Enum):
    """
    Defines how candidates apply to a job position.

    SHORT: Minimal application - just email + CV + GDPR consent
    FULL: Complete application - requires filling experience, education, etc.
    CV_BUILDER: Help candidate create CV - guides through structured data entry
    """
    SHORT = "short"
    FULL = "full"
    CV_BUILDER = "cv_builder"
