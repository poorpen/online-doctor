from src.common.application.queries.base import QueryHandler

from src.application.med_card.models.query import GetAnswersForCategory
from src.application.med_card.models.dto import AnswersForCategory
from src.application.med_card.interfaces.med_card_db_gateway import IMedCardDBGateway


class GetAnswersForCategoryQuery(QueryHandler):

    def __init__(
            self,
            db_gateway: IMedCardDBGateway,
    ):
        self._db_gateway = db_gateway

    def __call__(self, query_data: GetAnswersForCategory) -> AnswersForCategory:
        return self._db_gateway.med_card_reader.get_answers_for_anamnesis_vitae(query_data.category_id)
