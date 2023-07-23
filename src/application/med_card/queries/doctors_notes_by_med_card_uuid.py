from typing import List

from src.common.domain.services.access_policy import IsDoctor, IsPatient, UserUUIDMatches
from src.common.application.queries.base import QueryHandler
from src.common.application.interfaces.identity_provider import IdentityProvider
from src.common.application.exceptions.access import AccessDenied

from src.application.med_card.models.query import GetDoctorsNotes
from src.application.med_card.models.dto import DoctorNotes

from src.application.med_card.interfaces.med_card_db_gateway import MedCardDBGateway


class GetDoctorsNotesQuery(QueryHandler):

    def __init__(
            self,
            db_gateway: MedCardDBGateway,
            identity_provider: IdentityProvider
    ):
        self._db_gateway = db_gateway
        self._identity_provider = identity_provider

    def __call__(self, query_data: GetDoctorsNotes) -> List[DoctorNotes]:
        patient_uuid = self._db_gateway.med_card_reader.get_patient_uuid_by_med_card_uuid(query_data.med_card_uuid)

        can_get_doctors_notes = IsDoctor() | (IsPatient() & UserUUIDMatches(patient_uuid))
        access_policy = self._identity_provider.get_access_policy()
        if not can_get_doctors_notes.is_satisfied_by(access_policy):
            raise AccessDenied(access_policy.user_uuid)

        doctors_notes = self._db_gateway.med_card_reader.get_doctors_notes_by_med_card_uuid(query_data.med_card_uuid)
        return doctors_notes
