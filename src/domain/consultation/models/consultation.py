from dataclasses import dataclass
from datetime import datetime, timedelta

from src.common.domain.models.aggregate import AggregateRoot
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.consultation.value_objects.consultation import PatientUUID, DoctorUUID, StartConsultationDateTime
from src.domain.consultation.enum.consultation_status import ConsultationStatus
from src.domain.consultation.exceptions.consultation import ConsultationFinished


@dataclass
class Consultation(AggregateRoot):
    uuid: UUIDVO
    patient_uuid: PatientUUID
    doctor_uuid: DoctorUUID
    start_datetime: StartConsultationDateTime
    status: ConsultationStatus

    def finish_consultation(self) -> None:
        if self.status == ConsultationStatus.FINISHED:
            raise ConsultationFinished(self.uuid)
        self.status = ConsultationStatus.FINISHED
