"""Reorder Stages Command."""
from dataclasses import dataclass
from typing import List
from src.shared.application.command import Command


@dataclass(frozen=True)
class ReorderStagesCommand(Command):
    """Command to reorder stages in a workflow."""

    workflow_id: str
    stage_ids_in_order: List[str]
