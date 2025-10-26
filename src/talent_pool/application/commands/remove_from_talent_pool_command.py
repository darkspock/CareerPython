"""
Remove from Talent Pool Command
Phase 8: Command to remove candidate from talent pool
"""

from dataclasses import dataclass

from core.cqrs.command import Command
from core.cqrs.command_handler import CommandHandler
from src.talent_pool.domain.value_objects.talent_pool_entry_id import TalentPoolEntryId
from src.talent_pool.domain.infrastructure.talent_pool_entry_repository_interface import (
    TalentPoolEntryRepositoryInterface,
)


@dataclass(frozen=True)
class RemoveFromTalentPoolCommand(Command):
    """Command to remove candidate from talent pool"""

    entry_id: str


class RemoveFromTalentPoolCommandHandler(CommandHandler[RemoveFromTalentPoolCommand]):
    """Handler for remove from talent pool command"""

    def __init__(self, repository: TalentPoolEntryRepositoryInterface):
        self._repository = repository

    def execute(self, command: RemoveFromTalentPoolCommand) -> None:
        """
        Execute the command to remove candidate from talent pool.

        Raises:
            ValueError: If entry not found
        """
        entry_id = TalentPoolEntryId.from_string(command.entry_id)
        entry = self._repository.get_by_id(entry_id)

        if not entry:
            raise ValueError(f"Talent pool entry {command.entry_id} not found")

        # Delete from repository
        self._repository.delete(entry_id)
