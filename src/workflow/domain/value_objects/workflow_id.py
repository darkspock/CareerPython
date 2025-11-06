from dataclasses import dataclass
import ulid


@dataclass(frozen=True)
class WorkflowId:
    """Value object for candidate application workflow ID"""
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Candidate application workflow ID cannot be empty")

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, id_string: str) -> "WorkflowId":
        """Create from string"""
        return cls(value=id_string)

    @classmethod
    def generate(cls) -> "WorkflowId":
        """Generate new ID"""
        return cls(value=str(ulid.new()))

