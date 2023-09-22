from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.sql.selectable import Select

from src.common.infrastructure.database.repositories.query_builder import BaseQueryBuilder

from src.infrastructure.database.models.med_card.anamnesis_vitae_point import (
    anamnesis_vitae_point, anamnesis_category, answer_for_anamnesis_point, answer_for_category)
from src.infrastructure.database.models.med_card.med_card import med_card


class AnamnesisQueryBuilder(BaseQueryBuilder):

    def __init__(self, med_card_query: Select):
        super().__init__(med_card_query)

    def with_names_categories(self) -> "AnamnesisQueryBuilder":
        self._query = self._query.add_columns(
            anamnesis_category.c.name.label('category_name')
        ).join(anamnesis_category, anamnesis_category.c.id == anamnesis_vitae_point.c.category_id)
        return self

    def with_names_answers(self) -> "AnamnesisQueryBuilder":
        self._query = self._query.add_columns(
            answer_for_category.c.name.label('answer_name')
        ).join(answer_for_category, answer_for_category.c.id == answer_for_anamnesis_point.c.answer_id)
        return self


class MedCardQueryBuilder(BaseQueryBuilder):

    def __init__(self):
        super().__init__(select(med_card.c.uuid.label('med_card_uuid'), med_card).select_from(med_card))

    def with_anamnesis_vitae_point(self) -> AnamnesisQueryBuilder:
        return AnamnesisQueryBuilder(
            self._query.add_columns(
                anamnesis_vitae_point.c.uuid.label('anamnesis_uuid'),
                anamnesis_vitae_point.c.category_id,
                answer_for_anamnesis_point.c.answer_id
            ).join(anamnesis_vitae_point).join(answer_for_anamnesis_point)
        )

    def by_med_card_uuid(self, uuid: UUID) -> "MedCardQueryBuilder":
        self._query = self._query.where(med_card.c.uuid == uuid)
        return self

    def by_patient_uuid(self, uuid: UUID) -> "MedCardQueryBuilder":
        self._query = self._query.where(med_card.c.patient_uuid == uuid)
        return self

    def by_med_card_or_patient_uuid(self,
                                    patient_uuid: Optional[UUID] = None,
                                    med_card_uuid: Optional[UUID] = None
                                    ) -> "MedCardQueryBuilder":
        if patient_uuid:
            self.by_patient_uuid(patient_uuid)
        else:
            self.by_med_card_uuid(med_card_uuid)

        return self
