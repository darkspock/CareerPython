from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, Type, Any


class Command(ABC):
    pass


TCommand = TypeVar('TCommand', bound=Command)


class CommandHandler(ABC, Generic[TCommand]):

    @abstractmethod
    def execute(self, command: TCommand) -> None:
        pass


class CommandBus:
    def __init__(self) -> None:
        from core.container import Container
        container = Container()
        self.container = container
        self._handlers_cache: Dict[Type[Command], Any] = {}

    def dispatch(self, command: Command) -> None:
        command_type = type(command)

        # Cache del handler para evitar búsquedas repetitivas
        if command_type in self._handlers_cache:
            handler_instance = self._handlers_cache[command_type]()
            handler_instance.execute(command)
            return

        # Buscar el handler por convención: GetUserCommand -> GetUserCommandHandler
        handler_name = f"{command_type.__name__}Handler"
        handler_provider_name = self._camel_to_snake(handler_name)

        handler_provider = getattr(self.container, handler_provider_name)
        self._handlers_cache[command_type] = handler_provider
        handler_instance = handler_provider()
        handler_instance.execute(command)

    def execute(self, command: Command) -> None:
        """Alias for dispatch method for backward compatibility"""
        self.dispatch(command)

    @staticmethod
    def _camel_to_snake(name: str) -> str:
        """Convierte CamelCase a snake_case"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
