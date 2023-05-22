from uuid import UUID
from datetime import datetime

from src.common.domain.exceptions.domain import DomainException


class CantCancelAppointment(DomainException):
    value: UUID


class AppointmentFinished(DomainException):
    value: UUID


class AppointmentCanceled(DomainException):
    value: UUID


class CantMakeAppointment(DomainException):
    value: datetime
