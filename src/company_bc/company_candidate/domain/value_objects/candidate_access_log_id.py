from dataclasses import dataclass
import ulid


@dataclass(frozen=True)
class CandidateAccessLogId:
    """Value object for CandidateAccessLog ID"""
    value: str

    def __post_init__(self) -> None:
        """Validate ID format"""
        if not self.value:
            raise ValueError("CandidateAccessLogId cannot be empty")

    @classmethod
    def generate(cls) -> "CandidateAccessLogId":
        """Generate a new unique ID"""
        return cls(value=str(ulid.new()))

    @classmethod
    def from_string(cls, value: str) -> "CandidateAccessLogId":
        """Create from string"""
        return cls(value=value)

    def __str__(self) -> str:
        return self.value
