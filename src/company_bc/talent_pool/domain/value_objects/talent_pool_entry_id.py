"""
Talent Pool Entry ID Value Object
Phase 8: Value object for talent pool entry identifiers
"""

import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class TalentPoolEntryId:
    """Value object representing a talent pool entry ID"""

    value: str

    def __post_init__(self) -> None:
        """Validate the ID format"""
        if not self.value:
            raise ValueError("Talent pool entry ID cannot be empty")
        if not isinstance(self.value, str):
            raise TypeError("Talent pool entry ID must be a string")
        # Validate UUID format
        try:
            uuid.UUID(self.value)
        except ValueError as e:
            raise ValueError(f"Invalid talent pool entry ID format: {self.value}") from e

    @classmethod
    def generate(cls) -> "TalentPoolEntryId":
        """Generate a new talent pool entry ID"""
        return cls(value=str(uuid.uuid4()))

    @classmethod
    def from_string(cls, value: str) -> "TalentPoolEntryId":
        """Create a TalentPoolEntryId from a string"""
        return cls(value=value)

    def __str__(self) -> str:
        """Return string representation"""
        return self.value

    def __repr__(self) -> str:
        """Return detailed representation"""
        return f"TalentPoolEntryId(value='{self.value}')"
