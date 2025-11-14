from enum import Enum


class KanbanDisplayEnum(str, Enum):
    """Kanban display configuration for workflow stages"""
    VERTICAL = "vertical"  # Display as column in Kanban
    HORIZONTAL_BOTTOM = "horizontal_bottom"  # Display as row at bottom
    HIDDEN = "hidden"  # Hidden from Kanban view
