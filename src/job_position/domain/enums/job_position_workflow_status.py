"""Job Position Workflow Status Enum."""
from enum import Enum


class JobPositionWorkflowStatusEnum(str, Enum):
    """Status of a job position workflow"""
    DRAFT = "draft"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
