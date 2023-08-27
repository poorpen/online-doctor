from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from src.common.domain.models.events import LoggingEvent


@dataclass
class MedCardCreatedEvent(LoggingEvent):
    med_card_uuid: UUID
    patient_uuid: UUID
    first_name: str
    last_name: str
    middle_name: str
    datetime_of_birth: datetime


@dataclass
class DoctorNoteAddedEvent(LoggingEvent):
    note_uuid: UUID
    med_card_uuid: UUID
    doctor_uuid: UUID


@dataclass
class AnswersUpdatedEvent(LoggingEvent):
    med_card_uuid: UUID
    answers: List[int]
    category_id: int


@dataclass
class AnthropometryDataEdited(LoggingEvent):
    med_card_uuid: UUID
    weight: int
    height: int


