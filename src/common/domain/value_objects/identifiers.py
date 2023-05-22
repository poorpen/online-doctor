from uuid import UUID

from src.common.domain.value_objects.base import BaseValueObject
from src.common.domain.value_objects.integer import PositiveInteger


class ID(PositiveInteger):
    pass


class UUIDVO(BaseValueObject[UUID]):
    pass
