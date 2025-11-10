"""Default view enum for phases"""
from enum import Enum


class DefaultView(str, Enum):
    """Default view type for a phase"""
    KANBAN = "KANBAN"
    LIST = "LIST"
