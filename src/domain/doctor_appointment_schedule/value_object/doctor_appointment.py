from datetime import datetime

from src.common.domain.value_objects.base import BaseValueObject
from src.common.domain.value_objects.identifiers import UUIDVO


class DoctorAppointmentDateTime(BaseValueObject[datetime]):
    pass


class DoctorScheduleUUID(UUIDVO):
    pass
