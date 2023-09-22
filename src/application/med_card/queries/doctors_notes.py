from typing import List

from src.common.domain.services.access_policy import IsPatient
from src.common.application.queries.base import QueryHandler
from src.common.application.interfaces.identity_provider import IIdentityProvider
from src.common.application.exceptions.access import AccessDenied

from src.application.med_card.models.query import GetDoctorsNotes
from src.application.med_card.models.dto import DoctorNotesDTO

from src.application.med_card.interfaces.med_card_db_gateway import IMedCardDBGateway


class GetDoctorsNotesQuery(QueryHandler):

    def __init__(
            self,
            db_gateway: IMedCardDBGateway,
            identity_provider: IIdentityProvider
    ):
        self._db_gateway = db_gateway
        self._identity_provider = identity_provider

    def __call__(self, query_data: GetDoctorsNotes) -> List[DoctorNotesDTO]:
        can_get_doctors_notes = IsPatient()
        access_policy = self._identity_provider.get_access_policy()
        if not can_get_doctors_notes.is_satisfied_by(access_policy):
            raise AccessDenied(access_policy.user_uuid)

        med_card_uuid = self._db_gateway.med_card_reader.get_med_card_uuid_by_patient_uuid(access_policy.user_uuid)
        doctors_notes = self._db_gateway.med_card_reader.get_doctors_notes_by_med_card_uuid(med_card_uuid)

        return doctors_notes
