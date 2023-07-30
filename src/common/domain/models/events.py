from abc import ABC

from dataclasses import dataclass


class Event(ABC):
    pass


class DomainEvent(Event):
    pass


class LoggingEvent(Event):
    pass
