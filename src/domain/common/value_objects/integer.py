from dataclasses import dataclass

from src.domain.common.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class PositiveInteger(BaseValueObject[int]):
    min_value: int = 0

    @classmethod
    def _validate(cls, v: int) -> None:
        if v < cls.min_value:
            raise ValueError('value less than minimum value')


@dataclass(frozen=True)
class IntegerInRange(BaseValueObject[int]):
    min_value: int = 0.0
    max_value: int = 10.0

    @classmethod
    def _validate(cls, v: int) -> None:
        if not cls.min_value <= v <= cls.max_value:
            raise ValueError('value uot of range')
