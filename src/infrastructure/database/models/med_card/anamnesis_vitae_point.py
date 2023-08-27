from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.infrastructure.database.models.base import Base

from src.infrastructure.database.models.med_card.answer import AnswerForAnamnesisDB
from src.infrastructure.database.models.med_card.category import AnamnesisCategoryDB


class AnamnesisVitaePointDB(Base):
    __tablename__ = 'anamnesis_vitae_point'

    med_card_uuid: Mapped[UUID] = mapped_column(ForeignKey('med_cards.uuid'), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('anamnesis_categories.id'), primary_key=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey('answers_for_anamnesis.id'), primary_key=True)
    category: Mapped["AnamnesisCategoryDB"] = relationship(lazy=None)
    answer: Mapped["AnswerForAnamnesisDB"] = relationship(lazy=None)
