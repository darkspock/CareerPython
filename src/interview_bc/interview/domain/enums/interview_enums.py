from enum import Enum


class InterviewStatusEnum(Enum):
    ENABLED = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    DISCARDED = "DISCARDED"
    PAUSED = "PAUSED"


class InterviewProcessTypeEnum(str, Enum):
    """Enum for the moment in the candidate selection process when the interview is conducted"""
    CANDIDATE_SIGN_UP = "CANDIDATE_SIGN_UP"
    CANDIDATE_APPLICATION = "CANDIDATE_APPLICATION"
    SCREENING = "SCREENING"
    INTERVIEW = "INTERVIEW"
    FEEDBACK = "FEEDBACK"  # Final feedback


class InterviewTypeEnum(str, Enum):
    """Enum for the type/category of interview"""
    CUSTOM = "CUSTOM"
    TECHNICAL = "TECHNICAL"
    BEHAVIORAL = "BEHAVIORAL"
    CULTURAL_FIT = "CULTURAL_FIT"
    KNOWLEDGE_CHECK = "KNOWLEDGE_CHECK"
    EXPERIENCE_CHECK = "EXPERIENCE_CHECK"


class InterviewModeEnum(str, Enum):
    """Enum for interview execution mode"""
    AUTOMATIC = "AUTOMATIC"  # Interview is automatically created/scheduled
    AI = "AI"  # Interview is automatically created/scheduled
    MANUAL = "MANUAL"  # Interview must be manually created/scheduled
