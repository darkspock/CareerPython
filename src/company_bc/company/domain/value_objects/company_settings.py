from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class CompanySettings:
    """Custom company settings"""
    value: Dict[str, Any]

    def __post_init__(self) -> None:
        """Validate settings - ensure value is never None"""
        pass

    @classmethod
    def default(cls) -> "CompanySettings":
        """Create default settings"""
        return cls(value={})

    @classmethod
    def from_dict(cls, settings: Dict[str, Any]) -> "CompanySettings":
        """Create settings from dictionary"""
        return cls(value=settings or {})

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return dict(self.value)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.value.get(key, default)
