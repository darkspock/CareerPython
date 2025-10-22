"""Query and QueryHandler base classes for CQRS pattern."""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic


class Query(ABC):
    """Base class for all queries."""
    pass


TQuery = TypeVar('TQuery', bound=Query)
TResult = TypeVar('TResult')


class QueryHandler(ABC, Generic[TQuery, TResult]):
    """Base class for query handlers."""

    @abstractmethod
    def handle(self, query: TQuery) -> TResult:
        """Handle the query."""
        pass

    def execute(self, query: TQuery) -> TResult:
        """Execute method for compatibility with QueryBus."""
        return self.handle(query)
