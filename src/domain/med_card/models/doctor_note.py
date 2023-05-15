from uuid import UUID
from dataclasses import dataclass

from src.domain.common.models.entity import Entity

from src.domain.med_card.value_objects.doctor_note import AnamnesisMorbi, Diagnosis, TreatmentPlan


@dataclass
class DoctorNote(Entity):
    uuid: UUID
    medcard_uuid: UUID
    doctor_uuid: UUID
    anamnesis_morbi: AnamnesisMorbi
    diagnosis: Diagnosis
    treatment_plan: TreatmentPlan

