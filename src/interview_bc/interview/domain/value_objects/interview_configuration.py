"""InterviewConfiguration value object - represents interview template configuration for a workflow stage"""
from dataclasses import dataclass
from typing import Any

from src.interview_bc.interview.domain.enums.interview_enums import InterviewModeEnum


@dataclass(frozen=True)
class InterviewConfiguration:
    """Value object representing an interview template configuration with its execution mode
    
    This value object pairs an interview template ID with its execution mode
    (AUTOMATIC or MANUAL) to define how interviews should be handled in a workflow stage.
    """
    template_id: str
    mode: InterviewModeEnum

    def __post_init__(self) -> None:
        """Validate the interview configuration"""
        if not self.template_id:
            raise ValueError("Template ID cannot be empty")
        if not isinstance(self.mode, InterviewModeEnum):
            raise ValueError(f"Mode must be an InterviewModeEnum, got {type(self.mode)}")

    @classmethod
    def create(
        cls,
        template_id: str,
        mode: InterviewModeEnum
    ) -> "InterviewConfiguration":
        """Factory method to create a new interview configuration"""
        if not template_id:
            raise ValueError("Template ID cannot be empty")
        if not isinstance(mode, InterviewModeEnum):
            raise ValueError(f"Mode must be an InterviewModeEnum, got {type(mode)}")
        
        return cls(
            template_id=template_id,
            mode=mode
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InterviewConfiguration":
        """Create from dictionary representation"""
        if "template_id" not in data:
            raise ValueError("Dictionary must contain 'template_id' key")
        if "mode" not in data:
            raise ValueError("Dictionary must contain 'mode' key")
        
        mode_value = data["mode"]
        if isinstance(mode_value, str):
            mode = InterviewModeEnum(mode_value)
        elif isinstance(mode_value, InterviewModeEnum):
            mode = mode_value
        else:
            raise ValueError(f"Mode must be a string or InterviewModeEnum, got {type(mode_value)}")
        
        return cls(
            template_id=str(data["template_id"]),
            mode=mode
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "template_id": self.template_id,
            "mode": self.mode.value
        }

    def __eq__(self, other: Any) -> bool:
        """Compare two interview configurations"""
        if not isinstance(other, InterviewConfiguration):
            return False
        return self.template_id == other.template_id and self.mode == other.mode

    def __hash__(self) -> int:
        """Hash for use in sets and dictionaries"""
        return hash((self.template_id, self.mode.value))

