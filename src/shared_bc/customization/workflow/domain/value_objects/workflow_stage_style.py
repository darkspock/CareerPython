from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowStageStyle:
    background_color: str
    text_color: str
    icon: str
