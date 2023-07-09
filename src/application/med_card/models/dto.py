from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.common.application.models.dto import DTO


@dataclass(frozen=True)
class AnamnesisVitaePoint(DTO):
    category_id: int
    category_name: str
    answers_names: List[str]


@dataclass(frozen=True)
class Answer(DTO):
    answer_name: str
    answer_id: int


@dataclass(frozen=True)
class MedCardDTO(DTO):
    patient_uuid: UUID
    height: int
    weight: int
    date_of_birth: datetime
    anamnesis_vitae: List[AnamnesisVitaePoint]
