from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.application.exceptions.base import ApplicationException
from src.common.infrastructure.database.repositories.base import SQLAlchemyRepo

from src.domain.med_card.models.med_card import MedCard
from src.application.med_card.interfaces.med_card_repo import IMedCardRepo
from src.application.med_card.exceptions.med_card import MedCardNotFound
from src.infrastructure.database.models.med_card.med_card import MedCardDB
from src.infrastructure.database.converters.med_card import db_model_to_aggregate, aggregate_to_db_model


class MedCardRepo(SQLAlchemyRepo, IMedCardRepo):

    def add_med_card(self, med_card: MedCard) -> None:
        med_card_db = aggregate_to_db_model(med_card)
        self._session.add(med_card_db)
        try:
            self._session.flush()
        except IntegrityError as exc:
            self._parse_error(med_card, exc)

    def get_med_card_by_uuid(self, med_card_uuid: UUIDVO) -> MedCard:

        med_card_uuid_value = med_card_uuid.get_value()
        sql = select(MedCardDB).join(MedCardDB.anamnesis_vitae).where(MedCardDB.uuid == med_card_uuid_value)

        result = self._session.execute(sql)

        med_card = result.scalar()

        if not med_card:
            raise MedCardNotFound(med_card_uuid_value)

        return db_model_to_aggregate(med_card)

    def update_med_card(self, med_card: MedCard) -> None:
        med_card_db = aggregate_to_db_model(med_card)
        try:
            self._session.merge(med_card_db)
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
