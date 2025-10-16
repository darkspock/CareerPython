from typing import Protocol, TypeVar

class Event:
    pass

E = TypeVar("E", bound=Event, contravariant=True)

class EventHandler(Protocol[E]):
    def execute(self, event: E) -> None:
        ...
