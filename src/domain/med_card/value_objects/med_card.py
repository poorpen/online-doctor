from datetime import datetime

from src.common.domain.value_objects.base import BaseValueObject
from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.value_objects.integer import IntegerInRange


class Height(IntegerInRange):
    min_value: int = 10
    max_value: int = 200


class Weight(IntegerInRange):
    min_value: int = 30
    max_value: int = 220


class PatientUUID(UUIDVO):
    pass


class DateTimeOfBirth(BaseValueObject[datetime]):
    pass
