from enum import Enum


class InterviewTemplateStatusEnum(Enum):
    ENABLED = "ENABLED"
    DRAFT = "DRAFT"
    DISABLED = "DISABLED"


class InterviewTemplateTypeEnum(Enum):
    EXTENDED_PROFILE = "EXTENDED_PROFILE"
    POSITION_INTERVIEW = "POSITION_INTERVIEW"
    SCREENING = "SCREENING"
    CUSTOM = "CUSTOM"


class InterviewTemplateSectionEnum(Enum):
    EXPERIENCE = "EXPERIENCE"
    EDUCATION = "EDUCATION"
    PROJECT = "PROJECT"
    SOFT_SKILL = "SOFT_SKILL"
    GENERAL = "GENERAL"


class ScoringModeEnum(str, Enum):
    """Enum for interview template scoring mode"""
    DISTANCE = "DISTANCE"  # Better when closer to requirements
    ABSOLUTE = "ABSOLUTE"  # Better when higher score
