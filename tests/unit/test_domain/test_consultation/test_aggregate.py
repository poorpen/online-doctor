import pytest
from uuid import uuid4
from unittest import mock
from datetime import datetime, timedelta

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.consultation.enum.consultation_status import ConsultationStatus
from src.domain.consultation.models.consultation import Consultation
from src.domain.consultation.value_objects.consultation import ConsultationDateTime, DoctorUUID, PatientUUID
from src.domain.consultation.exceptions.consultation import ConsultationFinished, CantMakeAnAppointment, \
    CantCancelConsultation, ConsultationCanceled, ConsultationInProcess


@pytest.fixture()
def scheduled_consultation():
    return Consultation(
        uuid=UUIDVO(uuid4()),
        patient_uuid=PatientUUID(uuid4()),
        doctor_uuid=DoctorUUID(uuid4()),
        consultation_datetime=ConsultationDateTime(datetime.utcnow()) + timedelta(days=5),
        status=ConsultationStatus.SCHEDULED
    )


@pytest.fixture()
def process_consultation():
    return Consultation(
        uuid=UUIDVO(uuid4()),
        patient_uuid=PatientUUID(uuid4()),
        doctor_uuid=DoctorUUID(uuid4()),
        consultation_datetime=ConsultationDateTime(datetime.utcnow()),
        status=ConsultationStatus.IN_PROCESS
    )


def test_scheduled_a_consultation_with_invalid_datetime():
    with pytest.raises(CantMakeAnAppointment):
        Consultation.scheduled_a_consultation(
            uuid=UUIDVO(uuid4()),
            patient_uuid=PatientUUID(uuid4()),
            doctor_uuid=DoctorUUID(uuid4()),
            consultation_datetime=ConsultationDateTime(datetime.utcnow()) - timedelta(minutes=1)
        )


def test_scheduled_a_consultation():
    Consultation.scheduled_a_consultation(
        uuid=UUIDVO(uuid4()),
        patient_uuid=PatientUUID(uuid4()),
        doctor_uuid=DoctorUUID(uuid4()),
        consultation_datetime=ConsultationDateTime(datetime.utcnow() + timedelta(days=10))
    )


@mock.patch('src.domain.consultation.models.consultation.datetime')
def test_cancel_consultation_with_invalid_datetime(mock_datetime, scheduled_consultation):
    mock_datetime.utcnow = mock.Mock(
        return_value=scheduled_consultation.consultation_datetime.get_value() - timedelta(hours=23))
    with pytest.raises(CantCancelConsultation):
        scheduled_consultation.cancel_scheduled_consultation()


def test_cancel_consultation_when_it_already_canceled(scheduled_consultation):
    scheduled_consultation.cancel_scheduled_consultation()
    with pytest.raises(ConsultationCanceled):
        scheduled_consultation.cancel_scheduled_consultation()


def test_cancel_consultation_when_it_in_process(process_consultation):
    with pytest.raises(ConsultationInProcess):
        process_consultation.cancel_scheduled_consultation()


def test_cancel_consultation(scheduled_consultation):
    scheduled_consultation.cancel_scheduled_consultation()
    assert ConsultationStatus.CANCELED == scheduled_consultation.status


def test_cancel_consultation_when_it_already_finished(process_consultation):
    process_consultation.finish_consultation()
    with pytest.raises(ConsultationFinished):
        process_consultation.cancel_scheduled_consultation()


def test_start_consultation_when_it_already_canceled(scheduled_consultation):
    scheduled_consultation.cancel_scheduled_consultation()
    with pytest.raises(ConsultationCanceled):
        scheduled_consultation.start_consultation()


def test_start_consultation_when_it_already_finished(process_consultation):
    process_consultation.finish_consultation()
    with pytest.raises(ConsultationFinished):
        process_consultation.start_consultation()


def test_start_consultation(scheduled_consultation):
    scheduled_consultation.consultation_datetime = ConsultationDateTime(datetime.utcnow())
    scheduled_consultation.start_consultation()
    assert ConsultationStatus.IN_PROCESS == scheduled_consultation.status


def test_finish_consultation_when_it_is_finished(process_consultation):
    process_consultation.finish_consultation()
    with pytest.raises(ConsultationFinished):
        process_consultation.finish_consultation()


def test_finish_consultation_when_it_is_canceled(scheduled_consultation):
    scheduled_consultation.cancel_scheduled_consultation()
    with pytest.raises(ConsultationCanceled):
        scheduled_consultation.finish_consultation()


def test_finish_consultation(process_consultation):
    process_consultation.finish_consultation()
