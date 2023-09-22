from src.common.domain.services.access_policy import IsPatient
from src.common.application.queries.base import QueryHandler
from src.common.application.interfaces.identity_provider import IIdentityProvider
from src.common.application.exceptions.access import AccessDenied

from src.application.med_card.models.dto import MedCardDTO
from src.application.med_card.interfaces.med_card_db_gateway import IMedCardDBGateway


class GetMedCardQuery(QueryHandler):

    def __init__(
            self,
            db_gateway: IMedCardDBGateway,
            identity_provider: IIdentityProvider
    ):
        self._db_gateway = db_gateway
        self._identity_provider = identity_provider

    def __call__(self) -> MedCardDTO:
        can_get_med_card = IsPatient()
        access_policy = self._identity_provider.get_access_policy()
        if not can_get_med_card.is_satisfied_by(access_policy):
            raise AccessDenied(access_policy.user_uuid)

        med_card = self._db_gateway.med_card_reader.get_med_card_by_patient_or_med_card_uuid(
            patient_uuid=access_policy.user_uuid)

        return med_card
