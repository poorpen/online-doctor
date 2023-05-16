from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from src.domain.common.models.entity import Entity

from src.domain.appointment_to_doctor.value_objects.appointment_to_doctor import Comment, DoctorUUID, PatientUUID
from src.domain.appointment_to_doctor.enum.appointment_status import AppointmentStatus
from src.domain.appointment_to_doctor.exceptions.appointment_to_doctor import \
    (InvalidDateTime, CantCancelAppointment, AlreadyDeleted)


@dataclass
class AppointmentToDoctor(Entity):
    uuid: UUID
    doctor_uuid: Optional[DoctorUUID]
    date: datetime
    comment: Comment
    status: Optional[AppointmentStatus]
    patient_uuid: Optional[PatientUUID] = None
    deleted: bool = False

    @classmethod
    def create_appointment(
            cls,
            datetime_of_appointment: datetime,
            doctor_uuid: DoctorUUID,
            comment: Comment,
    ) -> "AppointmentToDoctor":
        if datetime_of_appointment < datetime.utcnow():
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
        if self.date - datetime.utcnow() < timedelta(hours=24):
            raise CantCancelAppointment()
        self.patient_uuid = None
        self.status = AppointmentStatus.IS_FREE

    def delete(self) -> None:
        self._validate_not_deleted()

        if self.patient_uuid:
            raise CantCancelAppointment
        self.patient_uuid = None
        self.doctor_uuid = None
        self.deleted = True
        self.status = None

    def _validate_not_deleted(self) -> None:
        if self.deleted:
            raise AlreadyDeleted()



