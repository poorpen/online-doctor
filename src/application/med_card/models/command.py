from uuid import UUID
from typing import List
from dataclasses import dataclass

from src.common.application.models.comand import CommandObject


@dataclass(frozen=True)
class AddDoctorNote(CommandObject):
    patient_uuid: UUID
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
    answers: List[int]

