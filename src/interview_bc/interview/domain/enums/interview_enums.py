from enum import Enum


class InterviewStatusEnum(Enum):
    ENABLED = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    DISCARDED = "DISCARDED"
    PAUSED = "PAUSED"


class InterviewTypeEnum(Enum):
    EXTENDED_PROFILE = "EXTENDED_PROFILE"
    POSITION_INTERVIEW = "POSITION_INTERVIEW"
    CUSTOM = "CUSTOM"
    TECHNICAL = "TECHNICAL"
    BEHAVIORAL = "BEHAVIORAL"
    CULTURAL_FIT = "CULTURAL_FIT"
    # Legacy values - kept for backward compatibility, deprecated
    JOB_POSITION = "JOB_POSITION"  # Deprecated: use POSITION_INTERVIEW
    PLATFORM_ONBOARDING = "PLATFORM_ONBOARDING"  # Deprecated
    COMPANY_ONBOARDING = "COMPANY_ONBOARDING"  # Deprecated
    PREMIUM_ONBOARDING = "PREMIUM_ONBOARDING"  # Deprecated


class InterviewModeEnum(str, Enum):
    """Enum for interview execution mode"""
    AUTOMATIC = "AUTOMATIC"  # Interview is automatically created/scheduled
    AI = "AI"  # Interview is automatically created/scheduled
    MANUAL = "MANUAL"  # Interview must be manually created/scheduled
