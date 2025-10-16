from enum import Enum


class LanguageLevelEnum(Enum):
    NONE = "none"
    BASIC = "basic"
    CONVERSATIONAL = "conversational"
    PROFESSIONAL = "professional"


class LanguageEnum(Enum):
    ENGLISH = "english"
    SPANISH = "spanish"
    PORTUGUESE = "portuguese"
    ITALIAN = "italian"
    FRENCH = "french"
    CHINESE = "chinese"
    GERMAN = "german"
    JAPANESE = "japanese"
    RUSSIAN = "russian"
    ARABIC = "arabic"


class CandidateStatusEnum(Enum):
    """Estados posibles de un candidato"""
    DRAFT = "DRAFT"
    COMPLETE = "COMPLETE"
    DELETED = "DELETED"


class CandidateTypeEnum(Enum):
    BASIC = "basic"
    EXTENDED = "extended"
    PREMIUM = "premium"


class PositionRoleEnum(Enum):
    MANAGE_PEOPLE = "manage_people"
    LEAD_INITIATIVES = "lead_initiatives"
    TECHNOLOGY = "technology"
    SALES = "sales"
    FINANCIAL = "financial"
    HR = "hr"
    EXECUTIVE = "executive"
    OPERATIONS = "operations"
    MARKETING = "marketing"
    PRODUCT = "product"
    LEGAL_COMPLIANCE = "legal_compliance"
    CUSTOMER_SUCCESS = "customer_success"


class WorkModalityEnum(Enum):
    REMOTE = "remote"
    ON_SITE = "on_site"
    HYBRID = "hybrid"
