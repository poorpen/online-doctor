import pytest
from uuid import uuid4
from unittest.mock import Mock
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.consultation.services.consultation import ConsultationService
from src.domain.consultation.models.consultation_events import ConsultationActive
from src.domain.consultation.value_objects.consultation import DoctorUUID, PatientUUID
from src.domain.consultation.exceptions.consultation import CantCommunicate


@pytest.fixture()
def db_gateway_mock():
    return Mock()


@pytest.fixture()
def consultation_service(db_gateway_mock):
    return ConsultationService(
        db_gateway_mock
    )


def test_check_active_when_consultation_finished(db_gateway_mock, consultation_service):
    db_gateway_mock.consultation_repo.is_active = Mock(return_value=False)
    with pytest.raises(CantCommunicate):
        consultation_service.check_active(UUIDVO(uuid4()), DoctorUUID(uuid4()), PatientUUID(uuid4()))


def test_check_active(db_gateway_mock, consultation_service):
    doctor_uuid, patient_uuid = DoctorUUID(uuid4()), PatientUUID(uuid4())
    db_gateway_mock.consultation_repo.is_active = Mock(return_value=True)
    consultation_service.check_active(UUIDVO(uuid4()), doctor_uuid, patient_uuid)
    excepted_event = ConsultationActive(
        doctor_uuid=doctor_uuid.get_value(),
        patient_uuid=patient_uuid.get_value()
    )
    assert excepted_event in consultation_service.pull_event()
