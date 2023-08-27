from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from src.common.infrastructure.database.models.base import Base


class DoctorNoteDB(Base):
    __tablename__ = 'doctors_notes'

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    med_card_uuid: Mapped[UUID] = mapped_column(ForeignKey('med_cards.uuid'))
    doctor_uuid: Mapped[UUID] = mapped_column(ForeignKey('users.uuid'))
    anamnesis_morbi: Mapped[str] = mapped_column(String(350))
    diagnosis: Mapped[str] = mapped_column(String(350))
    treatment_plan: Mapped[str] = mapped_column(String(350))
    doctor = relationship("User")
