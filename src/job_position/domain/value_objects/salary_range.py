from dataclasses import dataclass
from typing import Optional

from src.job_position.domain.exceptions.job_position_exceptions import JobPositionValidationError


@dataclass(frozen=True)
class SalaryRange:
    """Value object for salary range"""
    min_salary: Optional[float]
    max_salary: Optional[float]
    currency: str = "USD"

    def __post_init__(self) -> None:
        """Validate salary range after initialization"""
        self._validate()

    def _validate(self) -> None:
        """Validate salary range data"""
        if not self.currency or len(self.currency.strip()) == 0:
            raise JobPositionValidationError("Currency is required")

        if self.currency not in ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CHF", "SEK", "NOK", "DKK"]:
            raise JobPositionValidationError(f"Unsupported currency: {self.currency}")

        if self.min_salary is not None and self.min_salary < 0:
            raise JobPositionValidationError("Minimum salary cannot be negative")

        if self.max_salary is not None and self.max_salary < 0:
            raise JobPositionValidationError("Maximum salary cannot be negative")

        if (self.min_salary is not None and
                self.max_salary is not None and
                self.min_salary > self.max_salary):
            raise JobPositionValidationError("Minimum salary cannot be greater than maximum salary")

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "min_salary": self.min_salary,
            "max_salary": self.max_salary,
            "currency": self.currency
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SalaryRange":
        """Create from dictionary"""
        return cls(
            min_salary=data.get("min_salary"),
            max_salary=data.get("max_salary"),
            currency=data.get("currency", "USD")
        )

    def is_in_range(self, amount: float) -> bool:
        """Check if amount is within the salary range"""
        if self.min_salary is not None and amount < self.min_salary:
            return False
        if self.max_salary is not None and amount > self.max_salary:
            return False
        return True
