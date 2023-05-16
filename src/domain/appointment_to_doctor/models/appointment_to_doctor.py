from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from src.domain.common.models.entity import Entity

from src.domain.appointment_to_doctor.value_objects.appointment_to_doctor import Comment, DoctorUUID, PatientUUID
from src.domain.appointment_to_doctor.enum.appointment_status import AppointmentStatus
from src.domain.appointment_to_doctor.exceptions.appointment_to_doctor import InvalidDateTime, CantCancelAppointment


@dataclass
class AppointmentToDoctor(Entity):
    uuid: UUID
    doctor_uuid: DoctorUUID
    date: datetime
    comment: Comment
    status: AppointmentStatus
    patient_uuid: Optional[PatientUUID] = None

    @classmethod
    def create_appointment(
            cls,
            datetime_of_appointment: datetime,
            doctor_uuid: DoctorUUID,
            comment: Comment,
    ) -> "AppointmentToDoctor":
        if datetime_of_appointment < datetime.now():
            raise InvalidDateTime()
        return AppointmentToDoctor(
            uuid=uuid4(),
            doctor_uuid=doctor_uuid,
            date=datetime_of_appointment,
            comment=comment,
            status=AppointmentStatus.IS_FREE
        )

    def make_an_appointment(self, patient_uuid: PatientUUID) -> None:
        self.patient_uuid = patient_uuid
        self.status = AppointmentStatus.IS_BUSY

    def cancel_an_appointment(self) -> None:
        if self.date - datetime.now() < timedelta(hours=24):
            raise CantCancelAppointment()
        self.patient_uuid = None
        self.status = AppointmentStatus.IS_FREE
