from dataclasses import dataclass
import ulid


@dataclass(frozen=True)
class WorkflowStageId:
    """Value object for workflow stage ID"""
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Workflow stage ID cannot be empty")

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, id_string: str) -> "WorkflowStageId":
        """Create from string"""
        return cls(value=id_string)

    @classmethod
    def generate(cls) -> "WorkflowStageId":
        """Generate new ID"""
        return cls(value=str(ulid.new()))
