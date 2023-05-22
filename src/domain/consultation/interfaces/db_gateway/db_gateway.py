from typing import Protocol

from src.domain.consultation.interfaces.repo.consultaton_repo import IConsultationRepo


class IDBGateway(Protocol):
    consultation_repo: IConsultationRepo
