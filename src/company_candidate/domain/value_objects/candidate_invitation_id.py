from dataclasses import dataclass
import ulid


@dataclass(frozen=True)
class CandidateInvitationId:
    """Value object for CandidateInvitation ID"""
    value: str

    def __post_init__(self):
        """Validate ID format"""
        if not self.value:
            raise ValueError("CandidateInvitationId cannot be empty")

    @classmethod
    def generate(cls) -> "CandidateInvitationId":
        """Generate a new unique ID"""
        return cls(value=str(ulid.new()))

    @classmethod
    def from_string(cls, value: str) -> "CandidateInvitationId":
        """Create from string"""
        return cls(value=value)

    def __str__(self) -> str:
        return self.value
