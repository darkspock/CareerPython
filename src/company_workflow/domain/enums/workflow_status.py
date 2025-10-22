from enum import Enum


class WorkflowStatus(str, Enum):
    """Status of a workflow"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
