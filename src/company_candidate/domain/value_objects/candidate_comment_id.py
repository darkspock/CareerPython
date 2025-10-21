from dataclasses import dataclass
import ulid


@dataclass(frozen=True)
class CandidateCommentId:
    """Value object for CandidateComment ID"""
    value: str

    def __post_init__(self):
        """Validate ID format"""
        if not self.value:
            raise ValueError("CandidateCommentId cannot be empty")

    @classmethod
    def generate(cls) -> "CandidateCommentId":
        """Generate a new unique ID"""
        return cls(value=str(ulid.new()))

    @classmethod
    def from_string(cls, value: str) -> "CandidateCommentId":
        """Create from string"""
        return cls(value=value)

    def __str__(self) -> str:
        return self.value
