from uuid import UUID

from dataclasses import dataclass

from src.domain.common.enum.access_level import LevelName


@dataclass(frozen=True)
class Access:
    user_uuid: UUID
    access_name: LevelName

