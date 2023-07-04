from typing import Protocol

from src.domain.med_card.models.med_card import MedCard
from src.domain.med_card.value_objects.med_card import PatientUUID


class MedCardRepo(Protocol):

    def get_med_card_by_patient_uuid(self, patient_uuid: PatientUUID) -> MedCard:
        raise NotImplemented

    def update_med_card(self, med_card: MedCard) -> None:
        raise NotImplemented
