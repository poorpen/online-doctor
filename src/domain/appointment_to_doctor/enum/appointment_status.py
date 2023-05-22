from enum import Enum


class AppointmentStatus(Enum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    FINISHED = "FINISHED"
