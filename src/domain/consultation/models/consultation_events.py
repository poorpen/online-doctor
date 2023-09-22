from uuid import UUID
from dataclasses import dataclass
from datetime import datetime

from src.common.domain.models.events import DomainEvent


@dataclass(frozen=True)
class ConsultationActive(DomainEvent):
    doctor_uuid: UUID
    patient_uuid: UUID


@dataclass(frozen=True)
class ConsultationScheduled(DomainEvent):
    consultation_datetime: datetime
