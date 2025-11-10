from enum import Enum


class KanbanDisplayEnum(str, Enum):
    COLUMN = "column"
    ROW = "row"
    HIDDEN = "hidden"
