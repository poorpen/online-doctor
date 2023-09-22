from typing import Optional, List
from uuid import UUID

from sqlalchemy import select

from src.common.infrastructure.database.repositories.base import SQLAlchemyRepo

from src.application.med_card.interfaces.med_card_reader import IMedCardReader
from src.application.med_card.models.dto import MedCardDTO, AnswersForCategory, DoctorNotesDTO
from src.application.med_card.exceptions.med_card import MedCardNotFound, AnswersForCurrentCategoryNotFound, \
    DoctorNotesNotFound

from src.infrastructure.database.models.med_card.doctor_note import doctor_note
from src.infrastructure.database.models.med_card.anamnesis_vitae_point import (
    answer_for_category, anamnesis_category)
from src.infrastructure.database.repositories.med_card.query_builder import MedCardQueryBuilder
from src.infrastructure.database.converters.med_card import (
    to_med_card_dto, to_answer_for_category_dto, to_doctor_notes_dto)


class MedCardReader(SQLAlchemyRepo, IMedCardReader):

    def get_med_card_by_patient_or_med_card_uuid(
            self,
            patient_uuid: Optional[UUID] = None,
            med_card_uuid: Optional[UUID] = None
    ) -> MedCardDTO:

        stmt = (
            MedCardQueryBuilder()
            .by_med_card_or_patient_uuid(patient_uuid, med_card_uuid)
            .with_anamnesis_vitae_point()
            .with_names_categories()
            .with_names_answers()
            .build())

        result = self._session.execute(stmt)
        mapped_result = result.mappings().all()

        if not mapped_result:
            raise MedCardNotFound(patient_uuid if patient_uuid else med_card_uuid)

        return to_med_card_dto(mapped_result)

    def get_answers_for_anamnesis_vitae(self, category_id: int) -> AnswersForCategory:
        sql = (select(anamnesis_category.c.id.label('category_id'),
                      anamnesis_category.c.name.label('category_name'),
                      answer_for_category.c.id.label('answer_id'),
                      answer_for_category.c.name.label('answer_name'))
               .where(anamnesis_category.c.id == category_id)
               .join(answer_for_category))

        result = self._session.execute(sql)

        mapped_result = result.mappings().all()

        if not mapped_result:
            raise AnswersForCurrentCategoryNotFound(category_id)

        return to_answer_for_category_dto(mapped_result)

    def get_doctors_notes_by_med_card_uuid(self, med_card_uuid: UUID) -> List[DoctorNotesDTO]:
        sql = select(doctor_note).where(doctor_note.c.med_card_uuid == med_card_uuid)

        result = self._session.execute(sql)

        mapped_result = result.mappings().all()

        if not mapped_result:
            raise DoctorNotesNotFound(med_card_uuid)

        return to_doctor_notes_dto(mapped_result)
