from dataclasses import dataclass
from datetime import datetime

from src.common.domain.models.entity import Entity
from src.common.domain.value_objects.identifiers import ID

from src.domain.doctor_appointment_schedule.value_object.doctor_appointment import DoctorAppointmentDateTime, \
    DoctorScheduleUUID
from src.domain.doctor_appointment_schedule.enum.doctor_appointment_status import DoctorAppointmentStatus
from src.domain.doctor_appointment_schedule.exceptions.doctor_appointment import AppointmentBusy


@dataclass
class DoctorAppointment(Entity):
    schedule_uuid: DoctorScheduleUUID
    datetime: DoctorAppointmentDateTime
    status: DoctorAppointmentStatus

    def mark_busy(self) -> None:
        if self.status == DoctorAppointmentStatus.BUSY:
            raise AppointmentBusy(self.datetime)
        self.status = DoctorAppointmentStatus.BUSY

    def check_for_delete(self) -> None:
        if self.status == DoctorAppointmentStatus.BUSY:
            raise AppointmentBusy(self.datetime)

    @property
    def appointment_datetime(self) -> DoctorAppointmentDateTime:
        return self.datetime
