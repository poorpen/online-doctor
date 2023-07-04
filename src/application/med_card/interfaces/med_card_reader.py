from typing import Protocol, List
from uuid import UUID

from src.application.med_card.models.dto import MedCardDTO, AnamnesisVitaePoint, Answer


class MedCardReader(Protocol):

    def get_med_card_by_patient_uuid(self, patient_uuid: UUID) -> MedCardDTO:
        raise NotImplemented

    def get_anamnesis_vitae_by_patient_uuid(self, patient_uuid: UUID) -> List[AnamnesisVitaePoint]:
        raise NotImplemented

    def get_answers_for_anamnesis_vitae(self, category_id) -> List[Answer]:
        raise NotImplemented
