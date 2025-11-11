from enum import Enum


class InterviewStatusEnum(Enum):
    ENABLED = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    DISCARDED = "DISCARDED"
    PAUSED = "PAUSED"


class InterviewTypeEnum(Enum):
    JOB_POSITION = "JOB_POSITION"
    PLATFORM_ONBOARDING = "PLATFORM_ONBOARDING"
    COMPANY_ONBOARDING = "COMPANY_ONBOARDING"
    PREMIUM_ONBOARDING = "PREMIUM_ONBOARDING"
    CUSTOM = "CUSTOM"


class InterviewModeEnum(str, Enum):
    """Enum for interview execution mode"""
    AUTOMATIC = "AUTOMATIC"  # Interview is automatically created/scheduled
    MANUAL = "MANUAL"  # Interview must be manually created/scheduled
