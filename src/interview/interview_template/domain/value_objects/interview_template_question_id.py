from dataclasses import dataclass
from typing import Any

import ulid

from src.shared.domain.value_objects.base_id import BaseId


@dataclass(frozen=True)
class InterviewTemplateQuestionId(BaseId):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("InterviewTemplateQuestionId cannot be empty")

    @classmethod
    def generate(cls) -> 'InterviewTemplateQuestionId':
        """Generate a new InterviewTemplateQuestionId using ULID"""
        return cls(ulid.new().str)

    @classmethod
    def from_string(cls, id_str: str) -> 'InterviewTemplateQuestionId':
        """Create InterviewTemplateQuestionId from string"""
        if not id_str:
            raise ValueError("ID string cannot be empty")
        return cls(id_str)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, InterviewTemplateQuestionId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
