from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.common.application.models.dto import DTO


@dataclass(frozen=True)
class Answer(DTO):
    answer_name: str
    answer_id: int


@dataclass(frozen=True)
class AnamnesisVitaePoint(DTO):
    category_id: int
    category_name: str
    answers_names: List[str]


@dataclass(frozen=True)
class AnswersForCategory(DTO):
    category_name: str
    answers: List[Answer]


@dataclass(frozen=True)
class PersonalInfoMedCardDTO(DTO):
    med_card_uuid: UUID
    patient_uuid: UUID
    first_name: str
    last_name: str
    middle_name: str
    date_of_birth: datetime
    gender: str


@dataclass(frozen=True)
class MedCardDTO(PersonalInfoMedCardDTO):
    height: int
    weight: int
    anamnesis_vitae: List[AnamnesisVitaePoint]


@dataclass(frozen=True)
class DoctorNoteDTO(DTO):
    anamnesis_morbi: str
    diagnosis: str
    treatment_plan: str


@dataclass(frozen=True)
class DoctorNotes(DTO):
    doctor_first_name: str
    doctor_last_name: str
    doctor_middle_name: str
    notes: List[DoctorNoteDTO]
