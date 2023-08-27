from uuid import UUID

from src.common.domain.utils.base_specification import Specification
from src.common.domain.models.access import Access
from src.common.domain.enum.access_level import LevelName


class AccessSpecification(Specification[Access]):
    pass


class IsDoctor(AccessSpecification):

    def is_satisfied_by(self, candidate: Access) -> bool:
        return candidate.access_name == LevelName.DOCTOR


class IsPatient(AccessSpecification):

    def is_satisfied_by(self, candidate: Access) -> bool:
        return candidate.access_name == LevelName.PATIENT


class UserUUIDMatches(AccessSpecification):

    def __init__(self, other_uuid: UUID):
        self.other_uuid = other_uuid

    def is_satisfied_by(self, candidates: Access) -> bool:
        return candidates.user_uuid == self.other_uuid
