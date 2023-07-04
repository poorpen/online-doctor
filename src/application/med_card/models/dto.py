from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.common.application.models.dto import DTO


@dataclass
class MedCardDTO(DTO):
    patient_uuid: UUID
    height: int
    weight: int
    date_of_birth: datetime


@dataclass
class AnamnesisVitaePoint(DTO):
    category_id: int
    category_name: str
    answers_names: List[str]


@dataclass
class Answer(DTO):
    answer_name: str
    answer_id: int
