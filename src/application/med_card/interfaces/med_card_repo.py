from typing import Protocol

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.models.med_card import MedCard


class IMedCardRepo(Protocol):

    def get_med_card_by_uuid(self, med_card_uuid: UUIDVO) -> MedCard:
        raise NotImplemented

    def update_med_card(self, med_card: MedCard) -> None:
        raise NotImplemented

    def add_med_card(self, med_card: MedCard) -> None:
        raise NotImplemented
