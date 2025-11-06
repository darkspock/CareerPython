from dataclasses import dataclass

import ulid


@dataclass(frozen=True)
class FieldConfigurationId:
    """Value object for field configuration ID"""
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Field configuration ID cannot be empty")

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, id_string: str) -> "FieldConfigurationId":
        """Create from string"""
        return cls(value=id_string)

    @classmethod
    def generate(cls) -> "FieldConfigurationId":
        """Generate new ID"""
        return cls(value=str(ulid.new()))
