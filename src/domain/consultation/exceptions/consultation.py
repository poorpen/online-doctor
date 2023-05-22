import uuid
from uuid import UUID

from src.common.domain.exceptions.domain import DomainException


class ConsultationFinished(DomainException):
    value: UUID


class CantCommunicate(DomainException):
    value: UUID
