from enum import Enum


class InterviewStatusEnum(Enum):
    PENDING = "PENDING"
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


class InterviewFilterEnum(str, Enum):
    """Enum for interview filter types used in statistics and filtering"""
    PENDING_TO_PLAN = "PENDING_TO_PLAN"  # No scheduled_at or no interviewers
    PLANNED = "PLANNED"  # Has scheduled_at and interviewers
    IN_PROGRESS = "IN_PROGRESS"  # scheduled_at = today
    RECENTLY_FINISHED = "RECENTLY_FINISHED"  # finished_at in last 30 days
    OVERDUE = "OVERDUE"  # deadline_date < now and not finished
    PENDING_FEEDBACK = "PENDING_FEEDBACK"  # finished but no score or feedback
