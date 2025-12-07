from enum import Enum


class ApplicationQuestionFieldType(str, Enum):
    """Field types for application questions."""
    TEXT = "TEXT"
    TEXTAREA = "TEXTAREA"
    NUMBER = "NUMBER"
    DATE = "DATE"
    SELECT = "SELECT"
    MULTISELECT = "MULTISELECT"
    BOOLEAN = "BOOLEAN"
