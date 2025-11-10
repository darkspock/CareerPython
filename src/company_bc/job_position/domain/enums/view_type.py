from enum import Enum


class ViewTypeEnum(str, Enum):
    """View type for job position workflow"""
    KANBAN = "kanban"
    LIST = "list"

