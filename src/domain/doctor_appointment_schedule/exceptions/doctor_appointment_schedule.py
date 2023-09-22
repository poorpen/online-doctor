from datetime import datetime

from src.common.domain.exceptions.domain import DomainException


class AppointmentAlreadyAdded(DomainException):
    value: datetime


class AppointmentNotExist(DomainException):
    value: datetime
