import pytest
from unittest import mock
from uuid import UUID, uuid4
from datetime import datetime, timedelta

from src.domain.appointment_to_doctor.models.appointment_to_doctor import AppointmentToDoctor
from src.domain.appointment_to_doctor.value_objects.appointment_to_doctor import Comment, DoctorUUID, PatientUUID
from src.domain.appointment_to_doctor.enum.appointment_status import AppointmentStatus
from src.domain.appointment_to_doctor.exceptions.appointment_to_doctor import \
    (InvalidDateTime, CantCancelAppointment, IsDeleted, IsBusy, IsOpen, IsClosed)


@pytest.fixture()
def appointment_to_doctor() -> AppointmentToDoctor:
    return AppointmentToDoctor.create_appointment(
        datetime_of_appointment=datetime.now() + timedelta(days=5),
        doctor_uuid=DoctorUUID(uuid4()),
    )


def test_create_appointment_with_invalid_date():
    with pytest.raises(InvalidDateTime):
        AppointmentToDoctor.create_appointment(
            datetime_of_appointment=datetime.now() - timedelta(days=5),
            doctor_uuid=DoctorUUID(uuid4()),
        )


def test_create_appointment():
    doctor_uuid = DoctorUUID(uuid4())
    date_of_appointment = datetime.now() + timedelta(days=5)
    appointment = AppointmentToDoctor.create_appointment(
        datetime_of_appointment=date_of_appointment,
        doctor_uuid=doctor_uuid,
    )
    expected_appointment = AppointmentToDoctor(
        uuid=appointment.uuid,
        doctor_uuid=doctor_uuid,
        date=date_of_appointment,
        status=AppointmentStatus.CLOSED
    )
    assert appointment == expected_appointment


def test_open_appointment_when_it_is_open(appointment_to_doctor):
    appointment_to_doctor.status = AppointmentStatus.OPEN
    with pytest.raises(IsOpen):
        appointment_to_doctor.open_an_appointment()


def test_open_appointment_when_it_is_busy(appointment_to_doctor):
    appointment_to_doctor.status = AppointmentStatus.BUSY
    with pytest.raises(IsBusy):
        appointment_to_doctor.open_an_appointment()


def test_open_appointment(appointment_to_doctor):
    expected_appointment = AppointmentToDoctor(
        uuid=appointment_to_doctor.uuid,
        doctor_uuid=appointment_to_doctor.doctor_uuid,
        date=appointment_to_doctor.date,
        status=AppointmentStatus.OPEN,
    )
    appointment_to_doctor.open_an_appointment()
    assert appointment_to_doctor == expected_appointment


def test_close_appointment_when_it_is_busy(appointment_to_doctor):
    patient_uuid = PatientUUID(uuid4())
    appointment_to_doctor.patient_uuid = patient_uuid
    appointment_to_doctor.status = AppointmentStatus.BUSY
    with pytest.raises(IsBusy):
        appointment_to_doctor.close_an_appointment()


def test_close_appointment_when_it_is_close(appointment_to_doctor):
    appointment_to_doctor.status = AppointmentStatus.CLOSED
    with pytest.raises(IsClosed):
        appointment_to_doctor.close_an_appointment()


def test_close_appointment(appointment_to_doctor):
    appointment_to_doctor.status = AppointmentStatus.OPEN
    appointment_to_doctor.close_an_appointment()
    expected_appointment = AppointmentToDoctor(
        uuid=appointment_to_doctor.uuid,
        doctor_uuid=appointment_to_doctor.doctor_uuid,
        date=appointment_to_doctor.date,
        status=AppointmentStatus.CLOSED,
    )
    assert appointment_to_doctor == expected_appointment


def test_make_an_appointment_when_it_is_busy(appointment_to_doctor):
    appointment_to_doctor.patient_uuid = PatientUUID(uuid4())
    appointment_to_doctor.status = AppointmentStatus.BUSY
    with pytest.raises(IsBusy):
        appointment_to_doctor.make_an_appointment(PatientUUID(uuid4()))


def test_make_an_appointment_when_it_is_closed(appointment_to_doctor):
    appointment_to_doctor.status = AppointmentStatus.CLOSED
    with pytest.raises(IsClosed):
        appointment_to_doctor.make_an_appointment(PatientUUID(uuid4()))


def test_make_an_appointment(appointment_to_doctor):
    patient_uuid = PatientUUID(uuid4())
    appointment_to_doctor.status = AppointmentStatus.OPEN
    appointment_to_doctor.make_an_appointment(patient_uuid)
    expected_appointment = AppointmentToDoctor(
        uuid=appointment_to_doctor.uuid,
        doctor_uuid=appointment_to_doctor.doctor_uuid,
        date=appointment_to_doctor.date,
        status=AppointmentStatus.BUSY,
        patient_uuid=patient_uuid
    )
    assert appointment_to_doctor == expected_appointment


@mock.patch('src.domain.appointment_to_doctor.models.appointment_to_doctor.datetime')
def test_cancel_an_appointment_with_invalid_data(mock_datetime, appointment_to_doctor):
    mock_datetime.utcnow = mock.Mock(return_value=appointment_to_doctor.date - timedelta(hours=23))
    with pytest.raises(CantCancelAppointment):
        appointment_to_doctor.cancel_an_appointment()


def test_cancel_an_appointment_when_it_is_closed(appointment_to_doctor):
    appointment_to_doctor.status = AppointmentStatus.CLOSED
    with pytest.raises(IsClosed):
        appointment_to_doctor.cancel_an_appointment()


def test_cancel_an_appointment_when_it_is_open(appointment_to_doctor):
    appointment_to_doctor.status = AppointmentStatus.OPEN
    with pytest.raises(IsOpen):
        appointment_to_doctor.cancel_an_appointment()


def test_cancel_an_appointment(appointment_to_doctor):
    appointment_to_doctor.patient_uuid = PatientUUID(uuid4())
    appointment_to_doctor.status = AppointmentStatus.BUSY
    appointment_to_doctor.cancel_an_appointment()
    expected_appointment = AppointmentToDoctor(
        uuid=appointment_to_doctor.uuid,
        doctor_uuid=appointment_to_doctor.doctor_uuid,
        date=appointment_to_doctor.date,
        status=AppointmentStatus.OPEN,
        patient_uuid=None
    )
    assert appointment_to_doctor == expected_appointment


def test_delete_appointment_when_it_is_deleted(appointment_to_doctor):
    appointment_to_doctor.deleted = True
    with pytest.raises(IsDeleted):
        appointment_to_doctor._validate_not_deleted()


def test_delete_appointment(appointment_to_doctor):
    appointment_to_doctor.delete_appointment()
    expected_appointment = AppointmentToDoctor(
        uuid=appointment_to_doctor.uuid,
        doctor_uuid=None,
        date=appointment_to_doctor.date,
        status=None,
        patient_uuid=None,
        deleted=True
    )
    assert appointment_to_doctor == expected_appointment
