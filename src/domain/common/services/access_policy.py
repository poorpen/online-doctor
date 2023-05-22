from src.domain.common.services.specification import Specification
from src.domain.common.models.access import Access
from src.domain.common.enum.access_level import LevelName


class IsDoctor(Specification):

    def is_satisfied_by(self, candidate: Access) -> bool:
        return candidate.access_name == LevelName.DOCTOR


class IsPatient(Specification):

    def is_satisfied_by(self, candidate: Access) -> bool:
        return candidate.access_name == LevelName.PATIENT


class DoctorUUIDMatches(Specification):

    def __init__(self, other_doctor_uuid):
        self.other_doctor_uuid = other_doctor_uuid

    def is_satisfied_by(self, candidates: Access) -> bool:
        return candidates.user_uuid == self.other_doctor_uuid


class PatientUUIDMatches(Specification):

    def __init__(self, other_patient_uuid):
        self.other_patient_uuid = other_patient_uuid

    def is_satisfied_by(self, candidates: Access) -> bool:
        return candidates.user_uuid == self.other_patient_uuid
