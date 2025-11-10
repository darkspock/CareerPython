from enum import Enum


class TaskStatus(str, Enum):
    """Status of the task for processing an application at a specific stage"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
