from uuid import uuid4
from datetime import datetime, timedelta
from dataclasses import dataclass

from src.common.domain.models.aggregate import AggregateRoot
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.appointment_to_doctor.value_objects.appointment_to_doctor import DoctorUUID, PatientUUID, \
    AppointmentDatetime
from src.domain.appointment_to_doctor.enum.appointment_status import AppointmentStatus
from src.domain.appointment_to_doctor.exceptions.appointment_to_doctor import \
    (CantCancelAppointment, AppointmentCanceled, AppointmentFinished, CantMakeAppointment)


@dataclass
class AppointmentToDoctor(AggregateRoot):
    uuid: UUIDVO
    doctor_uuid: DoctorUUID
    date: AppointmentDatetime
    status: AppointmentStatus
    patient_uuid: PatientUUID

    def cancel_an_appointment(self) -> None:
        if self.date - datetime.utcnow() < timedelta(hours=24):
            raise CantCancelAppointment(self.date)
        elif self.status == AppointmentStatus.FINISHED:
            raise AppointmentFinished(self.uuid)
        elif self.status == AppointmentStatus.CANCELED:
            raise AppointmentCanceled(self.uuid)
        self.status = AppointmentStatus.CANCELED

    def finish(self) -> None:
        if self.status == AppointmentStatus.FINISHED:
            raise AppointmentFinished(self.uuid)
        elif self.status == AppointmentStatus.CANCELED:
            raise AppointmentCanceled(self.uuid)
        self.status = AppointmentStatus.FINISHED
