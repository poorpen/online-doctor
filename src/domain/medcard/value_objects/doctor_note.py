from dataclasses import dataclass

from src.domain.common.value_objects.string import NonEmptyText


class AnamnesisMorbi(NonEmptyText):
    pass


class TreatmentPlan(NonEmptyText):
    pass


@dataclass(frozen=True)
class Diagnosis(NonEmptyText):
    max_len: int = 100
