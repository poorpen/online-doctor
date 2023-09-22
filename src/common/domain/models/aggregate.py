from abc import ABC
from typing import List
from dataclasses import dataclass, field

from src.common.domain.models.events import Event


@dataclass
class AggregateRoot(ABC):
    _events: List[Event] = field(default_factory=list, init=False)

    def _get_events(self) -> List[Event]:
        return self._events.copy()

    def _clear_events(self) -> None:
        self._events.clear()

    def record_event(self, event: Event) -> None:
        self._events.append(event)

    def pull_events(self) -> List[Event]:
        events = self._get_events()
        self._clear_events()
        return events
