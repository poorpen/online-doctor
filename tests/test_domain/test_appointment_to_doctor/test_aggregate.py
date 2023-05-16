import pytest
from unittest import mock
from uuid import UUID, uuid4
from datetime import datetime, timedelta

from src.domain.appointment_to_doctor.models.appointment_to_doctor import AppointmentToDoctor
from src.domain.appointment_to_doctor.value_objects.appointment_to_doctor import Comment, DoctorUUID, PatientUUID
from src.domain.appointment_to_doctor.enum.appointment_status import AppointmentStatus
from src.domain.appointment_to_doctor.exceptions.appointment_to_doctor import \
    (InvalidDateTime, CantCancelAppointment, AlreadyDeleted)


@pytest.fixture()
def appointment_to_doctor():
    return AppointmentToDoctor.create_appointment(
        datetime_of_appointment=datetime.now() + timedelta(days=5),
        doctor_uuid=DoctorUUID(uuid4()),
        comment=Comment(""),
    )


def test_create_appointment_with_invalid_date():
    with pytest.raises(InvalidDateTime):
        AppointmentToDoctor.create_appointment(
            datetime_of_appointment=datetime.now() - timedelta(days=5),
            doctor_uuid=DoctorUUID(uuid4()),
            comment=Comment(""),
        )


def test_create_appointment_with_valid_date():
    date_of_appointment = datetime.now() + timedelta(hours=1)
    doctor_uuid = DoctorUUID(uuid4())
    comment = Comment("")
    appointment = AppointmentToDoctor.create_appointment(
        datetime_of_appointment=date_of_appointment,
        doctor_uuid=doctor_uuid,
        comment=comment,
    )
    expected_appointment = AppointmentToDoctor(
        uuid=appointment.uuid,
        date=date_of_appointment,
        doctor_uuid=doctor_uuid,
        comment=comment,
        status=AppointmentStatus.IS_FREE
    )
    assert expected_appointment == appointment


def test_make_an_appointment(appointment_to_doctor):
    patient_uuid = PatientUUID(uuid4())
    appointment_to_doctor.make_an_appointment(patient_uuid)
    assert appointment_to_doctor.status == AppointmentStatus.IS_BUSY
    assert appointment_to_doctor.patient_uuid == patient_uuid


@mock.patch('src.domain.appointment_to_doctor.models.appointment_to_doctor.datetime')
def test_cancel_an_appointment_invalid(mock_datetime, appointment_to_doctor):
    mock_datetime.utcnow = mock.Mock(return_value=appointment_to_doctor.date - timedelta(hours=23))
    with pytest.raises(CantCancelAppointment):
        appointment_to_doctor.cancel_an_appointment()


def test_cancel_an_appointment(appointment_to_doctor):
    appointment_to_doctor.cancel_an_appointment()
    assert appointment_to_doctor.patient_uuid is None
    assert appointment_to_doctor.status == AppointmentStatus.IS_FREE


def test_soft_delete_when_appointment_is_delete(appointment_to_doctor):
    appointment_to_doctor.deleted = True
    with pytest.raises(AlreadyDeleted):
        appointment_to_doctor.delete()


def test_test_soft_delete(appointment_to_doctor):
    appointment_to_doctor.delete()
    assert all([not attr for attr in
                [appointment_to_doctor.patient_uuid, appointment_to_doctor.doctor_uuid, appointment_to_doctor.status]])
    assert appointment_to_doctor.deleted
