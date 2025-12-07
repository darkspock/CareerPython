from dataclasses import dataclass

from src.framework.domain.value_objects.base_id import BaseId


@dataclass(frozen=True)
class PositionQuestionConfigId(BaseId):
    """Value object representing a Position Question Config ID."""
    pass
