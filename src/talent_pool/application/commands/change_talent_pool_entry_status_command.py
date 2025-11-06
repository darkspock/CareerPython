"""
Change Talent Pool Entry Status Command
Phase 8: Command to change talent pool entry status
"""

from dataclasses import dataclass

from src.shared.application.command_bus import CommandHandler, Command
from src.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus
from src.talent_pool.domain.infrastructure.talent_pool_entry_repository_interface import (
    TalentPoolEntryRepositoryInterface,
)
from src.talent_pool.domain.value_objects.talent_pool_entry_id import TalentPoolEntryId


@dataclass(frozen=True)
class ChangeTalentPoolEntryStatusCommand(Command):
    """Command to change talent pool entry status"""

    entry_id: str
    new_status: TalentPoolStatus


class ChangeTalentPoolEntryStatusCommandHandler(CommandHandler[ChangeTalentPoolEntryStatusCommand]):
    """Handler for change talent pool entry status command"""

    def __init__(self, repository: TalentPoolEntryRepositoryInterface):
        self._repository = repository

    def execute(self, command: ChangeTalentPoolEntryStatusCommand) -> None:
        """
        Execute the command to change talent pool entry status.

        Raises:
            ValueError: If entry not found
        """
        entry_id = TalentPoolEntryId.from_string(command.entry_id)
        entry = self._repository.get_by_id(entry_id)

        if not entry:
            raise ValueError(f"Talent pool entry {command.entry_id} not found")

        # Change status
        entry.change_status(command.new_status)

        # Save to repository
        self._repository.save(entry)
