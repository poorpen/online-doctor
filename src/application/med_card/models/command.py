from uuid import UUID
from typing import List
from datetime import datetime
from dataclasses import dataclass

from src.common.application.models.comand import CommandObject


@dataclass(frozen=True)
class CreateMedCard(CommandObject):
    patient_uuid: UUID
    first_name: str
    last_name: str
    middle_name: str
    datetime_of_birth: datetime
    gender: str


@dataclass(frozen=True)
class AddDoctorNote(CommandObject):
    med_card_uuid: UUID
    anamnesis_morbi: str
    diagnosis: str
    treatment_plan: str


@dataclass(frozen=True)
class EditAnthropometryData(CommandObject):
    med_card_uuid: UUID
    weight: int | None = None
    height: int | None = None


@dataclass(frozen=True)
class UpdateAnswersInAnamnesis(CommandObject):
    med_card_uuid: UUID
    category_id: int
    answers: List[int]
