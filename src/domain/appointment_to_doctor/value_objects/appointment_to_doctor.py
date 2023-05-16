from uuid import UUID
from dataclasses import dataclass

from src.domain.common.value_objects.base import BaseValueObject
from src.domain.common.value_objects.string import OptionalText


@dataclass(frozen=True)
class Comment(OptionalText):
    pass


@dataclass(frozen=True)
class DoctorUUID(BaseValueObject[UUID]):
    pass


@dataclass(frozen=True)
class PatientUUID(BaseValueObject[UUID]):
    pass
