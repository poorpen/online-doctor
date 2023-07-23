from src.common.application.interfaces.db_gateway import DBGateway

from src.application.med_card.interfaces.med_card_reader import MedCardReader
from src.application.med_card.interfaces.med_card_repo import MedCardRepo


class MedCardDBGateway(DBGateway):
    med_card_reader: MedCardReader
    med_card_repo: MedCardRepo
