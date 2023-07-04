from src.common.application.interfaces.db_gateway import DBGateway

from src.application.med_card.interfaces.med_card_repo import MedCardRepo
from src.application.med_card.interfaces.med_card_reader import MedCardReader


class MedCardDBGateway(DBGateway):
    med_card_repo: MedCardRepo
    med_card_reader: MedCardReader
