import phonenumbers
from datetime import datetime

from src.common.domain.value_objects.base import BaseValueObject
from src.common.domain.value_objects.string import NonEmptyText, Text


class FirstName(NonEmptyText):
    max_len: int = 60


class LastName(NonEmptyText):
    max_len: int = 60


class MiddleName(Text):
    max_len: int = 60


class Password(NonEmptyText):
    pass


class Phone(BaseValueObject[str]):

    @classmethod
    def _validate(cls, v: str) -> None:
        try:
            parsed_number = phonenumbers.parse(v)
        except phonenumbers.NumberParseException:
            raise ValueError("Missing or invalid default region")
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Phone humber invalid!")


class DateTimeOfBirth(BaseValueObject[datetime]):
    pass
