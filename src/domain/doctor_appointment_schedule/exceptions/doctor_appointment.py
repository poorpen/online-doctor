from uuid import UUID

from src.common.domain.exceptions.domain import DomainException


class AppointmentBusy(DomainException):
    value: UUID
