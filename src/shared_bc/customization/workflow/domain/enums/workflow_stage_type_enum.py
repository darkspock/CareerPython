from enum import Enum


class WorkflowStageTypeEnum(str, Enum):
    SUCCESS = "success"
    INITIAL = "initial"
    PROGRESS = "progress"
    FAIL = "fail"
    HOLD = "hold"
