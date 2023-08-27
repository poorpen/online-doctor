from typing import Protocol, Optional, List
from datetime import datetime
from uuid import UUID

from src.application.med_card.models.dto import MedCardPreviewDTO, AnswersForCategory, MedCardDTO, DoctorNotesDTO


class IMedCardReader(Protocol):

    def search_med_card(self,
                        fist_name: Optional[str] = None,
                        last_name: Optional[str] = None,
                        middle_name: Optional[str] = None,
                        datetime_of_birth: Optional[datetime] = None,
                        gender: Optional[str] = None) -> List[MedCardPreviewDTO]:
        raise NotImplemented

    def get_med_card_by_med_card_or_patient_uuid(self, patient_uuid: Optional[UUID] = None,
                                                 med_card_uuid: Optional[UUID] = None) -> MedCardDTO:
        raise NotImplemented

    def get_answers_for_anamnesis_vitae(self, category_id: int) -> AnswersForCategory:
        raise NotImplemented

    def get_patient_uuid_by_med_card_uuid(self, med_card_uuid: UUID) -> UUID:
        raise NotImplemented

    def get_doctors_notes_by_med_card_uuid(self, med_card_uuid: UUID) -> List[DoctorNotesDTO]:
        raise NotImplemented
