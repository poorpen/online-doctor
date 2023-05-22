from dataclasses import dataclass
from typing import Any

from src.common.domain.value_objects.base import BaseValueObject

from src.common.domain.value_objects.identifiers import ID


@dataclass
class DomainException(Exception):
    value: Any

    def __init__(self, value: BaseValueObject):
        self.value = value.get_value()

