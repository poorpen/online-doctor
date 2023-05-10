from dataclasses import dataclass

from src.domain.common.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class NonEmptyString(BaseValueObject[str]):

    @classmethod
    def _validate(cls, v: str) -> None:
        if not v or v.isspace():
            raise ValueError()


@dataclass(frozen=True)
class Text(BaseValueObject[str]):
    max_len: int = 500

    @classmethod
    def _validate(cls, v: str) -> None:
        if len(v) > cls.max_len:
            raise ValueError(f'text lenght exceeds the allowed threshold of {cls.max_len} characters')

