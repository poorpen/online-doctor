from datetime import datetime, timedelta

from src.common.domain.value_objects.base import BaseValueObject
from src.common.domain.value_objects.identifiers import UUIDVO


class DoctorUUID(UUIDVO):
    pass


class PatientUUID(UUIDVO):
    pass


class ConsultationDateTime(BaseValueObject[datetime]):

    def __sub__(self, other):
        res = self.value - self._value_getter(other)
        if not isinstance(res, timedelta):
            res = self.__class__(res)
        return res
