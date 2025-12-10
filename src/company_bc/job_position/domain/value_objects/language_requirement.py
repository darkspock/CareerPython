from dataclasses import dataclass
from typing import List

from src.company_bc.job_position.domain.exceptions.job_position_exceptions import JobPositionValidationError


VALID_LANGUAGE_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2", "Native"]


@dataclass(frozen=True)
class LanguageRequirement:
    """Value object for language requirement"""
    language: str  # e.g., "English", "Spanish", "French"
    level: str     # CEFR level: A1, A2, B1, B2, C1, C2, or Native

    def __post_init__(self) -> None:
        """Validate after initialization"""
        self._validate()

    def _validate(self) -> None:
        """Validate language requirement data"""
        if not self.language or len(self.language.strip()) == 0:
            raise JobPositionValidationError("Language is required")

        if not self.level or self.level not in VALID_LANGUAGE_LEVELS:
            raise JobPositionValidationError(
                f"Invalid language level: {self.level}. "
                f"Must be one of: {', '.join(VALID_LANGUAGE_LEVELS)}"
            )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "language": self.language,
            "level": self.level
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LanguageRequirement":
        """Create from dictionary"""
        return cls(
            language=data.get("language", ""),
            level=data.get("level", "")
        )

    @classmethod
    def from_list(cls, data: List[dict]) -> List["LanguageRequirement"]:
        """Create list of LanguageRequirement from list of dicts"""
        return [cls.from_dict(item) for item in data] if data else []

    @staticmethod
    def to_list(requirements: List["LanguageRequirement"]) -> List[dict]:
        """Convert list of LanguageRequirement to list of dicts"""
        return [req.to_dict() for req in requirements] if requirements else []
