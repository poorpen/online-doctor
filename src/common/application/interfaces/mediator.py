from typing import Protocol, List

from src.common.domain.models.events import Event


class IMediator(Protocol):

    def publish(self, events: List[Event]) -> None:
        raise NotImplemented
