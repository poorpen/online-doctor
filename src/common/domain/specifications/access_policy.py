from src.common.domain.specifications.base import Specification
from src.common.domain.models.access import Access
from src.common.domain.enum.access_level import LevelName


class IsDoctor(Specification):

    def is_satisfied_by(self, candidate: Access) -> bool:
        return candidate.access_name == LevelName.DOCTOR


class IsPatient(Specification):

    def is_satisfied_by(self, candidate: Access) -> bool:
        return candidate.access_name == LevelName.PATIENT


class UserUUIDMatches(Specification):

    def __init__(self, other_uuid):
        self.other_uuid = other_uuid

    def is_satisfied_by(self, candidates: Access) -> bool:
        return candidates.user_uuid == self.other_uuid
