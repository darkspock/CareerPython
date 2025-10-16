from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Dict, Type


class Query(ABC):
    """Clase base para todas las queries"""
    pass


TQuery = TypeVar('TQuery', bound=Query)
TResult = TypeVar('TResult')


class QueryHandler(ABC, Generic[TQuery, TResult]):
    """Clase base para todos los query handlers"""

    @abstractmethod
    def handle(self, query: TQuery) -> TResult:
        pass


class QueryBus:
    def __init__(self) -> None:
        from core.container import Container
        container = Container()
        self.container = container
        self._handlers_cache: Dict[Type[Query], Any] = {}

    def query(self, query: Query) -> TResult:  # type: ignore
        """
        Ejecuta una query buscando automáticamente el handler por convención de nombres
        """
        query_type = type(query)

        # Cache del handler para evitar búsquedas repetitivas
        if query_type in self._handlers_cache:
            handler_instance = self._handlers_cache[query_type]()
            return handler_instance.handle(query)  # type: ignore

        # Buscar el handler por convención: GetUserQuery -> GetUserQueryHandler
        handler_name = f"{query_type.__name__}Handler"
        handler_provider_name = self._camel_to_snake(handler_name)

        handler_provider = getattr(self.container, handler_provider_name)
        self._handlers_cache[query_type] = handler_provider
        handler_instance = handler_provider()
        return handler_instance.handle(query)  # type: ignore

    @staticmethod
    def _camel_to_snake(name: str) -> str:
        """Convierte CamelCase a snake_case"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
