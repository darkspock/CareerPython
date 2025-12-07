from dataclasses import dataclass

from src.framework.domain.value_objects.base_id import BaseId


@dataclass(frozen=True)
class ApplicationQuestionId(BaseId):
    """Value object representing an Application Question ID."""
    pass
