from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String
from sqlalchemy import ForeignKey

from src.common.infrastructure.database.models.base import Base


class AnswerForAnamnesisDB(Base):
    __tablename__ = 'answers_for_anamnesis'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    category_id: Mapped[int] = mapped_column(ForeignKey('anamnesis_categories.id'))
