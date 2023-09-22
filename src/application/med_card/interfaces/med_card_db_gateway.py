from src.common.application.interfaces.db_gateway import IDBGateway

from src.application.med_card.interfaces.med_card_reader import IMedCardReader
from src.application.med_card.interfaces.med_card_repo import IMedCardRepo


class IMedCardDBGateway(IDBGateway):
    med_card_reader: IMedCardReader
    med_card_repo: IMedCardRepo
