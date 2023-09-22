from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.domain.value_objects.string import NonEmptyText


class FirstName(NonEmptyText):
    max_len: int = 60


class LastName(NonEmptyText):
    max_len: int = 60


class MiddleName(NonEmptyText):
    max_len: int = 60
