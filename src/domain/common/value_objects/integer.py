from dataclasses import dataclass

from src.domain.common.value_objects.base import BaseValueObject


@dataclass(frozen=True, init=False)
class PositiveInteger(BaseValueObject[int]):
    min_value: int = 0

    @classmethod
    def _validate(cls, v: int) -> None:
        if v < cls.min_value:
            raise ValueError('value less than minimum value')

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value


@dataclass(frozen=True, init=False)
class IntegerInRange(BaseValueObject[int]):
    min_value: int
    max_value: int

    @classmethod
    def _validate(cls, v: int) -> None:
        if not cls.min_value <= v <= cls.max_value:
            raise ValueError('value uot of range')

