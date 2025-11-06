"""Field Option Value Object - represents a single option/check value with i18n support."""
from dataclasses import dataclass
from typing import List, Dict, Optional

import ulid


@dataclass(frozen=True)
class FieldOptionLabel:
    """Single i18n label entry"""
    language: str  # Language code (e.g., "en", "es")
    label: str  # The translated label text

    def __post_init__(self) -> None:
        if not self.language:
            raise ValueError("Language code cannot be empty")
        if not self.label:
            raise ValueError("Label text cannot be empty")
        if len(self.language) > 10:
            raise ValueError("Language code cannot exceed 10 characters")
        if len(self.label) > 500:
            raise ValueError("Label text cannot exceed 500 characters")


@dataclass(frozen=True)
class FieldOption:
    """
    Field Option Value Object

    Represents a single option value for dropdown, multi-select, radio, or checkbox fields.
    Each option has:
    - id: ULID for stable reference (prevents data corruption on rename)
    - sort: Order index for display
    - labels: Array of i18n labels with language codes
    """
    id: str  # ULID
    sort: int  # Order index (0-based)
    labels: List[FieldOptionLabel]  # i18n labels array

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Option ID cannot be empty")
        if self.sort < 0:
            raise ValueError("Sort index cannot be negative")
        if not self.labels:
            raise ValueError("Options must have at least one label")

    @staticmethod
    def create(
            labels: List[Dict[str, str]],  # [{"language": "en", "label": "Option 1"}, ...]
            sort: int = 0,
            id: Optional[str] = None
    ) -> "FieldOption":
        """Factory method to create a new field option"""
        option_id = id if id else str(ulid.new())

        field_option_labels = [
            FieldOptionLabel(language=label["language"], label=label["label"])
            for label in labels
        ]

        return FieldOption(
            id=option_id,
            sort=sort,
            labels=field_option_labels
        )

    def get_label(self, language: Optional[str] = None) -> str:
        """
        Get label for a specific language with fallback

        Args:
            language: Language code (e.g., "en", "es"). If None, returns first label.

        Returns:
            Label text for the requested language, or first label as fallback
        """
        if not self.labels:
            return ""

        # If no language specified, return first label
        if not language:
            return self.labels[0].label

        # Try to find label for requested language
        for label in self.labels:
            if label.language == language:
                return label.label

        # Fallback to first label
        return self.labels[0].label

    def update_label(self, language: str, new_label: str) -> "FieldOption":
        """Update or add a label for a specific language"""
        new_labels = []
        updated = False

        for label in self.labels:
            if label.language == language:
                new_labels.append(FieldOptionLabel(language=language, label=new_label))
                updated = True
            else:
                new_labels.append(label)

        # If language doesn't exist, add it
        if not updated:
            new_labels.append(FieldOptionLabel(language=language, label=new_label))

        return FieldOption(
            id=self.id,
            sort=self.sort,
            labels=new_labels
        )

    def remove_label(self, language: str) -> "FieldOption":
        """Remove a label for a specific language (must have at least one remaining)"""
        new_labels = [label for label in self.labels if label.language != language]

        if not new_labels:
            raise ValueError("Cannot remove last label from option")

        return FieldOption(
            id=self.id,
            sort=self.sort,
            labels=new_labels
        )

    def change_sort(self, new_sort: int) -> "FieldOption":
        """Change the sort order of this option"""
        if new_sort < 0:
            raise ValueError("Sort index cannot be negative")

        return FieldOption(
            id=self.id,
            sort=new_sort,
            labels=self.labels
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "sort": self.sort,
            "labels": [
                {"language": label.language, "label": label.label}
                for label in self.labels
            ]
        }

    @staticmethod
    def from_dict(data: Dict) -> "FieldOption":
        """Create from dictionary"""
        return FieldOption(
            id=data["id"],
            sort=data["sort"],
            labels=[
                FieldOptionLabel(language=label["language"], label=label["label"])
                for label in data["labels"]
            ]
        )
