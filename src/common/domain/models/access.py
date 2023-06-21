from uuid import UUID

from dataclasses import dataclass

from src.common.domain.enum.access_level import LevelName
from src.common.domain.value_objects.identifiers import UUIDVO


@dataclass(frozen=True)
class Access:
    user_uuid: UUIDVO
    access_name: LevelName

