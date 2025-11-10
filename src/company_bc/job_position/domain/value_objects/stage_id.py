from dataclasses import dataclass

from src.framework.domain.value_objects.base_id import BaseId


@dataclass(frozen=True)
class StageId(BaseId):
    """Value object for job position stage ID"""
    value: str

