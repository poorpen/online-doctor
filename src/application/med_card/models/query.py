from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.common.application.models.query import Query


@dataclass(frozen=True)
class GetMedCard(Query):
    med_card_uuid: UUID
    patient_uuid: UUID


@dataclass(frozen=True)
class SearchMedCard(Query):
    fist_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    datetime_of_birth: Optional[datetime] = None
    gender: Optional[str] = None


@dataclass(frozen=True)
class GetAnswersForCategory(Query):
    category_id: int


@dataclass(frozen=True)
class GetDoctorsNotes(Query):
    med_card_uuid: UUID
