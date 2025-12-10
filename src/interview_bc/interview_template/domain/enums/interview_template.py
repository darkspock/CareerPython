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


class InterviewTemplateScopeEnum(str, Enum):
    """Enum for interview template scope - where the template can be used"""
    PIPELINE = "PIPELINE"  # Used in candidate pipeline (phase-level interviews)
    APPLICATION = "APPLICATION"  # Used for job application screening
    STANDALONE = "STANDALONE"  # Standalone interview, not tied to pipeline or application