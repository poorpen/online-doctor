import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.consultation.enum.consultation_status import ConsultationStatus
from src.domain.consultation.models.consultation import Consultation
from src.domain.consultation.value_objects.consultation import StartConsultationDateTime, DoctorUUID, PatientUUID
from src.domain.consultation.exceptions.consultation import ConsultationFinished


@pytest.fixture()
def consultation():
    return Consultation(
        uuid=UUIDVO(uuid4()),
        patient_uuid=PatientUUID(uuid4()),
        doctor_uuid=DoctorUUID(uuid4()),
        start_datetime=StartConsultationDateTime(datetime.utcnow()),
        status=ConsultationStatus.IN_PROCESS
    )


def test_create_consultation_when_datetime_invalid_past():
    with pytest.raises(ValueError):
        Consultation(
            uuid=UUIDVO(uuid4()),
            patient_uuid=PatientUUID(uuid4()),
            doctor_uuid=DoctorUUID(uuid4()),
            start_datetime=StartConsultationDateTime(datetime.utcnow()) - timedelta(minutes=5),
            status=ConsultationStatus.IN_PROCESS
        )


def test_create_consultation_when_datetime_invalid_future():
    with pytest.raises(ValueError):
        Consultation(
            uuid=UUIDVO(uuid4()),
            patient_uuid=PatientUUID(uuid4()),
            doctor_uuid=DoctorUUID(uuid4()),
            start_datetime=StartConsultationDateTime(datetime.utcnow()) + timedelta(minutes=6),
            status=ConsultationStatus.IN_PROCESS
        )


def test_finish_consultation_when_it_is_finished(consultation):
    consultation.finish_consultation()
    with pytest.raises(ConsultationFinished):
        consultation.finish_consultation()


