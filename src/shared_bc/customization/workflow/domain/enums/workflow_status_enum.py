from enum import Enum


class WorkflowStatusEnum(str, Enum):
    """Status of a workflow"""
    DRAFT = "draft"  # Workflow is being configured
    ACTIVE = "active"  # Workflow is active and can be used
    ARCHIVED = "archived"  # Workflow is archived
