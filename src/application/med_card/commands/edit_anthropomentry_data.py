from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.services.access_policy import IsPatient, UserUUIDMatches
from src.common.application.commands.base import CommandHandler
from src.common.application.interfaces.identity_provider import IIdentityProvider
from src.common.application.interfaces.mediator import IMediator
from src.common.application.exceptions.access import AccessDenied

from src.domain.med_card.value_objects.med_card import Height, Weight
from src.application.med_card.models.command import EditAnthropometryData
from src.application.med_card.interfaces.med_card_db_gateway import IMedCardDBGateway
from src.application.med_card.exceptions.med_card import MedCardNotFound


class EditAnthropometryDataCommand(CommandHandler):

    def __init__(self, db_gateway: IMedCardDBGateway, identity_provider: IIdentityProvider, mediator: IMediator):
        self._db_gateway = db_gateway
        self._identity_provider = identity_provider
        self._mediator = mediator

    def __call__(self, command_data: EditAnthropometryData) -> None:
        med_card_uuid = UUIDVO(command_data.med_card_uuid)
        height = Height(command_data.height)
        weight = Weight(command_data.weight)

        med_card = self._db_gateway.med_card_repo.get_med_card_by_uuid(med_card_uuid)

        access_policy = self._identity_provider.get_access_policy()
        can_edit_anthropometry_data = IsPatient() & UserUUIDMatches(med_card.get_patient_uuid)
        if not can_edit_anthropometry_data.is_satisfied_by(access_policy):
            raise AccessDenied(access_policy.user_uuid)

        med_card.edit_anthropometry_data(weight=weight, height=height)

        self._mediator.publish(
            med_card.pull_events()
        )

        try:
            self._db_gateway.med_card_repo.update_med_card(med_card)
            self._db_gateway.commit()
        except MedCardNotFound:
            self._db_gateway.rollback()
