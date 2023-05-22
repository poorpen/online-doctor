from uuid import UUID

from src.common.domain.exceptions.domain import DomainException


class PasswordMismatch(DomainException):
    password: str
