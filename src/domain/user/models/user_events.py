from uuid import UUID
from datetime import datetime
from dataclasses import dataclass

from src.common.domain.models.event import Event


@dataclass(frozen=True)
class UserCreated(Event):
    user_uuid: UUID
    date_time_of_birth: datetime
