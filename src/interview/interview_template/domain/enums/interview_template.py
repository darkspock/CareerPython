from enum import Enum


class InterviewTemplateStatusEnum(Enum):
    ENABLED = "ENABLED"
    DRAFT = "DRAFT"
    DISABLED = "DISABLED"


class InterviewTemplateTypeEnum(Enum):
    EXTENDED_PROFILE = "EXTENDED_PROFILE"
    POSITION_INTERVIEW = "POSITION_INTERVIEW"


class InterviewTemplateSectionEnum(Enum):
    EXPERIENCE = "EXPERIENCE"
    EDUCATION = "EDUCATION"
    PROJECT = "PROJECT"
    SOFT_SKILL = "SOFT_SKILL"
    GENERAL = "GENERAL"
