from uuid import UUID

from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.specifications.base import Specification

from src.common.application.commands.base import CommandHandler
from src.common.application.interfaces.identity_provider import IdentityProvider
from src.common.application.exceptions.access import AccessDenied

from src.domain.med_card.value_objects.doctor_note import TreatmentPlan, Diagnosis, DoctorUUID, AnamnesisMorbi

from src.application.med_card.models.command import AddDoctorNote
from src.application.med_card.interfaces.med_card_db_gateway import MedCardDBGateway


class AddDoctorNoteCommand(CommandHandler):

    def __init__(self, db_gateway: MedCardDBGateway, identity_provider: IdentityProvider, can_add_note: Specification):
        self._db_gateway = db_gateway
        self._can_add_note = can_add_note
        self._identity_provider = identity_provider

    def __call__(self, command_data: AddDoctorNote) -> None:
        access_policy = self._identity_provider.get_access_policy()

        if not self._can_add_note.is_satisfied_by(access_policy):
            raise AccessDenied()

        doctor_uuid = DoctorUUID(access_policy.user_uuid)
        patient_uuid = UUIDVO(command_data.patient_uuid)
        anamnesis_morbi = AnamnesisMorbi(command_data.anamnesis_morbi)
        diagnosis = Diagnosis(command_data.diagnosis)
        treatment_plan = TreatmentPlan(command_data.treatment_plan)

        med_card_aggregate = self._db_gateway.med_card_repo.get_med_card_by_patient_uuid(patient_uuid)

        med_card_aggregate.add_doctor_note(
            doctor_uuid=doctor_uuid,
            anamnesis_morbi=anamnesis_morbi,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan
        )

        self._db_gateway.med_card_repo.update_med_card(med_card_aggregate)
        self._db_gateway.commit()
