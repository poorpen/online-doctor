from dataclasses import dataclass
from datetime import datetime, timedelta

from src.common.domain.models.aggregate import AggregateRoot
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.consultation.value_objects.consultation import PatientUUID, DoctorUUID, ConsultationDateTime
from src.domain.consultation.models.consultation_events import ConsultationScheduled
from src.domain.consultation.enum.consultation_status import ConsultationStatus
from src.domain.consultation.exceptions.consultation import ConsultationFinished, CantCancelConsultation, \
    ConsultationCanceled, CantStartConsultation, CantMakeAnAppointment, ConsultationNotStarted, ConsultationInProcess


@dataclass
class Consultation(AggregateRoot):
    uuid: UUIDVO
    patient_uuid: PatientUUID
    doctor_uuid: DoctorUUID
    consultation_datetime: ConsultationDateTime
    status: ConsultationStatus

    @classmethod
    def scheduled_a_consultation(cls,
                                 uuid: UUIDVO,
                                 patient_uuid: PatientUUID,
                                 doctor_uuid: DoctorUUID,
                                 consultation_datetime: ConsultationDateTime
                                 ) -> "Consultation":
        if consultation_datetime < datetime.utcnow() - timedelta(minutes=1):
            raise CantMakeAnAppointment(consultation_datetime)
        consultation = cls(
            uuid=uuid,
            patient_uuid=patient_uuid,
            doctor_uuid=doctor_uuid,
            consultation_datetime=consultation_datetime,
            status=ConsultationStatus.SCHEDULED
        )
        consultation.record_event(
            ConsultationScheduled(
                consultation_datetime.get_value()
            )
        )
        return consultation

    def cancel_scheduled_consultation(self) -> None:
        self._check_consultation_finish_or_canceled()
        if self.status == ConsultationStatus.IN_PROCESS:
            raise ConsultationInProcess(self.uuid)
        elif self.consultation_datetime - datetime.utcnow() < timedelta(hours=24):
            raise CantCancelConsultation(self.consultation_datetime)
        self.status = ConsultationStatus.CANCELED

    def start_consultation(self) -> None:
        self._check_consultation_finish_or_canceled()
        if self.consultation_datetime < datetime.utcnow() - timedelta(
                minutes=5) or self.consultation_datetime > datetime.utcnow() + timedelta(minutes=5):
            raise CantStartConsultation(self.consultation_datetime)
        elif self.status == ConsultationStatus.IN_PROCESS:
            raise ConsultationInProcess(self.uuid)
        self.status = ConsultationStatus.IN_PROCESS

    def finish_consultation(self) -> None:
        self._check_consultation_finish_or_canceled()
        if self.status == ConsultationStatus.SCHEDULED:
            raise ConsultationNotStarted(self.uuid)
        self.status = ConsultationStatus.FINISHED

    def _check_consultation_finish_or_canceled(self) -> None:
        if self.status == ConsultationStatus.FINISHED:
            raise ConsultationFinished(self.uuid)
        elif self.status == ConsultationStatus.CANCELED:
            raise ConsultationCanceled(self.uuid)
