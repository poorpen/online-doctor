import uuid
from uuid import UUID
from datetime import datetime

from src.common.domain.exceptions.domain import DomainException


class ConsultationFinished(DomainException):
    value: UUID


class CantCommunicate(DomainException):
    value: UUID


class CantCancelConsultation(DomainException):
    value: datetime


class ConsultationCanceled(DomainException):
    value: UUID


class ConsultationInProcess(DomainException):
    value: UUID


class ConsultationNotStarted(DomainException):
    value: UUID


class CantStartConsultation(DomainException):
    value: datetime


class CantMakeAnAppointment(DomainException):
    value: datetime
