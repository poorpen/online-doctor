from datetime import datetime

from src.common.domain.value_objects.base import BaseValueObject
from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.value_objects.integer import IntegerInRange
from src.common.domain.value_objects.string import NonEmptyText


class Height(IntegerInRange):
    min_value: int = 0
    max_value: int = 200


class Weight(IntegerInRange):
    min_value: int = 0
    max_value: int = 220


class PatientUUID(UUIDVO):
    pass


class DateTimeOfBirth(BaseValueObject[datetime]):
    pass


class FirstName(NonEmptyText):
    max_len: int = 60


class LastName(NonEmptyText):
    max_len: int = 60


class MiddleName(NonEmptyText):
    max_len: int = 60
