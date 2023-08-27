from typing import Optional, List
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common.infrastructure.database.repositories.base import SQLAlchemyRepo

from src.application.med_card.interfaces.med_card_reader import IMedCardReader
from src.application.med_card.models.dto import MedCardPreviewDTO, MedCardDTO, AnswersForCategory, DoctorNotesDTO
from src.application.med_card.exceptions.med_card import MedCardNotFound, AnswersForCurrentCategoryNotFound, DoctorNotesNotFound

from src.infrastructure.database.models.med_card.answer import AnswerForAnamnesisDB
from src.infrastructure.database.models.med_card.category import AnamnesisCategoryDB
from src.infrastructure.database.models.med_card.doctor_note import DoctorNoteDB
from src.infrastructure.database.models.med_card.med_card import MedCardDB
from src.infrastructure.database.converters.med_card import db_model_to_dto, db_answers_model_to_dto, \
    db_doctors_notes_to_dto


class MedCardReader(SQLAlchemyRepo, IMedCardReader):

    def __init__(self, session: Session, query_builder):
        super().__init__(session)
        self.query_builder = query_builder

    def search_med_card(
            self,
            fist_name: Optional[str] = None,
            last_name: Optional[str] = None,
            middle_name: Optional[str] = None,
            datetime_of_birth: Optional[datetime] = None,
            gender: Optional[str] = None
    ) -> List[MedCardPreviewDTO]:
        pass

    def get_med_card_by_med_card_or_patient_uuid(
            self,
            patient_uuid: Optional[UUID] = None,
            med_card_uuid: Optional[UUID] = None
    ) -> MedCardDTO:
        sql = select(MedCardDB)

        if patient_uuid:
            sql = sql.where(MedCardDB.patient_uuid == patient_uuid)
            identity = patient_uuid
        else:
            sql = sql.where(MedCardDB.uuid == med_card_uuid)
            identity = med_card_uuid

        result = self._session.execute(sql)

        med_card = result.scalar()

        if not med_card:
            raise MedCardNotFound(identity)

        return db_model_to_dto(med_card)

    def get_answers_for_anamnesis_vitae(self, category_id: int) -> AnswersForCategory:
        sql = select(AnamnesisCategoryDB, AnswerForAnamnesisDB).where(
            AnswerForAnamnesisDB.category_id == category_id
        ).join(
            AnamnesisCategoryDB, AnamnesisCategoryDB.id == AnswerForAnamnesisDB.category_id
        )

        result = self._session.execute(sql)

        answers = result.all()

        if not answers:
            raise AnswersForCurrentCategoryNotFound(category_id)

        return db_answers_model_to_dto(answers)

    def get_doctors_notes_by_med_card_uuid(self, med_card_uuid: UUID) -> List[DoctorNotesDTO]:
        sql = select(DoctorNoteDB).where(DoctorNoteDB.med_card_uuid == med_card_uuid)

        result = self._session.execute(sql)

        notes = result.scalars().all()

        if not notes:
            raise DoctorNotesNotFound(med_card_uuid)

        return db_doctors_notes_to_dto(notes)

    def get_patient_uuid_by_med_card_uuid(self, med_card_uuid: UUID) -> UUID:
        sql = select(MedCardDB.patient_uuid).where(MedCardDB.uuid == med_card_uuid)

        result = self._session.execute(sql)

        return result.scalar()
