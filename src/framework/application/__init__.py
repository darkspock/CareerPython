"""Framework application module - exports core CQRS components"""

# Core CQRS
from .command_bus import CommandBus
from .query_bus import QueryBus

__all__ = [
    "CommandBus",
    "QueryBus",
]
