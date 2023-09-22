from uuid import uuid4, UUID

from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.services.access_policy import IsPatient
from src.common.application.commands.base import CommandHandler
from src.common.application.interfaces.identity_provider import IIdentityProvider
from src.common.application.interfaces.mediator import IMediator
from src.common.application.exceptions.access import AccessDenied

from src.domain.med_card.models.med_card import MedCard
from src.domain.med_card.value_objects.med_card import FirstName, LastName, MiddleName, DateTimeOfBirth, PatientUUID
from src.domain.med_card.enum.gender import Gender
from src.application.med_card.interfaces.med_card_db_gateway import IMedCardDBGateway
from src.application.med_card.models.command import CreateMedCard
from src.application.med_card.exceptions.med_card import CurrentPatientAlreadyHaveMedCard, PatientNotFound


class CreateMedCardCommand(CommandHandler):

    def __init__(self, db_gateway: IMedCardDBGateway, identity_provider: IIdentityProvider, mediator: IMediator):
        self._db_gateway = db_gateway
        self._identity_provider = identity_provider
        self._mediator = mediator

    def __call__(self, command_data: CreateMedCard) -> None:
        access_policy = self._identity_provider.get_access_policy()
        can_create_med_card = IsPatient()
        if not can_create_med_card.is_satisfied_by(access_policy):
            raise AccessDenied(access_policy.user_uuid)

        med_card_uuid = UUIDVO(uuid4())
        patient_uuid = PatientUUID(access_policy.user_uuid)
        first_name = FirstName(command_data.first_name)
        last_name = LastName(command_data.last_name)
        middle_name = MiddleName(command_data.middle_name)
        datetime_of_birth = DateTimeOfBirth(command_data.datetime_of_birth)
        gender = Gender(command_data.gender)

        med_card = MedCard.create_med_card(
            uuid=med_card_uuid,
            patient_uuid=patient_uuid,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            datetime_of_birth=datetime_of_birth,
            gender=gender
        )

        self._mediator.publish(
            med_card.pull_events()
        )

        try:
            self._db_gateway.med_card_repo.add_med_card(med_card)
            self._db_gateway.commit()
        except (CurrentPatientAlreadyHaveMedCard, PatientNotFound):
            self._db_gateway.rollback()
