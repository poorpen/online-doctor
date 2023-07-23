from src.common.domain.services.access_policy import IsDoctor
from src.common.application.queries.base import QueryHandler
from src.common.application.interfaces.identity_provider import IdentityProvider
from src.common.application.exceptions.access import AccessDenied

from src.application.med_card.models.query import GetPersonalMedCardInfo
from src.application.med_card.models.dto import PersonalInfoMedCardDTO
from src.application.med_card.interfaces.med_card_db_gateway import MedCardDBGateway


class GetPersonalInfoFromMedCardQuery(QueryHandler):

    def __init__(
            self,
            db_gateway: MedCardDBGateway,
            identity_provider: IdentityProvider
    ):
        self._db_gateway = db_gateway
        self._identity_provider = identity_provider

    def __call__(self, query_data: GetPersonalMedCardInfo) -> PersonalInfoMedCardDTO:
        can_get_med_card = IsDoctor()

        access_policy = self._identity_provider.get_access_policy()
        if not can_get_med_card.is_satisfied_by(access_policy):
            raise AccessDenied(access_policy.user_uuid)

        med_card = self._db_gateway.med_card_reader.get_personal_info_in_med_card_by_patient_uuid(
            patient_uuid=query_data.patient_uuid)

        return med_card
