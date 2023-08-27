from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

from src.common.infrastructure.database.models.base import Base


class AnamnesisCategoryDB(Base):
    __tablename__ = 'anamnesis_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
