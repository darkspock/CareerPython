from dataclasses import dataclass

from src.framework.domain.value_objects.base_id import BaseId


@dataclass(frozen=True)
class WorkflowId(BaseId):
    """Value object representing a Workflow ID."""
    pass
