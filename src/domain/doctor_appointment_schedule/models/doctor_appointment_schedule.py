from typing import List
from dataclasses import dataclass, field

from src.common.domain.models.aggregate import AggregateRoot
from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.utils.binary_search import binary_search

from src.domain.doctor_appointment_schedule.models.doctor_appointment import DoctorAppointment
from src.domain.doctor_appointment_schedule.value_object.doctor_appointment_schedule import DoctorUUID
from src.domain.doctor_appointment_schedule.value_object.doctor_appointment import DoctorAppointmentDateTime, \
    DoctorScheduleUUID
from src.domain.doctor_appointment_schedule.enum.doctor_appointment_status import DoctorAppointmentStatus
from src.domain.doctor_appointment_schedule.exceptions.doctor_appointment_schedule import AppointmentAlreadyAdded, \
    AppointmentNotExist


@dataclass
class DoctorAppointmentsSchedule(AggregateRoot):
    uuid: UUIDVO
    doctor_uuid: DoctorUUID
    doctor_appointments: List[DoctorAppointment] = field(default_factory=list)

    def add_appointments(self, doctor_appointments_dates: List[DoctorAppointmentDateTime]) -> None:
        for doctor_appointment_date in doctor_appointments_dates:
            if self._search_appointment(doctor_appointment_date):
                raise AppointmentAlreadyAdded(doctor_appointment_date)
            self.doctor_appointments.append(DoctorAppointment(schedule_uuid=DoctorScheduleUUID(self.uuid.get_value()),
                                                              datetime=doctor_appointment_date,
                                                              status=DoctorAppointmentStatus.OPEN))

    def delete_appointments(self, doctor_appointments_dates: List[DoctorAppointmentDateTime]) -> None:
        for doctor_appointment_date in doctor_appointments_dates:
            doctor_appointment = self._search_appointment(doctor_appointment_date)
            if not doctor_appointment:
                raise AppointmentNotExist(doctor_appointment_date)
            doctor_appointment.check_for_delete()
            self.doctor_appointments.remove(doctor_appointment)

    def mark_appointment_busy(self, doctor_appointment_date: DoctorAppointmentDateTime) -> None:
        appointment = self._search_appointment(doctor_appointment_date)
        if not appointment:
            raise AppointmentNotExist(doctor_appointment_date)
        appointment.mark_busy()

    def _search_appointment(self, doctor_appointment_datetime: DoctorAppointmentDateTime) -> DoctorAppointment | None:
        collection_to_search = sorted(self.doctor_appointments, key=lambda p: p.appointment_datetime)
        return binary_search(
            collection_to_search,
            doctor_appointment_datetime,
            lambda appointment: appointment.appointment_datetime
        )
