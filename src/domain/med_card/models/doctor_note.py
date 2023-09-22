from dataclasses import dataclass

from src.common.domain.models.entity import Entity
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.value_objects.common import FirstName, LastName, MiddleName
from src.domain.med_card.value_objects.doctor_note import AnamnesisMorbi, Diagnosis, TreatmentPlan, DoctorUUID


@dataclass
class DoctorNote(Entity):
    uuid: UUIDVO
    med_card_uuid: UUIDVO
    doctor_first_name: FirstName
    doctor_last_name: LastName
    doctor_middle_name: MiddleName
    doctor_uuid: DoctorUUID
    anamnesis_morbi: AnamnesisMorbi
    diagnosis: Diagnosis
    treatment_plan: TreatmentPlan
