from uuid import UUID
from dataclasses import dataclass

from src.common.domain.models.event import Event


@dataclass(frozen=True)
class ConsultationActive(Event):
    doctor_uuid: UUID
    patient_uuid: UUID
