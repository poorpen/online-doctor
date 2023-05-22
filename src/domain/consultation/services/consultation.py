from typing import List

from src.common.domain.models.event import Event
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.consultation.models.consultation_events import ConsultationActive
from src.domain.consultation.exceptions.consultation import CantCommunicate
from src.domain.consultation.interfaces.db_gateway.db_gateway import IDBGateway
from src.domain.consultation.value_objects.consultation import DoctorUUID, PatientUUID


class ConsultationService:

    def __init__(self, db_gateway: IDBGateway):
        self._db_gateway = db_gateway
        self._events: List[Event] = []

    def _record_event(self, event: Event) -> None:
        self._events.append(event)

    def _clear_event(self) -> None:
        self._events.clear()

    def _get_events(self) -> List[Event]:
        return self._events.copy()

    def pull_event(self) -> List[Event]:
        events = self._get_events()
        self._clear_event()
        return events

    def check_active(self, consultation_uuid: UUIDVO, doctor_uuid: DoctorUUID, patient_uuid: PatientUUID) -> None:
        check_result = self._db_gateway.consultation_repo.is_active(consultation_uuid)
        if not check_result:
            raise CantCommunicate(consultation_uuid)
        self._record_event(
            ConsultationActive(doctor_uuid=doctor_uuid.get_value(), patient_uuid=patient_uuid.get_value())
        )
