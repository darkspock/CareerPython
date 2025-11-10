"""Talent pool application module - exports queries and commands"""

# Queries
from .queries.get_talent_pool_entry_by_id_query import (
    GetTalentPoolEntryByIdQuery,
    GetTalentPoolEntryByIdQueryHandler,
)
from .queries.list_talent_pool_entries_query import (
    ListTalentPoolEntriesQuery,
    ListTalentPoolEntriesQueryHandler,
)
from .queries.search_talent_pool_query import SearchTalentPoolQuery, SearchTalentPoolQueryHandler

# Commands
from .commands.add_to_talent_pool_command import (
    AddToTalentPoolCommand,
    AddToTalentPoolCommandHandler,
)
from .commands.change_talent_pool_entry_status_command import (
    ChangeTalentPoolEntryStatusCommand,
    ChangeTalentPoolEntryStatusCommandHandler,
)
from .commands.remove_from_talent_pool_command import (
    RemoveFromTalentPoolCommand,
    RemoveFromTalentPoolCommandHandler,
)
from .commands.update_talent_pool_entry_command import (
    UpdateTalentPoolEntryCommand,
    UpdateTalentPoolEntryCommandHandler,
)

__all__ = [
    # Queries
    "GetTalentPoolEntryByIdQuery",
    "GetTalentPoolEntryByIdQueryHandler",
    "ListTalentPoolEntriesQuery",
    "ListTalentPoolEntriesQueryHandler",
    "SearchTalentPoolQuery",
    "SearchTalentPoolQueryHandler",
    # Commands
    "AddToTalentPoolCommand",
    "AddToTalentPoolCommandHandler",
    "ChangeTalentPoolEntryStatusCommand",
    "ChangeTalentPoolEntryStatusCommandHandler",
    "RemoveFromTalentPoolCommand",
    "RemoveFromTalentPoolCommandHandler",
    "UpdateTalentPoolEntryCommand",
    "UpdateTalentPoolEntryCommandHandler",
]

