from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.common.application.models.dto import DTO


@dataclass(frozen=True)
class AnswerDTO(DTO):
    answer_name: str
    answer_id: int


@dataclass(frozen=True)
class AnamnesisVitaePointDTO(DTO):
    category_id: int
    category_name: str
    answers_names: List[str]


@dataclass(frozen=True)
class AnswersForCategory(DTO):
    category_id: int
    category_name: str
    answers: List[AnswerDTO]


# @dataclass(frozen=True)
# class MedCardPreviewDTO(DTO):
#     uuid: UUID
#     first_name: str
#     last_name: str
#     middle_name: str
#     date_of_birth: datetime
#     gender: str


@dataclass(frozen=True)
class MedCardDTO(DTO):
    uuid: UUID
    first_name: str
    last_name: str
    middle_name: str
    date_of_birth: datetime
    gender: str
    height: int
    weight: int
    anamnesis_vitae: List[AnamnesisVitaePointDTO]


@dataclass(frozen=True)
class DoctorNoteDTO(DTO):
    note_uuid: UUID
    anamnesis_morbi: str
    diagnosis: str
    treatment_plan: str


@dataclass(frozen=True)
class DoctorNotesDTO(DTO):
    doctor_uuid: UUID
    doctor_first_name: str
    doctor_last_name: str
    doctor_middle_name: str
    notes: List[DoctorNoteDTO]
