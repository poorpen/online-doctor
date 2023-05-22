from enum import Enum


class AppointmentStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    BUSY = "BUSY"
