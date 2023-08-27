from dataclasses import dataclass

from src.common.domain.models.entity import Entity
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.value_objects.common import MedCardUUID
from src.domain.med_card.value_objects.doctor_note import AnamnesisMorbi, Diagnosis, TreatmentPlan, DoctorUUID


@dataclass
class DoctorNote(Entity):
    uuid: UUIDVO
    med_card_uuid: MedCardUUID
    doctor_uuid: DoctorUUID
    anamnesis_morbi: AnamnesisMorbi
    diagnosis: Diagnosis
    treatment_plan: TreatmentPlan
