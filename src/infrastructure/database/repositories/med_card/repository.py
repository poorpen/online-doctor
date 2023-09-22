from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.application.exceptions.base import ApplicationException
from src.common.infrastructure.database.repositories.base import SQLAlchemyRepo

from src.domain.med_card.models.med_card import MedCard
from src.application.med_card.interfaces.med_card_repo import IMedCardRepo
from src.application.med_card.exceptions.med_card import MedCardNotFound


class MedCardRepo(SQLAlchemyRepo, IMedCardRepo):

    def add_med_card(self, med_card: MedCard) -> None:
        self._session.add(med_card)
        try:
            self._session.flush()
        except IntegrityError as exc:
            self._parse_error(med_card, exc)

    def get_med_card_by_uuid(self, med_card_uuid: UUIDVO) -> MedCard:

        sql = select(MedCard).options(selectinload(MedCard.anamnesis_vitae)).where(MedCard.uuid == med_card_uuid)

        result = self._session.execute(sql)

        med_card = result.scalar()

        if not med_card:
            raise MedCardNotFound(med_card_uuid.get_value())

        return med_card

    def update_med_card(self, med_card: MedCard) -> None:
        try:
            self._session.merge(med_card)
            self._session.flush()
        except IntegrityError as exc:
            self._parse_error(med_card, exc)

    def _parse_error(self, model: MedCard, exception: IntegrityError) -> ApplicationException:
        field = exception.__cause__.diag.constraint_name
        if field == '':
            ...
        elif field == '':
            ...
        elif field == '':
            ...
        else:
            ...
