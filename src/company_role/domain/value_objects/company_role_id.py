"""Company Role ID value object."""
from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyRoleId:
    """Value object for company role ID."""
    value: str

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_string(value: str) -> "CompanyRoleId":
        """Create from string."""
        if not value:
            raise ValueError("Company role ID cannot be empty")
        return CompanyRoleId(value)
