from uuid import UUID
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from src.common.infrastructure.database.models.base import Base

from src.domain.med_card.enum.gender import Gender
from src.infrastructure.database.models.med_card.anamnesis_vitae_point import AnamnesisVitaePointDB
from src.infrastructure.database.models.med_card.doctor_note import DoctorNoteDB


class MedCardDB(Base):
    __tablename__ = 'med_cards'

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    patient_uuid: Mapped[UUID] = mapped_column(ForeignKey('users.uuid'))
    first_name: Mapped[str] = mapped_column(String(60))
    last_name: Mapped[str] = mapped_column(String(60))
    middle_name: Mapped[str] = mapped_column(String(60))
    datetime_of_birth: Mapped[datetime]
    gender: Mapped[Gender]
    height: Mapped[int]
    weight: Mapped[int]
    deleted: Mapped[bool] = mapped_column(default=False)
    anamnesis_vitae: Mapped[List["AnamnesisVitaePointDB"]] = relationship(lazy=None)
    doctor_notes: Mapped[List["DoctorNoteDB"]] = relationship(lazy=None)

