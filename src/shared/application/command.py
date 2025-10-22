"""Command and CommandHandler base classes for CQRS pattern."""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic


class Command(ABC):
    """Base class for all commands."""
    pass


TCommand = TypeVar('TCommand', bound=Command)
TResult = TypeVar('TResult')


class CommandHandler(ABC, Generic[TCommand, TResult]):
    """Base class for command handlers."""

    @abstractmethod
    def handle(self, command: TCommand) -> TResult:
        """Handle the command."""
        pass

    def execute(self, command: TCommand) -> TResult:
        """Execute method for compatibility with CommandBus."""
        return self.handle(command)
