from uuid import uuid4
from typing import List, Optional
from dataclasses import dataclass, field

from src.common.domain.models.aggregate import AggregateRoot
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.models.doctor_note import DoctorNote
from src.domain.med_card.models.anamesis_vitae_point import AnamnesisVitaePoint
from src.domain.med_card.value_objects.common import MedCardUUID
from src.domain.med_card.value_objects.doctor_note import AnamnesisMorbi, Diagnosis, TreatmentPlan, DoctorUUID
from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID
from src.domain.med_card.value_objects.med_card import Height, Weight, PatientUUID, DateTimeOfBirth
from src.domain.med_card.exceptions.anamnesis_vitae_point import AnamnesisVitaePointNotExist


@dataclass
class MedCard(AggregateRoot):
    uuid: UUIDVO
    patient_uuid: PatientUUID
    height: Height
    weight: Weight
    date_of_birth: DateTimeOfBirth
    anamnesis_vitae: List[AnamnesisVitaePoint] = field(default_factory=list)
    doctor_notes: List[DoctorNote] = field(default_factory=list)

    def add_doctor_note(
            self,
            doctor_uuid: DoctorUUID,
            anamnesis_morbi: AnamnesisMorbi,
            diagnosis: Diagnosis,
            treatment_plan: TreatmentPlan
    ) -> None:
        self.doctor_notes.append(
            DoctorNote(
                uuid=UUIDVO(uuid4()),
                medcard_uuid=MedCardUUID(self.uuid.get_value()),
                doctor_uuid=doctor_uuid,
                anamnesis_morbi=anamnesis_morbi,
                diagnosis=diagnosis,
                treatment_plan=treatment_plan
            )
        )

    def add_answers_in_anamnesis_vitae(self, answers_ids: List[AnswerID], category_id: CategoryID) -> None:
        anamnesis_vitae_point = self._search_anamnesis_vitae_point(category_id)
        if not anamnesis_vitae_point:
            anamnesis_vitae_point = AnamnesisVitaePoint(medcard_uuid=MedCardUUID(self.uuid.get_value()),
                                                        category_id=category_id)
            anamnesis_vitae_point.add_answer(answers_ids)
            self.anamnesis_vitae.append(anamnesis_vitae_point)
        else:
            anamnesis_vitae_point.add_answer(answers_ids)

    def delete_answers_in_anamnesis_vitae(self, answers_ids: List[AnswerID], category_id: CategoryID) -> None:
        anamnesis_vitae_point = self._search_anamnesis_vitae_point(category_id)
        if not anamnesis_vitae_point:
            raise AnamnesisVitaePointNotExist(category_id)
        anamnesis_vitae_point.delete_answer(answers_ids)

    def edit_anthropometry_data(self, weight: Optional[Weight] = None, height: Optional[Height] = None) -> None:
        if weight:
            self.weight = weight
        if height:
            self.height = height

    def _search_anamnesis_vitae_point(self, category_id: CategoryID) -> AnamnesisVitaePoint | None:
        collection_to_search = sorted(self.anamnesis_vitae, key=lambda p: p.anamnesis_category_id)
        low = 0
        high = len(collection_to_search) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_item: AnamnesisVitaePoint = collection_to_search[mid]
            if mid_item.anamnesis_category_id == category_id:
                return mid_item
            elif mid_item.anamnesis_category_id < category_id:
                low = mid + 1
            elif mid_item.anamnesis_category_id > category_id:
                high = mid - 1
