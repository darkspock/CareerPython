from dataclasses import dataclass

from src.framework.domain.value_objects.base_id import BaseId


@dataclass(frozen=True)
class JobPositionWorkflowId(BaseId):
    """Value object for job position workflow ID"""
    value: str
