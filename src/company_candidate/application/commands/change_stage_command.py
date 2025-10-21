from dataclasses import dataclass

from src.shared.application.command import Command


@dataclass(frozen=True)
class ChangeStageCommand(Command):
    """Command to change the workflow stage of a company candidate"""
    id: str
    new_stage_id: str
