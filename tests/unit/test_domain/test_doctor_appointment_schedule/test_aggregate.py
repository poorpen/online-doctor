import datetime

import pytest
from uuid import uuid4
from datetime import datetime

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.doctor_appointment_schedule.models.doctor_appointment_schedule import DoctorAppointmentsSchedule
from src.domain.doctor_appointment_schedule.models.doctor_appointment import DoctorAppointment
from src.domain.doctor_appointment_schedule.value_object.doctor_appointment_schedule import DoctorUUID
from src.domain.doctor_appointment_schedule.value_object.doctor_appointment import DoctorAppointmentDateTime, \
    DoctorScheduleUUID
from src.domain.doctor_appointment_schedule.enum.doctor_appointment_status import DoctorAppointmentStatus
from src.domain.doctor_appointment_schedule.exceptions.doctor_appointment_schedule import AppointmentAlreadyAdded, \
    AppointmentNotExist
from src.domain.doctor_appointment_schedule.exceptions.doctor_appointment import AppointmentBusy


@pytest.fixture()
def doctor_appointment_schedule():
    return DoctorAppointmentsSchedule(
        uuid=UUIDVO(uuid4()),
        doctor_uuid=DoctorUUID(uuid4())
    )


def test_add_appointment_when_it_already_exist(doctor_appointment_schedule):
    first_appointment_date = DoctorAppointmentDateTime(datetime.utcnow())
    appointments_dates = [first_appointment_date, DoctorAppointmentDateTime(datetime.utcnow())]
    doctor_appointment_schedule.add_appointments(appointments_dates)
    with pytest.raises(AppointmentAlreadyAdded):
        doctor_appointment_schedule.add_appointments([first_appointment_date])


def test_add_appointment(doctor_appointment_schedule):
    appointments_dates = [DoctorAppointmentDateTime(datetime.utcnow()),
                          DoctorAppointmentDateTime(datetime.utcnow())]
    doctor_appointment_schedule.add_appointments(appointments_dates)
    expected = [DoctorAppointment(datetime=appointments_dates[0], status=DoctorAppointmentStatus.OPEN,
                                  schedule_uuid=DoctorScheduleUUID(doctor_appointment_schedule.uuid.get_value())),
                DoctorAppointment(datetime=appointments_dates[1], status=DoctorAppointmentStatus.OPEN,
                                  schedule_uuid=DoctorScheduleUUID(doctor_appointment_schedule.uuid.get_value()))]
    assert expected == doctor_appointment_schedule.doctor_appointments


def test_mark_appointment_when_it_not_exist(doctor_appointment_schedule):
    with pytest.raises(AppointmentNotExist):
        doctor_appointment_schedule.mark_appointment_busy(DoctorAppointmentDateTime(datetime.utcnow()))


def test_mark_appointment_when_it_busy(doctor_appointment_schedule):
    doctor_appointments_dates = [DoctorAppointmentDateTime(datetime.utcnow())]
    doctor_appointment_schedule.add_appointments(doctor_appointments_dates)
    doctor_appointment_schedule.mark_appointment_busy(doctor_appointments_dates[-1])
    with pytest.raises(AppointmentBusy):
        doctor_appointment_schedule.mark_appointment_busy(doctor_appointments_dates[-1])


def test_delete_appointments_when_it_not_exist(doctor_appointment_schedule):
    with pytest.raises(AppointmentNotExist):
        doctor_appointment_schedule.delete_appointments([DoctorAppointmentDateTime(datetime.utcnow())])


def test_delete_appointment_when_it_is_busy(doctor_appointment_schedule):
    doctor_appointments_dates = [DoctorAppointmentDateTime(datetime.utcnow())]
    doctor_appointment_schedule.add_appointments(doctor_appointments_dates)
    doctor_appointment_schedule.mark_appointment_busy(doctor_appointments_dates[-1])
    with pytest.raises(AppointmentBusy):
        doctor_appointment_schedule.delete_appointments(doctor_appointments_dates)
