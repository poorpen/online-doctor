from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.value_objects.string import NonEmptyText


class AnamnesisMorbi(NonEmptyText):
    pass


class TreatmentPlan(NonEmptyText):
    pass


class Diagnosis(NonEmptyText):
    max_len: int = 100


class DoctorUUID(UUIDVO):
    pass
