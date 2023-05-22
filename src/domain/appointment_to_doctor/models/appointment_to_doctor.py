from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from src.domain.common.models.entity import Entity

from src.domain.appointment_to_doctor.value_objects.appointment_to_doctor import Comment, DoctorUUID, PatientUUID
from src.domain.appointment_to_doctor.enum.appointment_status import AppointmentStatus
from src.domain.appointment_to_doctor.exceptions.appointment_to_doctor import \
    (InvalidDateTime, IsBusy, IsClosed, IsDeleted, IsOpen, CantCancelAppointment)


@dataclass
class AppointmentToDoctor(Entity):
    uuid: UUID
    doctor_uuid: Optional[DoctorUUID]
    date: datetime
    status: Optional[AppointmentStatus] = None
    comment: Optional[Comment] = None
    patient_uuid: Optional[PatientUUID] = None
    deleted: bool = False

    @classmethod
    def create_appointment(
            cls,
            datetime_of_appointment: datetime,
            doctor_uuid: DoctorUUID,
    ) -> "AppointmentToDoctor":
        if datetime_of_appointment < datetime.utcnow():
            raise InvalidDateTime()
        return AppointmentToDoctor(
            uuid=uuid4(),
            doctor_uuid=doctor_uuid,
            date=datetime_of_appointment,
            status=AppointmentStatus.CLOSED
        )

    def open_an_appointment(self):
        if self.status == AppointmentStatus.OPEN:
            raise IsOpen()
        elif self.status == AppointmentStatus.BUSY or self.patient_uuid:
            raise IsBusy()
        self.status = AppointmentStatus.OPEN

    def close_an_appointment(self):
        if self.status == AppointmentStatus.BUSY or self.patient_uuid:
            raise IsBusy()
        elif self.status == AppointmentStatus.CLOSED:
            raise IsClosed()
        self.status = AppointmentStatus.CLOSED

    def make_an_appointment(self, patient_uuid: PatientUUID) -> None:
        if self.status == AppointmentStatus.BUSY or self.patient_uuid:
            raise IsBusy()
        elif self.status == AppointmentStatus.CLOSED:
            raise IsClosed()
        self.patient_uuid = patient_uuid
        self.status = AppointmentStatus.BUSY

    def cancel_an_appointment(self) -> None:
        if self.date - datetime.utcnow() < timedelta(hours=24):
            raise CantCancelAppointment()
        elif self.status == AppointmentStatus.CLOSED:
            raise IsClosed()
        elif self.status == AppointmentStatus.OPEN:
            raise IsOpen()
        self.patient_uuid = None
        self.status = AppointmentStatus.OPEN

    def delete_appointment(self) -> None:
        self._validate_not_deleted()
        self.patient_uuid = None
        self.doctor_uuid = None
        self.deleted = True
        self.status = None

    def _validate_not_deleted(self) -> None:
        if self.deleted:
            raise IsDeleted()



