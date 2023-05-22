import pytest
from unittest import mock
from uuid import uuid4
from datetime import datetime, timedelta

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.appointment_to_doctor.models.appointment_to_doctor import AppointmentToDoctor
from src.domain.appointment_to_doctor.value_objects.appointment_to_doctor import AppointmentDatetime, DoctorUUID, \
    PatientUUID
from src.domain.appointment_to_doctor.enum.appointment_status import AppointmentStatus
from src.domain.appointment_to_doctor.exceptions.appointment_to_doctor import \
    (CantCancelAppointment, AppointmentFinished, AppointmentCanceled, CantMakeAppointment)


@pytest.fixture()
def appointment_to_doctor() -> AppointmentToDoctor:
    return AppointmentToDoctor(
        uuid=UUIDVO(uuid4()),
        date=AppointmentDatetime(datetime.utcnow() + timedelta(days=5)),
        doctor_uuid=DoctorUUID(uuid4()),
        patient_uuid=PatientUUID(uuid4()),
        status=AppointmentStatus.ACTIVE
    )


def test_make_an_appointment_with_invalid_data():
    with pytest.raises(ValueError):
        AppointmentToDoctor(
            uuid=UUIDVO(uuid4()),
            date=AppointmentDatetime(datetime.utcnow() - timedelta(minutes=2)),
            doctor_uuid=DoctorUUID(uuid4()),
            patient_uuid=PatientUUID(uuid4()),
            status=AppointmentStatus.ACTIVE
        )


@mock.patch('src.domain.appointment_to_doctor.models.appointment_to_doctor.datetime')
def test_cancel_an_appointment_with_invalid_data(mock_datetime, appointment_to_doctor):
    mock_datetime.utcnow = mock.Mock(return_value=appointment_to_doctor.date.get_value() - timedelta(hours=23))
    with pytest.raises(CantCancelAppointment):
        appointment_to_doctor.cancel_an_appointment()


def test_cancel_an_appointment_when_it_is_canceled(appointment_to_doctor):
    appointment_to_doctor.cancel_an_appointment()
    with pytest.raises(AppointmentCanceled):
        appointment_to_doctor.cancel_an_appointment()


def test_cancel_an_appointment_when_it_is_finished(appointment_to_doctor):
    appointment_to_doctor.finish()
    with pytest.raises(AppointmentFinished):
        appointment_to_doctor.cancel_an_appointment()


def test_cancel_an_appointment(appointment_to_doctor):
    appointment_to_doctor.cancel_an_appointment()
    expected_appointment = AppointmentToDoctor(
        uuid=appointment_to_doctor.uuid,
        doctor_uuid=appointment_to_doctor.doctor_uuid,
        date=appointment_to_doctor.date,
        status=AppointmentStatus.CANCELED,
        patient_uuid=appointment_to_doctor.patient_uuid
    )
    assert appointment_to_doctor == expected_appointment


def test_finish_appointment_when_it_is_canceled(appointment_to_doctor):
    appointment_to_doctor.cancel_an_appointment()
    with pytest.raises(AppointmentCanceled):
        appointment_to_doctor.finish()


def test_finish_appointment_when_it_is_finished(appointment_to_doctor):
    appointment_to_doctor.finish()
    with pytest.raises(AppointmentFinished):
        appointment_to_doctor.finish()
