from dataclasses import dataclass

from src.domain.common.value_objects.base import BaseVO


@dataclass(frozen=True)
class PositiveInteger(BaseVO[int]):
    min_value: int = 0

    @classmethod
    def _validate(cls, v):
        if v < cls.min_value:
            raise ValueError('value less than minimum value')
