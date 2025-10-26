"""
Update Talent Pool Entry Command
Phase 8: Command to update talent pool entry
"""

from dataclasses import dataclass
from typing import Optional, List

from src.shared.application.command_bus import Command, CommandHandler
from src.talent_pool.domain.value_objects.talent_pool_entry_id import TalentPoolEntryId
from src.talent_pool.domain.infrastructure.talent_pool_entry_repository_interface import (
    TalentPoolEntryRepositoryInterface,
)


@dataclass(frozen=True)
class UpdateTalentPoolEntryCommand(Command):
    """Command to update talent pool entry"""

    entry_id: str
    added_reason: Optional[str] = None
    tags: Optional[List[str]] = None
    rating: Optional[int] = None
    notes: Optional[str] = None


class UpdateTalentPoolEntryCommandHandler(CommandHandler[UpdateTalentPoolEntryCommand]):
    """Handler for update talent pool entry command"""

    def __init__(self, repository: TalentPoolEntryRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateTalentPoolEntryCommand) -> None:
        """
        Execute the command to update talent pool entry.

        Raises:
            ValueError: If entry not found
        """
        entry_id = TalentPoolEntryId.from_string(command.entry_id)
        entry = self._repository.get_by_id(entry_id)

        if not entry:
            raise ValueError(f"Talent pool entry {command.entry_id} not found")

        # Update entry
        entry.update(
            added_reason=command.added_reason,
            tags=command.tags,
            rating=command.rating,
            notes=command.notes,
        )

        # Save to repository
        self._repository.save(entry)
