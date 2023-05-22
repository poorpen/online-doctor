from datetime import datetime, timedelta

from src.common.domain.value_objects.base import BaseValueObject
from src.common.domain.value_objects.identifiers import UUIDVO


class DoctorUUID(UUIDVO):
    pass


class PatientUUID(UUIDVO):
    pass


class StartConsultationDateTime(BaseValueObject[datetime]):

    @classmethod
    def _validate(cls, v: datetime) -> None:
        if v < datetime.utcnow() - timedelta(minutes=5) or v > datetime.utcnow() + timedelta(minutes=5):
            raise ValueError("consultation date invalid")
