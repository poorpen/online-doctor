from uuid import uuid4, UUID
from typing import List, Optional
from dataclasses import dataclass, field

from src.common.domain.models.aggregate import AggregateRoot
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.models.doctor_note import DoctorNote
from src.domain.med_card.models.anamesis_vitae_point import AnamnesisVitaePoint
from src.domain.med_card.models.med_card_events import (
    MedCardCreatedEvent, DoctorNoteAddedEvent, AnswersUpdatedEvent, AnthropometryDataEdited)
from src.domain.med_card.value_objects.common import MedCardUUID
from src.domain.med_card.value_objects.doctor_note import AnamnesisMorbi, Diagnosis, TreatmentPlan, DoctorUUID
from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID
from src.domain.med_card.value_objects.med_card import (
    Height, Weight, PatientUUID, DateTimeOfBirth, FirstName, LastName, MiddleName)
from src.domain.med_card.enum.gender import Gender


@dataclass
class MedCard(AggregateRoot):
    uuid: UUIDVO
    patient_uuid: PatientUUID
    first_name: FirstName
    last_name: LastName
    middle_name: MiddleName
    datetime_of_birth: DateTimeOfBirth
    gender: Gender
    height: Height = field(default=Height(0))
    weight: Weight = field(default=Weight(0))
    anamnesis_vitae: List[AnamnesisVitaePoint] = field(default_factory=list)
    doctor_notes: List[DoctorNote] = field(default_factory=list)

    @classmethod
    def create_med_card(cls,
                        uuid: UUIDVO,
                        patient_uuid: PatientUUID,
                        first_name: FirstName,
                        last_name: LastName,
                        middle_name: MiddleName,
                        datetime_of_birth: DateTimeOfBirth,
                        gender: Gender) -> "MedCard":
        med_card = cls(
            uuid=uuid,
            patient_uuid=patient_uuid,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            datetime_of_birth=datetime_of_birth,
            gender=gender
        )
        med_card.record_event(
            MedCardCreatedEvent(
                med_card_uuid=uuid.get_value(),
                patient_uuid=patient_uuid.get_value(),
                first_name=first_name.get_value(),
                last_name=last_name.get_value(),
                middle_name=middle_name.get_value(),
                datetime_of_birth=datetime_of_birth.get_value()
            )
        )
        return med_card

    @property
    def get_patient_uuid(self) -> UUID:
        return self.patient_uuid.get_value()

    def add_doctor_note(
            self,
            doctor_uuid: DoctorUUID,
            anamnesis_morbi: AnamnesisMorbi,
            diagnosis: Diagnosis,
            treatment_plan: TreatmentPlan
    ) -> None:
        note_uuid = UUIDVO(uuid4())
        self.doctor_notes.append(
            DoctorNote(
                uuid=note_uuid,
                medcard_uuid=MedCardUUID(self.uuid.get_value()),
                doctor_uuid=doctor_uuid,
                anamnesis_morbi=anamnesis_morbi,
                diagnosis=diagnosis,
                treatment_plan=treatment_plan
            )
        )
        self.record_event(
            DoctorNoteAddedEvent(
                note_uuid=note_uuid.get_value(),
                med_card_uuid=self.uuid.get_value(),
                doctor_uuid=doctor_uuid.get_value()
            )
        )

    def update_answers_in_anamnesis_vitae(self, answers_ids: List[AnswerID], category_id: CategoryID) -> None:
        anamnesis_vitae_point = self._search_anamnesis_vitae_point(category_id)
        if not anamnesis_vitae_point:
            anamnesis_vitae_point = AnamnesisVitaePoint(medcard_uuid=MedCardUUID(self.uuid.get_value()),
                                                        category_id=category_id)
            self.anamnesis_vitae.append(anamnesis_vitae_point)
        anamnesis_vitae_point.update_answers(answers_ids)
        self.record_event(
            AnswersUpdatedEvent(
                med_card_uuid=self.uuid.get_value(),
                answers=[x.get_value() for x in answers_ids],
                category_id=category_id.get_value()
            )
        )

    def edit_anthropometry_data(self, weight: Optional[Weight] = None, height: Optional[Height] = None) -> None:
        if weight:
            self.weight = weight
        if height:
            self.height = height
        self.record_event(
            AnthropometryDataEdited(
                med_card_uuid=self.uuid.get_value(),
                weight=weight.get_value(),
                height=height.get_value()
            )
        )

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
