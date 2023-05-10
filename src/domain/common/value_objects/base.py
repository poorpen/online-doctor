from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T")


@dataclass(frozen=True)
class BaseVO(Generic[T]):
    value: T

    @classmethod
    def _validate(cls, v):
        ...

    @classmethod
    def _validate_type(cls, v):
        current_type = cls.__orig_bases__[0].__args__[0]
        if not isinstance(v, current_type):
            raise TypeError(f'value must match the type {current_type}')

    def __new__(cls, v):
        cls._validate_type(v)
        cls._validate(v)
        return super().__new__(cls)

