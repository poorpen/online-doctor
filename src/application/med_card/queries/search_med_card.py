from typing import List

from src.common.domain.services.access_policy import IsDoctor
from src.common.application.queries.base import QueryHandler
from src.common.application.interfaces.identity_provider import IdentityProvider
from src.common.application.exceptions.access import AccessDenied

from src.application.med_card.models.query import SearchMedCard
from src.application.med_card.models.dto import MedCardDTO
from src.application.med_card.interfaces.med_card_db_gateway import MedCardDBGateway


class SearchMedCardQuery(QueryHandler):

    def __init__(
            self,
            db_gateway: MedCardDBGateway,
            identity_provider: IdentityProvider
    ):
        self._db_gateway = db_gateway
        self._identity_provider = identity_provider

    def __call__(self, query_data: SearchMedCard) -> List[MedCardDTO]:
        can_search_med_card = IsDoctor()
        access_policy = self._identity_provider.get_access_policy()
        if not can_search_med_card.is_satisfied_by(access_policy):
            raise AccessDenied(access_policy.user_uuid)

        med_cards = self._db_gateway.med_card_reader.search_med_card(
            fist_name=query_data.fist_name,
            last_name=query_data.last_name,
            middle_name=query_data.middle_name,
            datetime_of_birth=query_data.datetime_of_birth
        )

        return med_cards
