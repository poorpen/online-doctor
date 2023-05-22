from uuid import UUID

from src.domain.common.value_objects.base import BaseValueObject
from src.domain.common.value_objects.string import Text


class Comment(Text):
    pass


class DoctorUUID(BaseValueObject[UUID]):
    pass


class PatientUUID(BaseValueObject[UUID]):
    pass
