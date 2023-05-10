from dataclasses import dataclass

from base import BaseVO


@dataclass(frozen=True)
class FloatInRange(BaseVO[float]):
    min_value: float = 0.0
    max_value: float = 10.0

    @classmethod
    def _validate(cls, v):
        if not cls.min_value <= v <= cls.max_value:
            raise ValueError('value uot of range')
