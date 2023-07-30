from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.services.access_policy import IsDoctor

from src.common.application.commands.base import CommandHandler
from src.common.application.interfaces.identity_provider import IIdentityProvider
from src.common.application.interfaces.mediator import IMediator
from src.common.application.exceptions.access import AccessDenied

from src.domain.med_card.value_objects.doctor_note import TreatmentPlan, Diagnosis, DoctorUUID, AnamnesisMorbi

from src.application.med_card.models.command import AddDoctorNote
from src.application.med_card.interfaces.med_card_db_gateway import IMedCardDBGateway
from src.application.med_card.exceptions.med_card import MedCardNotFound, DoctorNotFound


class AddDoctorNoteCommand(CommandHandler):

    def __init__(self, db_gateway: IMedCardDBGateway, identity_provider: IIdentityProvider, mediator: IMediator):
        self._db_gateway = db_gateway
        self._identity_provider = identity_provider
        self._mediator = mediator

    def __call__(self, command_data: AddDoctorNote) -> None:
        access_policy = self._identity_provider.get_access_policy()
        can_add_note = IsDoctor()
        if not can_add_note.is_satisfied_by(access_policy):
            raise AccessDenied(access_policy.user_uuid)

        med_card_uuid = UUIDVO(command_data.med_card_uuid)
        doctor_uuid = DoctorUUID(access_policy.user_uuid)
        anamnesis_morbi = AnamnesisMorbi(command_data.anamnesis_morbi)
        diagnosis = Diagnosis(command_data.diagnosis)
        treatment_plan = TreatmentPlan(command_data.treatment_plan)

        med_card_aggregate = self._db_gateway.med_card_repo.get_med_card_by_uuid(med_card_uuid)

        med_card_aggregate.add_doctor_note(
            doctor_uuid=doctor_uuid,
            anamnesis_morbi=anamnesis_morbi,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan
        )

        self._mediator.publish(
            med_card_aggregate.pull_events()
        )

        try:
            self._db_gateway.med_card_repo.update_med_card(med_card_aggregate)
            self._db_gateway.commit()
        except (MedCardNotFound, DoctorNotFound):
            self._db_gateway.rollback()
