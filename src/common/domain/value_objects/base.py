from typing import TypeVar, Generic, Any
from dataclasses import dataclass

T = TypeVar("T")


@dataclass(frozen=True)
class BaseValueObject(Generic[T]):
    value: T

    def get_value(self) -> T:
        return self.value

    @classmethod
    def _validate(cls, v: T) -> None:
        pass

    @staticmethod
    def _value_getter(other) -> Any:
        if isinstance(other, BaseValueObject):
            other = other.get_value()
        return other

    def __new__(cls, v: T) -> 'BaseValueObject':
        cls._validate(v)
        return super().__new__(cls)

    def __add__(self, other):
        res = self.value + self._value_getter(other)
        return self.__class__(res)

    def __sub__(self, other):
        res = self.value - self._value_getter(other)
        return self.__class__(res)

    def __eq__(self, other):
        return self.value == self._value_getter(other)

    def __ne__(self, other):
        return self.value != self._value_getter(other)

    def __lt__(self, other):
        return self.value < self._value_getter(other)

    def __gt__(self, other):
        return self.value > self._value_getter(other)

    def __le__(self, other):
        return self.value <= self._value_getter(other)

    def __ge__(self, other):
        return self.value >= self._value_getter(other)
