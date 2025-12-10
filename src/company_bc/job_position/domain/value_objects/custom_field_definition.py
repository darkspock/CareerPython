from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from src.company_bc.job_position.domain.exceptions.job_position_exceptions import JobPositionValidationError


VALID_FIELD_TYPES = ["TEXT", "NUMBER", "SELECT", "MULTISELECT", "DATE", "BOOLEAN", "URL"]


@dataclass
class CustomFieldDefinition:
    """
    Value object for custom field definition.

    This represents a field definition that is COPIED from workflow to job position
    at creation time (Snapshot Pattern). Once the position is published, the structure
    is frozen and only values can be changed.
    """
    field_key: str                              # Unique identifier
    label: str                                  # Display name for recruiters/candidates
    field_type: str                             # TEXT, NUMBER, SELECT, MULTISELECT, DATE, BOOLEAN, URL
    options: Optional[List[Any]]                # For SELECT/MULTISELECT types (strings or i18n objects)
    is_required: bool                           # Whether field must be filled
    candidate_visible: bool                     # Whether candidates see this field
    validation_rules: Optional[Dict[str, Any]]  # Min/max, patterns, etc.
    sort_order: int                             # Display order
    is_active: bool                             # Recruiter can deactivate per position

    def __post_init__(self) -> None:
        """Validate after initialization"""
        self._validate()

    def _validate(self) -> None:
        """Validate custom field definition"""
        if not self.field_key or len(self.field_key.strip()) == 0:
            raise JobPositionValidationError("Field key is required")

        if not self.label or len(self.label.strip()) == 0:
            raise JobPositionValidationError("Field label is required")

        if self.field_type not in VALID_FIELD_TYPES:
            raise JobPositionValidationError(
                f"Invalid field type: {self.field_type}. "
                f"Must be one of: {', '.join(VALID_FIELD_TYPES)}"
            )

        # SELECT and MULTISELECT require options
        if self.field_type in ["SELECT", "MULTISELECT"]:
            if not self.options or len(self.options) == 0:
                raise JobPositionValidationError(
                    f"Options are required for {self.field_type} field type"
                )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "field_key": self.field_key,
            "label": self.label,
            "field_type": self.field_type,
            "options": self.options,
            "is_required": self.is_required,
            "candidate_visible": self.candidate_visible,
            "validation_rules": self.validation_rules,
            "sort_order": self.sort_order,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CustomFieldDefinition":
        """Create from dictionary"""
        return cls(
            field_key=data.get("field_key", ""),
            label=data.get("label", ""),
            field_type=data.get("field_type", "TEXT"),
            options=data.get("options"),
            is_required=data.get("is_required", False),
            candidate_visible=data.get("candidate_visible", True),
            validation_rules=data.get("validation_rules"),
            sort_order=data.get("sort_order", 0),
            is_active=data.get("is_active", True)
        )

    @classmethod
    def from_list(cls, data: List[dict]) -> List["CustomFieldDefinition"]:
        """Create list of CustomFieldDefinition from list of dicts"""
        return [cls.from_dict(item) for item in data] if data else []

    @staticmethod
    def to_list(definitions: List["CustomFieldDefinition"]) -> List[dict]:
        """Convert list of CustomFieldDefinition to list of dicts"""
        return [defn.to_dict() for defn in definitions] if definitions else []

    def deactivate(self) -> "CustomFieldDefinition":
        """Return a copy with is_active=False"""
        return CustomFieldDefinition(
            field_key=self.field_key,
            label=self.label,
            field_type=self.field_type,
            options=self.options,
            is_required=self.is_required,
            candidate_visible=self.candidate_visible,
            validation_rules=self.validation_rules,
            sort_order=self.sort_order,
            is_active=False
        )

    def activate(self) -> "CustomFieldDefinition":
        """Return a copy with is_active=True"""
        return CustomFieldDefinition(
            field_key=self.field_key,
            label=self.label,
            field_type=self.field_type,
            options=self.options,
            is_required=self.is_required,
            candidate_visible=self.candidate_visible,
            validation_rules=self.validation_rules,
            sort_order=self.sort_order,
            is_active=True
        )
