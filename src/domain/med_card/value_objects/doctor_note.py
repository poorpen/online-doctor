from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.value_objects.string import NonEmptyText


class AnamnesisMorbi(NonEmptyText):
    max_len: int = 350


class TreatmentPlan(NonEmptyText):
    max_len: int = 350


class Diagnosis(NonEmptyText):
    max_len: int = 255


class DoctorUUID(UUIDVO):
    pass
