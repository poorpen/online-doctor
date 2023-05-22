import uuid
from typing import Protocol

from src.common.domain.value_objects.identifiers import UUIDVO

class IConsultationRepo(Protocol):

    def is_active(self, consultation_uuid: UUIDVO) -> bool:
        raise NotImplemented