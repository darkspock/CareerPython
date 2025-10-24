from dataclasses import dataclass
import ulid


@dataclass(frozen=True)
class CompanyWorkflowId:
    """Value object for company workflow ID"""
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Company workflow ID cannot be empty")

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, id_string: str) -> "CompanyWorkflowId":
        """Create from string"""
        return cls(value=id_string)

    @classmethod
    def generate(cls) -> "CompanyWorkflowId":
        """Generate new ID"""
        return cls(value=str(ulid.new()))
