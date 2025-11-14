from enum import Enum


class InterviewTemplateQuestionStatusEnum(Enum):
    ENABLED = "ENABLED"
    DRAFT = "DRAFT"
    DISABLED = "DISABLED"


class InterviewTemplateQuestionDataTypeEnum(Enum):
    INT = "int"
    DATE = "date"
    SHORT_STRING = "short_string"
    LARGE_STRING = "large_string"
    SCORING = "scoring"


class InterviewTemplateQuestionScopeEnum(Enum):
    GLOBAL = "global"
    ITEM = "item"
