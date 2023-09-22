from uuid import uuid4, UUID
from typing import List, Optional
from dataclasses import dataclass, field

from src.common.domain.models.aggregate import AggregateRoot
from src.common.domain.value_objects.identifiers import UUIDVO, ID
from src.common.domain.utils.binary_search import binary_search

from src.domain.med_card.models.doctor_note import DoctorNote
from src.domain.med_card.models.anamesis_vitae_point import AnamnesisVitaePoint
from src.domain.med_card.models.med_card_events import (
    MedCardCreatedEvent, DoctorNoteAddedEvent, AnswersUpdatedEvent, AnthropometryDataEdited)
from src.domain.med_card.value_objects.common import FirstName, LastName, MiddleName
from src.domain.med_card.value_objects.doctor_note import AnamnesisMorbi, Diagnosis, TreatmentPlan, DoctorUUID
from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID
from src.domain.med_card.value_objects.med_card import Height, Weight, PatientUUID, DateTimeOfBirth
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
    deleted: bool = field(default=False)
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
        self._check_delete()
        return self.patient_uuid.get_value()

    def add_doctor_note(
            self,
            doctor_uuid: DoctorUUID,
            anamnesis_morbi: AnamnesisMorbi,
            diagnosis: Diagnosis,
            treatment_plan: TreatmentPlan,
            doctor_first_name: FirstName,
            doctor_middle_name: MiddleName,
            doctor_last_name: LastName
    ) -> None:
        self._check_delete()
        note_uuid = UUIDVO(uuid4())
        self.doctor_notes.append(
            DoctorNote(
                uuid=note_uuid,
                med_card_uuid=self.uuid,
                doctor_uuid=doctor_uuid,
                anamnesis_morbi=anamnesis_morbi,
                diagnosis=diagnosis,
                treatment_plan=treatment_plan,
                doctor_first_name=doctor_first_name,
                doctor_middle_name=doctor_middle_name,
                doctor_last_name=doctor_last_name
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
        self._check_delete()

        anamnesis_vitae_point = self._search_anamnesis_vitae_point(category_id)

        if not anamnesis_vitae_point:
            anamnesis_vitae_point = AnamnesisVitaePoint(
                uuid=UUIDVO(uuid4()),
                med_card_uuid=self.uuid,
                category_id=category_id,
                answers_ids=[]
            )
            self.anamnesis_vitae.append(anamnesis_vitae_point)

        anamnesis_vitae_point.update_answers(answers_ids)
        self.record_event(
            AnswersUpdatedEvent(
                med_card_uuid=self.uuid.get_value(),
                answers=[x.get_value() for x in answers_ids],
                category_id=category_id.get_value()
            )
        )

    def edit_anthropometry_data(self, weight: Weight, height: Height) -> None:
        self._check_delete()
        if weight.get_value():
            self.weight = weight
        if height.get_value():
            self.height = height
        self.record_event(
            AnthropometryDataEdited(
                med_card_uuid=self.uuid.get_value(),
                weight=self.weight.get_value(),
                height=self.height.get_value()
            )
        )

    def delete_med_card(self):
        self._check_delete()
        self.deleted = True

    def _check_delete(self) -> None:
        if self.deleted:
            raise Exception

    def _search_anamnesis_vitae_point(self, category_id: CategoryID) -> AnamnesisVitaePoint:
        collection_to_search = sorted(self.anamnesis_vitae, key=lambda p: p.anamnesis_category_id)
        return binary_search(
            collection_to_search,
            category_id,
            lambda vitae_point: vitae_point.anamnesis_category_id
        )
