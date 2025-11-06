from dataclasses import dataclass

import ulid


@dataclass(frozen=True)
class CustomFieldId:
    """Value object for custom field ID"""
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Custom field ID cannot be empty")

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, id_string: str) -> "CustomFieldId":
        """Create from string"""
        return cls(value=id_string)

    @classmethod
    def generate(cls) -> "CustomFieldId":
        """Generate new ID"""
        return cls(value=str(ulid.new()))
